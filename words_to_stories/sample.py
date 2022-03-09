""" adapted from https://github.com/minimaxir/gpt-2-simple/blob/master/gpt_2_simple/src/sample.py"""

import numpy as np
import tensorflow as tf
import sys
from gpt_2_simple.src import model


def top_k_logits(logits, k):
    if k == 0:
        # no truncation
        return logits

    def _top_k():
        values, _ = tf.nn.top_k(logits, k=k)
        min_values = values[:, -1, tf.newaxis]
        return tf.compat.v1.where(
            logits < min_values,
            tf.ones_like(logits, dtype=logits.dtype) * -1e10,
            logits,
        )

    return tf.cond(
        pred=tf.equal(k, 0),
        true_fn=lambda: logits,
        false_fn=lambda: _top_k(),
    )


def top_p_logits(logits, p):
    with tf.compat.v1.variable_scope('top_p_logits'):
        logits_sort = tf.sort(logits, direction='DESCENDING')
        probs_sort = tf.nn.softmax(logits_sort)
        probs_sums = tf.cumsum(probs_sort, axis=1, exclusive=True)
        logits_masked = tf.compat.v1.where(probs_sums < p, logits_sort, tf.ones_like(
            logits_sort) * 1000)  # [batchsize, vocab]
        min_logits = tf.reduce_min(input_tensor=logits_masked, axis=1, keepdims=True)  # [batchsize, 1]

        return tf.compat.v1.where(
            logits < min_logits,
            tf.ones_like(logits, dtype=logits.dtype) * -1e10,
            logits,
        )


def sample_sequence(target, *, hparams, length, start_token=None,
                    batch_size=None, context=None, temperature=1,
                    top_k=0, top_p=0.0):
    """ Returns a tensor flow graph that contains the tokens of the generated text and (we added) also the
    probability of the target word being selected for each token in the output.
    This function contains the changes we made for our project."""
    if start_token is None:
        assert context is not None, 'Specify exactly one of start_token and context!'
    else:
        assert context is None, 'Specify exactly one of start_token and context!'
        context = tf.fill([batch_size, 1], start_token)


    def step(hparams, tokens, past=None):

        lm_output = model.model(hparams=hparams, X=tokens,
                                past=past, reuse=tf.compat.v1.AUTO_REUSE)

        logits = lm_output['logits'][:, :, :hparams.n_vocab]

        presents = lm_output['present']
        presents.set_shape(model.past_shape(
            hparams=hparams, batch_size=batch_size))
        return {
            'logits': logits,
            'presents': presents,
        }

    with tf.compat.v1.name_scope('sample_sequence'):
        # Don't feed the last context token -- leave that to the loop below
        # TODO: Would be slightly faster if we called step on the entire context,
        # rather than leaving the last token transformer calculation to the while loop.
        context_output = step(hparams, context[:, :-1])
        #pad out the probabilities tensor so it is same size as the tokens list
        #give the target word NINF probability so the index to truncate at will never be part of the prompt
        prob = tf.fill(tf.shape(context), np.NINF)
        def body(past, prev, output, prob, target):
            next_outputs = step(hparams, prev[:, tf.newaxis], past=past)
            logits = next_outputs['logits'][:, -1, :] / tf.cast(temperature, tf.float32)

            #get the probability of the target word and put it in a singleton list so it can be appended to the
            #full tensor
            target_value = logits[0][target]
            target_value = tf.reshape(target_value, [1, 1])

            if top_p > 0.0:
                logits = top_p_logits(logits, p=top_p)
            else:
                logits = top_k_logits(logits, k=top_k)
            samples = tf.random.categorical(
                logits, num_samples=1, dtype=tf.int32)
            return [
                tf.concat([past, next_outputs['presents']], axis=-2),
                tf.squeeze(samples, axis=[1]),
                tf.concat([output, samples], axis=1),
                tf.concat([prob, target_value], axis=1),
                target,
            ]

        def cond(*args):
            return True

        _, _, tokens, prob, target = tf.nest.map_structure(
            tf.stop_gradient,
            tf.while_loop(
                cond=cond,
                body=body,
                maximum_iterations=length,
                loop_vars=[
                    context_output['presents'],
                    context[:, -1],
                    context,
                    #pass the list of probabilities at each index and the target word into each iteration of the loop
                    prob,
                    target,
                ],
                shape_invariants=[
                    tf.TensorShape(model.past_shape(hparams=hparams, batch_size=batch_size)),
                    tf.TensorShape([batch_size]),
                    tf.TensorShape([batch_size, None]),
                    tf.TensorShape([1, None]),
                    tf.TensorShape(None),
                ],
            )
        )
        #combine the probabilities and token sequence into one tensor that can be unpacked in gpt_2.generate
        #I don't think we need to do this but it made more intuitive sense to unpack them together
        tokens = tf.cast(tokens, tf.float32)
        out = tf.stack([tokens, prob])

        return out
