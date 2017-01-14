# -*- coding: utf-8 -*-

import operator
import random
import treetaggerwrapper
from collections import Counter, defaultdict
from multiprocessing.pool import Pool


# dictionaries of type {'word': []}
nouns_matrix_chron = defaultdict(lambda: [])
nouns_matrix_dechron = defaultdict(lambda: [])
adj_matrix_chron = defaultdict(lambda: [])
adj_matrix_dechron = defaultdict(lambda: [])
verbs_matrix_chron = defaultdict(lambda: [])
verbs_matrix_dechron = defaultdict(lambda: [])
pour_matrix_chron = defaultdict(lambda: [])
pour_matrix_dechron = defaultdict(lambda: [])
contre_matrix_chron = defaultdict(lambda: [])
contre_matrix_dechron = defaultdict(lambda: [])

loop_count = 0


def list_the_file(path):
    """Reads a file and puts each line in
    a list of strings. Removes the '\n'
    characters
    """
    text = open(path, 'r')
    res = text.read().splitlines()
    text.close()
    return res


def lowercase_list(lst):
    return [item.lower() for item in lst]


def display_initiative_text(initiative):
    print("display_initiative_text not implemented yet")


def display_top_words(top_words):
    print("display_word_info not implemented yet")


def display_date(date):
    print("Not implemented yet")


def display_prediction(text):
    print("display_prediction not implemented yet")


def get_most_frequent_words_tuples(dico):
    return sorted(dico.items(), key=lambda x: x[1][-1], reverse=True)


def sort_list_of_tuples(lst, total):
    """Takes a list of words and returns
    a sorted list of tuples of its words
    and count
    """
    tmp = dict(Counter(lst))
    for k, v in tmp.items():
        tmp[k] = v/total
    return sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)


def get_list_predictions(lst):
    """"From an ordered list of tuples, returns an ordered list of
    tuples as (word, [freq, pred])
    """
    tmp = {}
    for tpl in lst:
        try:
            a = tpl[1][-2]
        except IndexError:
            a = 0
        b = tpl[1][-1]
        tmp[tpl[0]] = [b, get_prediction(a, b)]
        # pred = "{0:.5f}".format(random.random())
        # ans[tpl[0]] = ["{0:.5f}".format(tpl[1]), pred]
    return get_most_frequent_words_tuples(tmp)


def get_opinion_prediction(mtrx):
    res = []
    for k, v in mtrx.items():
        res.append(k)
        try:
            a = v[-2]
        except IndexError:
            a = 0
        b = v[-1]
        res.append([v[-1], get_prediction(a, b)])
    return res


def feed_matrix(mtrx, lst):
    """takes an ordered list of tuples
    and add them in the specified matrix
    """
    for tpl in lst:
        mtrx[tpl[0]].append(tpl[1])
    # for key, value in mtrx.items():
    #     if len(value) < loop_count:
    #         mtrx[key].append(mtrx[key][-1])
    for key, value in mtrx.items():
        if len(value) < loop_count:
            mtrx[key].insert(0, 0)


def merge_tuple_list(lst1, lst2):
    counter = Counter(dict(lst1)) + Counter(dict(lst2))
    return sorted(counter.items(), key=operator.itemgetter(1), reverse=True)


