#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import nltk
import treetaggerwrapper
import time
from initiative import Initiative
import utils
import gui
import config
import generator


def main():

    gui.init()

    # read config file
    conf = configparser.ConfigParser()
    conf.read('config.conf')
    dataset_dechron_file = conf['DEFAULT']['dataset_dechron_file']
    tagdir = conf['DEFAULT']['tagdir']
    grammar_file = conf['DEFAULT']['grammar_file']

    # tokenizer to split text by sentences
    # tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')

    # tokenizer to split text by words
    tokenizer = nltk.tokenize.TreebankWordTokenizer()

    # tagger initialisation for french pos tagging
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR=tagdir)

    dataset = utils.list_the_file(dataset_dechron_file)

    initiatives_list = []

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
            initiatives_list.append(initiative)
        else:
            continue

    initiatives_list_dechron = sorted(initiatives_list, key=lambda initiative: initiative.date, reverse=True)
    initiatives_list_chron = initiatives_list_dechron[::-1]

    # utils.log("initiative list = ", initiatives_list_chron[:5])
    # text analyze and predictions
    for i in range(len(initiatives_list_chron)):
        utils.treat_current_dataset(tokenizer, tagger, initiatives_list_chron[0:i+1], initiatives_list_dechron[0:i+1])

        initiative = initiatives_list_dechron[i]
        gui.print_srt(gui.inner_text_win, 2, 1, initiative.title, initiative.content)
        gui.display_year(gui.win_date, initiative.date)

        gui.print_noun_values(gui.inner_nouns_win, config.nouns_dechron_predictions_list)

        gui.print_opinion_window(gui.win_op, config.pour_dechron_predictions_list, config.contre_dechron_predictions_list)

        gui.print_verb_adj_window(gui.win_adj, config.bottom_20_verbs_dechron, config.top_20_adj_dechron)

        # generate new initiative titles with most or less used words
        nouns = [w for w, p in config.nouns_chron_predictions_list[:3] + \
            config.nouns_dechron_predictions_list[::-1][:3]]
        adjs = [a for a, p in config.top_20_adj_chron[:5] + \
            config.bottom_20_adj_dechron[:5]]
        verbs = [v for v, p in config.bottom_20_verbs_chron[:5] + \
            config.bottom_20_verbs_dechron[:5]]
        with open("listes.txt", "a") as text_file:
            print("\nNouns list = {}".format(nouns), file=text_file)
            print("\nAdjs list = {}".format(adjs), file=text_file)
            print("\nVerbs list = {}".format(verbs), file=text_file)
        titles = generator.generate_initiative(nouns, adjs, verbs)
        with open("generation.txt", "w") as text_file:
            for sentence in titles:
                print("{}".format(' '.join(sentence)), file=text_file)

        # pause to give time to read between initiatives
        time.sleep(1)

if __name__ == "__main__":
    main()
