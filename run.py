#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import nltk
import treetaggerwrapper
import time
from initiative import Initiative
from utils import *
import gui


def main():

    gui.init()

    # read config file
    config = configparser.ConfigParser()
    config.read('config.conf')
    dataset_dechron_file = config['DEFAULT']['dataset_dechron_file']
    tagdir = config['DEFAULT']['tagdir']

    # tokenizer to split text by sentences
    # tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')

    # tokenizer to split text by words
    tokenizer = nltk.tokenize.TreebankWordTokenizer()

    # tagger initialisation for french pos tagging
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR=tagdir)

    dataset = list_the_file(dataset_dechron_file)

    initiatives_list_dechron = []

    # create list of initiatives from the dataset
    # (dechronological order, as per the file)
    for i in range(len(dataset)):
        opinion = ''
        if (dataset[i] != '') and (dataset[i][0] == "#"):
            if dataset[i+1][0:4] == "Pour":
                opinion = 'pour'
            elif dataset[i+1][0:4] == "Cont":
                opinion = 'contre'
            initiative = Initiative(dataset[i+1], dataset[i+3], dataset[i][1:5], opinion)
            initiatives_list_dechron.append(initiative)
        else:
            continue

    initiatives_list_chron = initiatives_list_dechron[::-1]

    # text analyze and predictions
    for i in range(len(initiatives_list_chron)):
        treat_current_dataset(tokenizer, tagger, initiatives_list_chron[0:i+1], initiatives_list_dechron[0:i+1])
        initiative = initiatives_list_chron[i]
        gui.print_srt(gui.inner_text_win, 2, 1, initiative.title)
        gui.print_srt(gui.inner_text_win, 3, 1, initiative.content)
        gui.display_year(gui.win_date, initiative.date, "green")

        # gui.win_nouns

        # sleep 4 seconds
        time.sleep(4)

if __name__ == "__main__":
    main()