def treat_current_dataset(tokenizer, tagger, partial_chron, partial_dechron):
    """Handles the growing list of initiatives chronologically and
    dechronologically, performs analyses and predictions
    """
    global loop_count
    loop_count += 1
    print("\nLoop number {}".format(loop_count))

    current_initiative_chron = partial_chron[-1]
    current_initiative_dechron = partial_dechron[-1]

    global nouns_matrix_chron
    global nouns_matrix_dechron
    global adj_matrix_chron
    global adj_matrix_dechron
    global verbs_matrix_chron
    global verbs_matrix_dechron

    # WTF DOES IT NOT WORK ???
    # with Pool() as pool:
    #     result_chron = pool.apply_async(extract_top_words, args=(tokenizer, tagger, partial_chron,))
    #     result_dechron = pool.apply_async(extract_top_words, args=(tokenizer, tagger, partial_dechron, ))
    #
    # values_chron = result_chron.get()
    # values_dechron = result_dechron.get()

    values_chron = extract_top_words(tokenizer, tagger, partial_chron)
    values_dechron = extract_top_words(tokenizer, tagger, partial_dechron)

    # update the nouns matrix
    feed_matrix(nouns_matrix_chron, values_chron['nouns'])
    feed_matrix(nouns_matrix_dechron, values_dechron['nouns'])
    feed_matrix(adj_matrix_chron, values_chron['adjectives'])
    feed_matrix(adj_matrix_dechron, values_dechron['adjectives'])
    feed_matrix(verbs_matrix_chron, values_chron['verbs'])
    feed_matrix(verbs_matrix_dechron, values_dechron['verbs'])
    feed_matrix(pour_matrix_chron, values_chron['pour'])
    feed_matrix(pour_matrix_dechron, values_dechron['pour'])
    feed_matrix(contre_matrix_chron, values_chron['contre'])
    feed_matrix(contre_matrix_dechron, values_dechron['contre'])

    # print("\nOrdered nouns chron : ")
    # print(values_chron['nouns'])
    # print("\nNouns matrix chron : ")
    # print(nouns_matrix_chron)

    # data for chronological screen
    date_chron = current_initiative_chron.date
    top_20_nouns_chron = get_most_frequent_words_tuples(nouns_matrix_chron)[:20]
    top_20_adj_chron = get_most_frequent_words_tuples(adj_matrix_chron)[:20]
    top_20_verbs_chron = get_most_frequent_words_tuples(verbs_matrix_chron)[:20]

    # print("\nTop 20 nouns ordered list of frequencies:")
    # print(top_20_nouns_chron)
    # print("Pour matrix = ", pour_matrix_chron)

    # data for dechronological screen
    date_dechron = current_initiative_dechron.date
    top_20_nouns_dechron = get_most_frequent_words_tuples(nouns_matrix_dechron)[:20]
    top_20_adj_dechron = get_most_frequent_words_tuples(adj_matrix_dechron)[:20]
    top_20_verbs_dechron = get_most_frequent_words_tuples(verbs_matrix_dechron)[:20]

    # predictions
    nouns_chron_prediction_list = get_list_predictions(top_20_nouns_chron)
    adj_chron_prediction_list = get_list_predictions(top_20_adj_chron)
    verbs_chron_prediction_list = get_list_predictions(top_20_verbs_chron)

    pour_chron_predictions_list = get_opinion_prediction(pour_matrix_chron)
    contre_chron_predictions_list = get_opinion_prediction(contre_matrix_chron)

    nouns_dechron_prediction_list = get_list_predictions(top_20_nouns_dechron)
    adj_dechron_prediction_list = get_list_predictions(top_20_adj_dechron)
    verbs_dechron_prediction_list = get_list_predictions(top_20_verbs_dechron)

    pour_dechron_predictions_list = get_opinion_prediction(pour_matrix_dechron)
    contre_dechron_predictions_list = get_opinion_prediction(contre_matrix_dechron)



