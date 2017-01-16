# -*- coding: utf-8 -*-

import operator
import random
from collections import Counter, defaultdict
from multiprocessing.pool import Pool
import treetaggerwrapper
import config


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
    for key, value in mtrx.items():
        if len(value) < loop_count:
            mtrx[key].insert(0, 0)


def merge_tuple_list(lst1, lst2):
    counter = Counter(dict(lst1)) + Counter(dict(lst2))
    return sorted(counter.items(), key=operator.itemgetter(1), reverse=True)


def extract_top_words(tokenizer, tagger, partial_list):
    # print("extract top words function started...")
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
    text_tags = treetaggerwrapper.make_tags(tagger.tag_text(text_tokens), True)
    for tag in text_tags:
        if tag.pos == 'NOM':
            nouns.append(tag.word)
        elif tag.pos == 'ADJ':
            adjectives.append(tag.word)
        elif tag.pos[0:3] == 'VER':
            if tag.lemma == "c":
                pass
            else:
                verbs.append(tag.lemma)
        elif tag.pos == 'ADV':
            adverbs.append(tag.word)
        elif tag.pos[0:3] == 'PRP':
            preps.append(tag.word)
        elif tag.pos == "KON":
            conj.append(tag.word)
        else:
            others.append(tag.word)

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


def reduce_too_high_frequencies(mx, dic):
    """reduce some too frequent words frequencies
    """
    for k, v in mx.items():
        if k in dic.keys():
            mx[k] = list(map(lambda x: x*dic[k], mx[k]))
    return mx


def treat_current_dataset(tokenizer, tagger, partial_chron, partial_dechron):
    """Handles the growing list of initiatives chronologically and
    dechronologically, performs analyses and predictions
    """
    global loop_count
    loop_count += 1
    # print("\nLoop number {}".format(loop_count))

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
    #     result_dechron = pool.apply_async(extract_top_words, args=(tokenizer, tagger, partial_dechron,))
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

    # data for chronological screen
    date_chron = current_initiative_chron.date

    # reduce some too frequent words frequencies
    mx_n = reduce_too_high_frequencies(nouns_matrix_chron, coeff_nouns)
    # with open("logs.txt", "a") as text_file:
    #     print("\nnouns matrix = {}".format(nouns_matrix_chron), file=text_file)
    #     print("\nmn matrix = {}".format(mx_n), file=text_file)
    top_20_nouns_chron = get_most_frequent_words_tuples(mx_n)[:20]
    mx_a = reduce_too_high_frequencies(adj_matrix_chron, coeff_adj)
    config.top_20_adj_chron = get_most_frequent_words_tuples(mx_a)[:20]

    # warning, here we take the 20 least used verbs
    config.top_20_verbs_chron = get_most_frequent_words_tuples(verbs_matrix_chron)[::-1][:20]

    # data for dechronological screen
    date_dechron = current_initiative_dechron.date

    # reduce some too frequent word frequencies
    mx_n2 = reduce_too_high_frequencies(nouns_matrix_dechron, coeff_nouns)
    top_20_nouns_dechron = get_most_frequent_words_tuples(mx_n2)[:20]
    mx_a2 = reduce_too_high_frequencies(adj_matrix_dechron, coeff_adj)
    config.top_20_adj_dechron = get_most_frequent_words_tuples(mx_a2)[:20]

    # warning, here we take the 20 least used verbs
    config.top_20_verbs_dechron = get_most_frequent_words_tuples(verbs_matrix_dechron)[::-1][:20]

    # predictions
    # global nouns_chron_prediction_list
    config.nouns_chron_predictions_list = get_list_predictions(top_20_nouns_chron)
    config.adj_chron_predictions_list = get_list_predictions(config.top_20_adj_chron)
    config.verbs_chron_predictions_list = get_list_predictions(config.top_20_verbs_chron)

    config.pour_chron_predictions_list = get_opinion_prediction(pour_matrix_chron)
    config.contre_chron_predictions_list = get_opinion_prediction(contre_matrix_chron)

    config.nouns_dechron_predictions_list = get_list_predictions(top_20_nouns_dechron)
    config.adj_dechron_predictions_list = get_list_predictions(config.top_20_adj_dechron)
    config.verbs_dechron_predictions_list = get_list_predictions(config.top_20_verbs_dechron)

    config.pour_dechron_predictions_list = get_opinion_prediction(pour_matrix_dechron)
    config.contre_dechron_predictions_list = get_opinion_prediction(contre_matrix_dechron)

    # print("\nNouns chron predictions = ")
    # print(nouns_chron_prediction_list)


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
    return a + fibo_ratios[random.randrange(0, 19)] * scale


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
    6: 1,
    7: 1.236,
    8: 1.382,
    9: 1.5,
    10: 1.618,
    11: 1.764,
    12: 2,
    13: 2.236,
    14: 2.382,
    15: 2.5,
    16: 2.618,
    17: 2.764,
    18: 3
}

coeff_nouns = {
    'confédération': 0.1,
    'cantons': 0.05,
    'droit': 0.3,
    'mesures': 0.2,
    'personnes': 0.8,
    'impôt': 0.05,
    'cas': 0.1,
    'protection': 0.8,
    'loi': 0.5,
    'assurance': 0.3,
    'constitution': 0.1,
    'législation': 0.1,
    'disposition': 0.05,
    'prix': 0.1,
    'conseil': 0.1,
    'dispositions': 0.05,
    'impôts': 0.1,
    'droits': 0.1,
    'suisse': 0.1,
    'article': 0.1,
    'personnes': 0.1,
    'citoyens': 0.05,
    'pays': 0.1,
    'service': 0.1,
    'peuple': 0.1,
    'travail': 0.1,
    'ans': 0.1,
    'revenu': 0.1,
    'membres': 0.1,
    'durée': 0.1,
    'protection': 0.1,
    'autorisation': 0.1,
    'voie': 0.1,
    'taux': 0.1,
    'base': 0.1,
    'environnement': 0.1,
    'population': 0.1,
    'prestations': 0.05,
    'salaires': 0.1,
    'salaires': 0.1,
    'population': 0.1,
    'territoire': 0.1,
    "l'environnement": 0.05,
    "l'impôt": 0.1


}

coeff_adj = {
    'fédéral': 0.1,
    'fédérale': 0.1,
    'suisse': 0.1,
    'autres': 0.1,
    'remplacé': 0.1,
    'nationale': 0.5,
    'générale': 0.1,
    'obligatoire': 0.5,
    'public': 0.8,
    'nécessaires': 0.7,
    "national": 0.1
}
