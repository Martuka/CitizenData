#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import nltk
import treetaggerwrapper
import time
from initiative import Initiative
from utils import *


def main():
	config = configparser.ConfigParser()
	config.read('config.conf')
	dataset_chron_file = config['DEFAULT']['dataset_chron_file']
	dataset_dechron_file = config['DEFAULT']['dataset_dechron_file']
	tagdir = config['DEFAULT']['tagdir']

	# tokenizer to split text by sentences
	# tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')

	# tokenizer to split text by words
	tokenizer = nltk.tokenize.TreebankWordTokenizer()

	# tagger initialisation for french pos tagging
	tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR=tagdir)

	initiatives_list = list()
	dataset = list_the_file(dataset_dechron_file)

	# create list of initiatives from the dataset
	for i in range(len(dataset)):
		if (dataset[i] != '') and (dataset[i][0] == "#"):
			initiative = Initiative(dataset[i+1], dataset[i+3])
			initiatives_list.append(initiative)
		else:
			continue

	# text analyze and predictions
	for i in range(len(initiatives_list)):
		# display_text_in_tty(None)
		analyze_current_dataset(tokenizer, tagger, initiatives_list[0:i+1])
		# display_word_info()
		# display_prediction()
		print("\n\nSleep 4 seconds...")
		time.sleep(4)

if __name__ == "__main__":
	main()