def extract_top_words(tokenizer, tagger, partial_list):
    # Structures of interest
    title_tokens = []
    content_tokens = []

    nouns = []
    adjectives = []
    verbs = []
    adverbs = []
    preps = []
    conj = []
    others = []

    top_nouns = []
    top_adjectives = []
    top_verbs = []

    for_count = 0
    against_count = 0

    # Seperate in words each initiatives of the list
    for initiative in partial_list:
        # words list from titles
        title_tokens += tokenizer.tokenize(initiative.title)
        # words list from contents
        content_tokens += tokenizer.tokenize(initiative.content)
        if initiative.opinion == 'pour':
            for_count += 1
        else:
            against_count += 1

    text_tokens = lowercase_list(title_tokens + content_tokens)

    # date of last initiative from the list (last one added)
    current_date = partial_list[-1].date

    # pos tags list from words
    text_tags = treetaggerwrapper.make_tags(tagger.tag_text(text_tokens))
    for tag in text_tags:
        if tag.pos == 'NOM':
            nouns.append(tag.lemma)
        elif tag.pos == 'ADJ':
            adjectives.append(tag.lemma)
        elif tag.pos[0:3] == 'VER':
            verbs.append(tag.lemma)
        elif tag.pos == 'ADV':
            adverbs.append(tag.lemma)
        elif tag.pos[0:3] == 'PRP':
            preps.append(tag.lemma)
        elif tag.pos == "KON":
            conj.append(tag.lemma)
        else:
            others.append(tag.lemma)

    total_word_count = len(text_tokens)
    # # ordered list of tuples (word, frequency), by frequencies
    # words_frequency = sort_list_of_tuples(text_tokens)
    # ordered list of tuples (nouns, freq)
    ordered_nouns = sort_list_of_tuples(nouns, total_word_count)
    # ordered list of tuples (adjectives, freq)
    ordered_adjectives = sort_list_of_tuples(adjectives, total_word_count)
    # ordered list of tuples (verbs, freq)
    ordered_verbs = sort_list_of_tuples(verbs, total_word_count)

    # make a list of words of interest (nouns, adjectives, verbs)
    selected_words = nouns + adjectives + verbs
    # ordered list of tuples ()
    ordered_words = sort_list_of_tuples(selected_words, total_word_count)

    result = {}
    result["words"] = ordered_words
    result["nouns"] = ordered_nouns
    result["adjectives"] = ordered_adjectives
    result["verbs"] = ordered_verbs
    result["pour"] = [('pour', for_count/total_word_count)]
    result["contre"] = [('contre', against_count/total_word_count)]
    return result


# Reads all words from dataset to get all possible POS
def get_full_pos_set(dataset_path):
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',
        TAGDIR='/Users/lweingart/Applications/tree-tagger')

    textfile = open(dataset_path, 'r')
    text = textfile.read()
    textfile.close()
    tags = tagger.tag_text(text)
    pretty_tags = treetaggerwrapper.make_tags(tags, True)
    poss = [tag.pos for tag in pretty_tags]
    pos_set = set(poss)
    return pos_set


def get_prediction(a, b):
    scale = abs(b - a)
    return a + fibo_ratios[loop_count % 7] * a

pos_dict = {
    'ABR': 'abreviation',
    'ADJ': 'adjectif',
    'ADV': 'adverbe',
    'DET:ART': 'article',
    'DET:POS': 'pronom possessif',
    'KON': 'conjonction',
    'NAM': 'nom propre',
    'NOM': 'nom',
    'NUM': 'nombre',
    'PRO:DEM': 'pronom demonstratif',
    'PRO:IND': 'pronom indefini',
    'PRO:PER': 'pronom personnel',
    'PRO:POS': 'pronom possessif',
    'PRO:REL': 'pronom relatif',
    'PRP': 'preposition',
    'PRP:det': 'preposition plus article',
    'PUN': 'ponctuation',
    'PUN:cit': 'ponctuation citation',
    'SENT': 'sentence tag ??',
    'SYM': 'symbole',
    'VER:cond': 'verbe conditionnel',
    'VER:impf': 'verbe imparfait',
    'VER:infi': 'verbe infinitif',
    'VER:futu': 'verbe futur',
    'VER:pper': 'verbe participe passe',
    'VER:ppre': 'vebre participe present',
    'VER:pres': 'verbe present',
    'VER:simp': 'verbe passe simple',
    'VER:subi': 'verbe subjonctif imparfait',
    'VER:subp': 'verbe subjonctif present'
}

fibo_ratios = {
    0: 0,
    1: 0.236,
    2: 0.382,
    3: 0.5,
    4: 0.618,
    5: 0.764,
    6: 1
}
