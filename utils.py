# -*- coding: utf-8 -*-

import treetaggerwrapper


def list_the_file(path):
	text = open(path, 'r')
	res = text.read().splitlines()
	text.close()
	return res


def display_text_in_tty(tty):
	print("display_text_in_tty not implemented yet")


def analyze_current_dataset(tokenizer, tagger, partial_list_of_initiatives):
	title_tokens = []
	content_tokens = []

	nouns_title = []
	adjectives_title = []
	verbs_title = []
	others_title = []

	nouns_content = []
	adjectives_content = []
	verbs_content = []
	others_content = []

	pretty_title_tags = dict()
	pretty_content_tags = dict()

	for_count = 0
	against_count = 0

	for initiative in partial_list_of_initiatives:
		# words list from titles
		title_tokens += tokenizer.tokenize(initiative.title)
		# words list from contents
		content_tokens += tokenizer.tokenize(initiative.content)
		if initiative.title[0:4] == "Pour":
			for_count += 1
		elif initiative.title[0:4] == "Cont":
			against_count +=1


	# pos tags list from titles
	title_tags = treetaggerwrapper.make_tags(tagger.tag_text(title_tokens))
	for tag in title_tags:
		# pos tags dictionary from titles
		pretty_title_tags[tag.lemma] = tag.pos
		if tag.pos == 'NOM':
			nouns_title.append(tag.lemma)
		elif tag.pos == 'ADJ':
			adjectives_title.append(tag.lemma)
		elif tag.pos[0:3] == 'VER':
			verbs_title.append(tag.lemma)
		else:
			others_title.append(tag.lemma)


	# pos tags list from contents
	content_tags = treetaggerwrapper.make_tags(tagger.tag_text(content_tokens))
	for tag in content_tags:
		# pos tags list dictionary from contents
		pretty_content_tags[tag.lemma] = tag.pos
		if tag.pos == 'NOM':
			nouns_content.append(tag.lemma)
		elif tag.pos == 'ADJ':
			adjectives_content.append(tag.lemma)
		elif tag.pos[0:3] == 'VER':
			verbs_content.append(tag.lemma)
		else:
			others_content.append(tag.lemma)


	print("title tokens = ", title_tokens)
	# print("title tags = ", title_tags)
	# print("title pretty tags = ", pretty_title_tags)
	print("content tokens = ", content_tokens)
	# print("content tags = ", content_tags)
	# print("content pretty tags = ", pretty_content_tags)
	# print("analyze_current_dataset not implemented yet")
	print("nouns in titles: ", nouns_title)
	print("adjectives in titles: ", adjectives_title)
	print("verbs in titles: ", verbs_title)
	print("nouns in content: ", nouns_content)
	print("adjectives in content: ", adjectives_content)
	print("verbs in content: ", verbs_content)
	print("Nb 'pour' = ", for_count)
	print("Nb 'contre' = ", against_count)


def display_word_info():
	print("display_word_info not implemented yet")


def display_prediction():
	print("display_prediction not implemented yet")


def get_full_pos_set(dataset_path):
	tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR='/Users/lweingart/Applications/tree-tagger')
	textfile = open(dataset_path, 'r')
	text = textfile.read()
	textfilelclose()
	tags = tagger.tag_text(text)
	pretty_tags = treetaggerwrapper.make_tags(tags, True)
	poss = [tag.pos for tag in pretty_tags]
	pos_set = set(poss)
	return pos_set


def f(x):
	return {
		'ABR':'abreviation',
		'ADJ':'adjectif',
		'ADV':'adverbe',
		'DET:ART':'article',
		'DET:POS':'pronom possessif',
		'KON':'conjonction',
		'NAM':'nom propre',
		'NOM':'nom',
		'NUM':'nombre',
		'PRO:DEM':'pronom demonstratif',
		'PRO:IND':'pronom indefini',
		'PRO:PER':'pronom personnel',
		'PRO:POS':'pronom possessif',
		'PRO:REL':'pronom relatif',
		'PRP':'preposition',
		'PRP:det':'preposition plus article',
		'PUN':'ponctuation',
		'PUN:cit':'ponctuation citation',
		'SENT':'sentence tag ??',
		'SYM':'symbole',
		'VER:cond':'verbe conditionnel',
		'VER:impf':'verbe imparfait',
		'VER:infi':'verbe infinitif',
		'VER:futu':'verbe futur',
		'VER:pper':'verbe participe passe',
		'VER:ppre':'vebre participe present',
		'VER:pres':'verbe present',
		'VER:simp':'verbe passe simple',
		'VER:subi':'verbe subjonctif imparfait',
		'VER:subp':'verbe subjonctif present'
	}[x]
