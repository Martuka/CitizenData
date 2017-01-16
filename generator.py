#!/usr/bin/env python
# handle automatic text generation


import configparser
import nltk
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import utils
from initiative import Initiative


def init_grammar(nouns, adjs, verbs):
    rules = """% start S
S -> PRP NP CP
NP -> DET NOM ADJ
CP -> PRP NOM ADJ PUN | DET NON ADJ PUN
"""
    prp = "PRP -> 'Pour' | 'Contre'"
    det = "DET -> 'le' | 'la' | 'un' | 'une'"
    nom = "NOM -> '"
    adj = "ADJ -> '"
    verb = "VER -> '"
    pun = "PUN -> '.' | '!'"
    nom += "' | '".join(nouns) + "'"
    adj += "' | '".join(adjs) + "'"
    verb += "' | '".join(verbs) + "'"

    rules += prp + "\n" + det + "\n" + nom + \
            "\n" + adj + "\n" + verb + "\n" + pun

    with open("data/citizen_grammar.cfg", "w") as text_file:
        print(rules, file=text_file)

    grammar = CFG.fromstring(open("data/citizen_grammar.cfg", 'r').read())
    with open("logs.txt", "a") as text_file:
        print("grammar = {}".format(grammar), file=text_file)
    return grammar


def generate_initiative(nouns, adjs, verbs):
    grammar = init_grammar(nouns, adjs, verbs)
    # print(grammar)

    # for sentence in generate(grammar, depth=1000):
    #     print(' '.join(sentence))

    results = generate(grammar)

    return results


# generate_initiative(['confédération', 'Suisse', 'vache', 'camouflage', 'armée'],
#                     ['robuste', 'salace', 'cryptique','indispensable'],
#                     ['manger', 'refuser'])
