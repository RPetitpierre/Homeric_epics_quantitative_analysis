
# coding: utf-8

import numpy as np
import pandas as pd

from json import dumps
from collections import OrderedDict

from xmljson import badgerfish as bf
from xmljson import parker, Parker

import xml.etree.ElementTree as et



part_of_speech = {
	'n': 'noun',
	'v': 'verb',
	'a': 'adjective',
	'd': 'adverb',
	'l': 'article',
	'g': 'particle',
	'c': 'conjunction',
	'r': 'preposition',
	'p': 'pronoun',
	'm': 'numeral',
	'i': 'interjection',
	'u': 'punctuation'
}

person = {
	'1': 'first person',
	'2': 'second person',
	'3': 'third person'
}

number = {
	's': 'singular',
	'p': 'plural',
	'd': 'dual'
}

tense = {
	'p': 'present',
	'i': 'imperfect',
	'r': 'perfect',
	'l': 'pluperfect',
	't': 'future perfect',
	'f': 'future',
	'a': 'aorist'
}

mood = {
	'i': 'indicative',
	's': 'subjunctive',
	'o': 'optative',
	'n': 'infinitive',
	'm': 'imperative',
	'p': 'participle'
}

voice = {
	'a': 'active',
	'p': 'passive',
	'm': 'middle',
	'e': 'medio-passive',
}

gender = {
	'm': 'masculine',
	'f': 'feminine',
	'n': 'neuter'
}

case = {
	'n': 'nominative',
	'g': 'genitive',
	'd': 'dative',
	'a': 'accusative',
	'v': 'vocative'
}

degree = {
	'c': 'comparative',
	's': 'superlative'
}

def XML_to_dataframe(path):

	f = open(path, "r")
	text = f.read()
	f.close()

	dico = parker.data(et.fromstring(text))

	frame = {
		'author': [],
		'title': [],
		'sentence': [], # s_n
		'verse': [], # t_p
		'token_position': [], # t_n
		'verse_occurence': [], # t_a
		'morphology': [], # t_o
		'position_in_sentence' : [], # t_u
		'word': [], # t => f
		'lemmata_1': [], # t => l => l1
		'lemmata_2': [], # t => l => l1
		'part_of_speech': [],
		'person': [],
		'number': [],
		'tense': [],
		'mood': [],
		'voice': [],
		'gender': [],
		'case': [],
		'degree': []
	} 

	for s in dico['s']:
		for t in s['t']:
			frame['word'].append(t['f'])
			
			if t['l'] == None:
				frame['lemmata_1'].append(np.nan)
				frame['lemmata_2'].append(np.nan)
				
			else:
				try:
					frame['lemmata_1'].append(t['l']['l1'])
				except:
					frame['lemmata_1'].append(np.nan)
				try:
					frame['lemmata_2'].append(t['l']['l2'])
				except:
					frame['lemmata_2'].append(np.nan)
				

	etree = et.parse(path)

	for text in etree.iter('text'):
		author = text.attrib['author']
		title = text.attrib['title']

		for s in text.iter('s'):
			sentence = s.attrib['n']

			for t in s.iter('t'):
				frame['sentence'].append(sentence)
				frame['verse'].append(str(t.attrib['p']) + '_')
				frame['token_position'].append(t.attrib['n'])
				frame['verse_occurence'].append(t.attrib['a'][1:-1])
				frame['morphology'].append(t.attrib['o'])
				frame['position_in_sentence'].append(t.attrib['u'])
				frame['author'].append(author)
				frame['title'].append(title)


	morpho_part = [part_of_speech, person, number, tense, mood, voice, gender, case, degree]
	morpho_name = ['part_of_speech', 'person', 'number', 'tense', 'mood',
				   'voice', 'gender', 'case', 'degree']

	for code in frame['morphology']:
	
		if (len(code) != 9):
			for i in range(len(morpho_part)):
				frame[morpho_name[i]].append(np.nan)
		else:
			for i in range(len(morpho_part)):
				if (code[i] == '-') or (code[i] == 'x'):
					frame[morpho_name[i]].append(np.nan)
				else:
					try:
						frame[morpho_name[i]].append(morpho_part[i][code[i]])
					except:
						frame[morpho_name[i]].append(np.nan)


	df = pd.DataFrame(frame)


	df['sentence'] = df['sentence'].astype('int')
	df['verse'] = df['verse'].astype('str')
	df['token_position'] = df['token_position'].astype('int')
	df['verse_occurence'] = df['verse_occurence'].astype('int')
	df['morphology'] = df['morphology'].astype('str')
	df['position_in_sentence'] = df['position_in_sentence'].astype('int')
	df['word'] = df['word'].astype('str')


	return df


def extract_morphology(serie):

	frame = {
		'part_of_speech': [],
		'person': [],
		'number': [],
		'tense': [],
		'mood': [],
		'voice': [],
		'gender': [],
		'case': [],
		'degree': []
	}

	morpho_part = [part_of_speech, person, number, tense, mood, voice, gender, case, degree]
	morpho_name = ['part_of_speech', 'person', 'number', 'tense', 'mood',
				   'voice', 'gender', 'case', 'degree']

	for ind, code in serie.iteritems():
	
		if (len(code) != 9):
			for i in range(len(morpho_part)):
				frame[morpho_name[i]].append(np.nan)
		else:
			for i in range(len(morpho_part)):
				if (code[i] == '-') or (code[i] == 'x'):
					frame[morpho_name[i]].append(np.nan)
				else:
					try:
						frame[morpho_name[i]].append(morpho_part[i][code[i]])
					except:
						frame[morpho_name[i]].append(np.nan)

	return frame



def codify_verse(df_, without = ['punctuation']):
	
	df = df_
	
	for condition in without:
		df = df[df['part_of_speech'] != condition]
	
	part_of_speech = { 'n': 'noun', 'v': 'verb', 'a': 'adjective', 'd': 'adverb',
				  'l': 'article', 'g': 'particle', 'c': 'conjunction',
				  'r': 'preposition', 'p': 'pronoun', 'm': 'numeral',
				  'i': 'interjection', 'u': 'punctuation' }
	
	code_pos = {v: k for k, v in part_of_speech.items()}
	
	verses = []

	for verse in df['verse'].value_counts().index:
		code = ''
	
		for ind, row in df[df['verse'] == verse].iterrows():
			try:
				code += code_pos[row['part_of_speech']]
			except:
				pass
	
		verses.append(code)
	
	df_output = pd.DataFrame({'verse': df['verse'].value_counts().index,
								'code': verses})
	
	return df_output



def stacked_plot_excel(df_list, df_names, feature):
    
    dico, key_element, cat = {}, {}, []
    
    morpho_part = [part_of_speech, person, number, tense, mood, voice, gender, case, degree]
    morpho_name = ['part_of_speech', 'person', 'number', 'tense', 'mood',
                    'voice', 'gender', 'case', 'degree']
    
    for i in range(len(morpho_name)):
        if feature == morpho_name[i]:
            invert = {v: k for k, v in morpho_part[i].items()}
            key_element = invert.keys()
    
    for key in key_element:
        cat.append(key)
    
    for name in df_names:
        dico[name] = []
        
    for i in range(len(df_list)):
        count = df_list[i][feature].value_counts()
        dico[df_names[i]] = count.values.tolist()
        
    dico['index'] = cat
    df = pd.DataFrame(dico)
    df.index = df['index']
    df = df[df_names]
    
    title = ''
    for name in df_names:
        title += name + '_'
        
    df.to_excel('xlsx/' + feature + '_' + title[:-1] + '.xlsx')
    
    return True








