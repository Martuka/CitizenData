#!/usr/bin/env python
# handle automatic text generation


import configparser
import nltk
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import utils
from initiative import Initiative


# def init_grammar(nouns, adjs, verbs):
#     rules = """% start S
# S -> PRP NP CP
# S -> PRP VER NP ADJ PUN
# NP -> DET NOM
# CP -> CAT NOM ADJ PUN
# CP -> NOM ADJ PUN
# CP -> NOM ADJ ET ADJ PUN
# CP -> ADJ
# """
#     prp = "PRP -> 'Pour' | 'Contre'"
#     det = "DET -> 'le' | 'la' | 'un' | 'une'"
#     et = "ET -> 'et'"
#     nom = "NOM -> '"
#     adj = "ADJ -> '"
#     verb = "VER -> '"
#     pun = "PUN -> '.'"
#     cat = "CAT -> 'de' | 'des' | 'du' | 'avec' | 'sans' | 'au' | 'à l\’abri' | 'dans' | 'de la part de' | 'ou' | 'contre'| 'sur' | 'et sans' | 'hors' | 'sur' | 'en cas de' | 'pour' | 'face à' | 'à la' | 'grâce à' | 'non' | 'plus' | 'moins' | 'par' | 'sur la' | 'sur le' | 'à' | 'au' | 'moins'"
#     nom += "' | '".join(nouns) + "'"
#     adj += "' | '".join(adjs) + "'"
#     verb += "' | '".join(verbs) + "'"
#
#     rules += prp + "\n" + det + "\n" + nom + \
#             "\n" + adj + "\n" + verb + "\n" + pun
#
#     with open("data/citizen_grammar.cfg", "w") as text_file:
#         print(rules, file=text_file)
#
#     grammar = CFG.fromstring(open("data/citizen_grammar.cfg", 'r').read())
#
#     return grammar

def init_grammar(nouns, adjs, verbs):
    rules = """% start S
S -> PRP DET NOM CAT NOM ADJ ET ADJ
"""
# S -> PRP VER NP ADJ PUN
# NP -> DET NOM
# CP -> CAT NOM ADJ PUN
# CP -> NOM ADJ PUN
# CP -> NOM ADJ ET ADJ PUN
# CP -> ADJ
    prp = "PRP -> 'Pour' | 'Contre'"
    det = "DET -> 'le' | 'la' | 'un' | 'une'"
    et = "ET -> 'et'"
    nom = "NOM -> '"
    adj = "ADJ -> '"
    verb = "VER -> '"
    pun = "PUN -> '.'"
    cat = "CAT -> 'de' | 'des' | 'du' | 'avec' | 'sans' | 'au' | 'dans' | 'de la part de' | 'ou' | 'contre'| 'sur' | 'hors' | 'pour' | 'face à' | 'à la' | 'grâce à' | 'non' | 'plus' | 'par' | 'sur la' | 'sur le' | 'à' | 'moins'"
    nom += "' | '".join(nouns) + "'"
    adj += "' | '".join(adjs) + "'"
    verb += "' | '".join(verbs) + "'"

    rules += prp + \
            "\n" + det + \
            "\n" + nom + \
            "\n" + adj + \
            "\n" + et + \
            "\n" + cat
            # "\n" + verb + \
            # "\n" + pun + \

    with open("data/citizen_grammar.cfg", "w") as text_file:
        print(rules, file=text_file)

    grammar = CFG.fromstring(open("data/citizen_grammar.cfg", 'r').read())

    utils.log("grammar = ", grammar)

    return grammar


def generate_initiative(nouns, adjs, verbs):
    grammar = init_grammar(nouns, adjs, verbs)
    # print(grammar)

    # for sentence in generate(grammar, depth=1000):
    #     print(' '.join(sentence))

    results = generate(grammar)

    return results
