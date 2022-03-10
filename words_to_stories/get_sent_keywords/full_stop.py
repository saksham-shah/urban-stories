from nltk.tokenize import RegexpTokenizer
import re
import numpy as np

def tokenize(text):
	tokenizer = RegexpTokenizer(r"\w+")
	tokens = tokenizer.tokenize(text.lower())
	return tokens

def get_preceding_words(text):
	pattern = "\w+\."
	matches = re.findall(pattern, text)
	return list(map(lambda x: x.strip(".").lower(), matches))

def count_occurrences(token_list):
	type_counts = {}
	for token in token_list:
		if token not in type_counts.keys():
			type_counts[token] = 0
		type_counts[token] += 1
	return type_counts

def adjust_counts(pre_stop_counts, global_counts):
	max_count = max(list(global_counts.values()))
	for type in pre_stop_counts.keys():
		if type in global_counts.keys():
			global_count = global_counts[type]
			pre_stop_counts[type] /= global_count
			reliability = global_count/max_count
			pre_stop_counts[type] += reliability - 1
		else:
			print("error: token not found globally")
			raise ValueError


def get_sorted_counts(type_counts):
	sorted_types = sorted(type_counts, key=lambda x: type_counts[x], reverse=True)
	return {type: type_counts[type] for type in sorted_types}

def sort_on_count(counts):
	counts = counts.sorted()

def filter_reliable_precedents(adjusted_counts, threshold=0):
	filt =  filter(lambda x: adjusted_counts[x] > threshold, adjusted_counts.keys())
	return list(filt)

def get_common_precedents(text):
	all_tokens = tokenize(text)
	global_type_counts = count_occurrences(all_tokens)

	preceding_words = get_preceding_words(text)
	type_counts = count_occurrences(preceding_words)

	adjust_counts(type_counts, global_type_counts)
	type_counts = get_sorted_counts(type_counts)
	return filter_reliable_precedents(type_counts, 0.001)

if __name__ == "__main__":
	f = open("treasure_island.txt", "r")
	text = f.read()
	precedents = get_common_precedents(text)
	print(precedents)