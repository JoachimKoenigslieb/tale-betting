#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:13:11 2020

@author: joachim
"""


import pickle
import matplotlib.pyplot as plt
import numpy as np
import math

def poisson(k, lamb):
	return math.exp(-lamb) * lamb**k / math.factorial(k)

def CDF_poisson(k, lamb):
	return sum([poisson(i, lamb) for i in range(k+1)])

def cumsum(y):
	s = [y[0]]
	for i in range(1, len(y)):
		s.append(s[-1] + y[i])
	return np.array(s)

with open('texts', 'rb') as file:
	texts = pickle.load(file)
	
odds_info = [
	{
		'word': 'danmark',
		'over/under': (1.95, 1.75, ),
		'threshold': 7.5,
	},
	{
		'word': 'danske',
		'over/under': (1.80, 1.90, ),
		'threshold': 4.5,
	},
	{
		'word': 'tak',
		'over/under': (1.70, 2.02, ),
		'threshold': 3.5,
	},
	{
		'word': 'grønland',
		'over/under': (1.62, 2.15, ),
		'threshold': 2.5,
	},
	{
		'word': 'færøerne',
		'over/under': (2.2, 1.6, ),
		'threshold': 2.5,
	},
	{
		'word': 'nytår',
		'over/under': (1.95, 1.75, ),
		'threshold': 2.5,
	},
	{
		'word': 'samfund',
		'over/under': (1.85, 1.85, ),
		'threshold': 2.5,
	},
	{
		'word': 'verden',
		'over/under': (1.60, 2.2, ),
		'threshold': 2.5,
	},
	{
		'word': 'nytårsønsker',
		'over/under': (2.2, 1.6, ),
		'threshold': 2.5,
	},
	{
		'word': 'varmeste',
		'over/under': (1.48, 2.45, ),
		'threshold': 1.5,
	},
]

over_under_words = [odds['word'] for odds in odds_info]
over_under_line = [odds['threshold'] for odds in odds_info]
over_under_odds = [odds['over/under'] for odds in odds_info]

over_under_count = {word: [] for word in over_under_words}
asigned_over_probs = []
kellys = []

punctuation = [',', '.', ':', '!', ';']

for text_ind, text in enumerate(texts):
	year = 1972 + text_ind 

	print('parsing year...', year)

	words = text.split(' ')
	
	for word in over_under_words:
		over_under_count[word].append(words.count(word))

for word in over_under_words: 
	over_under_count[word] = np.array(over_under_count[word])

plot_x = 5
plot_y = 2

f, a = plt.subplots(plot_x, plot_y, figsize=(10, 7))
f1, a1 = plt.subplots(plot_x, plot_y, figsize=(10, 7))

for i in range(plot_y):
	for j in range(plot_x):
		word = over_under_words[i*plot_x + j]
		count = np.array(over_under_count[word])[:]

		lamb = count.mean() #max-likelyhood estimator for lambda in poission distriubution is just the mean!
		p = 1 - CDF_poisson(int(over_under_line[i*plot_x + j]), lamb) #tail of distribution
		asigned_over_probs.append(p)

		under_odds = over_under_odds[i*plot_x + j][0] 
		b = under_odds - 1
		
		kelly = (b * (1-p) + (1-p) - 1)/b
		kellys.append(kelly)
		
		a[j, i].plot(count, 'o')
		yticks = range(0, count.max()+1) if count.max() < 6 else range(0, count.max()+2, 2)
		a[j, i].set_yticks(yticks)
		a[j, i].plot([0, len(count)], [over_under_line[i*plot_x + j]] * 2, 'red')
		a[j, i].set_title(f'"{word}"')
		a[j, i].set_xlabel('Years (after 1972)')

		labels, counts = np.unique(count, return_counts=True)
		poisson_fit = [poisson(i, lamb) for i in range(len(labels) + 1)]

		a1[j, i].set_title(f'{word}')
		a1[j, i].bar(labels, counts/counts.sum(), align='center')
		a1[j, i].set_xticks(labels)
		a1[j, i].plot(range(len(labels)+1), poisson_fit, 'r--')

money = 1000
kellys = np.array(kellys)

distribute_odds = kellys/kellys.sum() * money

payout = distribute_odds * [odds[0] for odds in over_under_odds] 

for i in range(plot_y):
	for j in range(plot_x):
		word = over_under_words[i*plot_x + j]
		suggested_bet = distribute_odds[i*plot_x + j]
		over_prop = asigned_over_probs[i * plot_x + j] * 100
		under_props = 100 - over_prop

		a1[j, i].set_title(f'"{word}"\nAssigned over/under : {over_prop:0.1f}%/{under_props:0.1f}%. Kelly: {kellys[i*plot_x + j]:0.2f}')
   
f.tight_layout()
f1.tight_layout()

f.savefig('fig1.png')
f1.savefig('fig2.png')

for odd, word in zip(distribute_odds, over_under_words):
	print(word, int(odd))