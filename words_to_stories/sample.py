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
            logits_sort)*1000)  # [batchsize, vocab]
        min_logits = tf.reduce_min(input_tensor=logits_masked, axis=1, keepdims=True)  # [batchsize, 1]

        return tf.compat.v1.where(
            logits < min_logits,
            tf.ones_like(logits, dtype=logits.dtype) * -1e10,
            logits,
        )




def sample_sequence(target,*, hparams, length, start_token=None,
                    batch_size=None, context=None, temperature=1,
                    top_k=0, top_p=0.0):
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

        prob = tf.constant([np.NINF])
        #print(target,"pre")
        #target = tf.constant(1169)
        #print(target,"post")
        def body(past, prev, output,prob,target):
            next_outputs = step(hparams, prev[:, tf.newaxis], past=past)
            logits = next_outputs['logits'][:, -1, :] / tf.cast(temperature, tf.float32)
            target_value = logits[0][target]
            #print(target_value,"target")
            target_value = tf.reshape(target_value,[1])
            #print(target_value)
            #print(prob,"prob")
            #print(tf.concat([prob, target_value], axis=-1))
            #print("target val and probs so far")

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
                tf.concat([prob, target_value], axis=-1),
                target,
            ]

        def cond(*args):
            return True

        _, _, tokens,prob,target= tf.nest.map_structure(
            tf.stop_gradient,
            tf.while_loop(
                cond=cond,
                body=body,
                maximum_iterations=length,
                loop_vars=[
                    context_output['presents'],
                    context[:, -1],
                    context,
                    prob,
                    target,
                ],
                shape_invariants=[
                    tf.TensorShape(model.past_shape(hparams=hparams, batch_size=batch_size)),
                    tf.TensorShape([batch_size]),
                    tf.TensorShape([batch_size, None]),
                    tf.TensorShape(None),
                    tf.TensorShape(None),
                ],
            )
        )
        #print(tokens,prob,"sample_sequence output")
        return tokens,prob
