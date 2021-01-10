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
    
all_words = {}

over_under_words = ['danmark', 'danske', 'verden', 'tak', 'nytår', 'familie', 'samfund', 'grønland', 'færøerne']
over_under_count = {word: [] for word in over_under_words}
over_under_line = [6.5, 4.5, 4.5, 4.5,  3.5, 3.5, 3.5, 2.5, 2.5]
over_under_odds = [(1.6, 2.2), (1.72, 2), (1.6, 2.2), (1.85, 1.85), (1.75, 1.95), (1.65, 2.1), (2.2, 1.6), (1.85, 1.85), (2.3, 1.55)]
over_under_assigned_prob = []
kellys = []

punctuation = [',', '.', ':', '!', ';']

for text in texts:
    words = text.split(' ')
    
    for word in words:
        for symbol in punctuation:
            word = word.replace(symbol, '')
        if word in all_words:
            all_words[word] += 1
        else:
            all_words[word] = 1
    for word in over_under_words:
        over_under_count[word].append(words.count(word))

for word in over_under_words: 
    over_under_count[word] = np.array(over_under_count[word])

f, a = plt.subplots(3,3, figsize=(10, 7))
f1, a1 = plt.subplots(3, 3, figsize=(10, 7))

for i in range(3):
    for j in range(3):
        word = over_under_words[i*3 + j]
        count = np.array(over_under_count[word])[:]

        lamb = count.mean() #max-likelyhood estimator for lambda in poission distriubution is just the mean!
        p = 1 - CDF_poisson(int(over_under_line[i*3 + j]), lamb) #tail of distribution
        over_under_assigned_prob.append(p)

        under_odds = over_under_odds[i*3 + j][0] 
        b = under_odds - 1
        
        kelly = (b * (1-p) + (1-p) - 1)/b
        kellys.append(kelly)
        
        a[i, j].plot(count, 'o')
        yticks = range(0, count.max()+1) if count.max() < 6 else range(0, count.max()+2, 2)
        a[i, j].set_yticks(yticks)
        a[i, j].plot([0, len(count)], [over_under_line[i*3 + j]] * 2, 'red')
        a[i, j].set_title(f'{word}. assigned proba: {100 * p:0.3f}%')

        labels, counts = np.unique(count, return_counts=True)
        poisson_fit = [poisson(i, lamb) for i in range(len(labels) + 1)]

        a1[i, j].set_title(f'{word}')
        a1[i, j].bar(labels, counts/counts.sum(), align='center')
        a1[i, j].set_xticks(labels)
        a1[i, j].plot(range(len(labels)+1), poisson_fit, 'r--')

money = 1000
kellys = np.array(kellys)

distribute_odds = kellys/kellys.sum() * money

payout = distribute_odds * [odds[0] for odds in over_under_odds] 

for i in range(3):
    for j in range(3):
        word = over_under_words[i*3 + j]
        suggested_bet = distribute_odds[i*3 + j]
        a1[i, j].set_title(f'{word}. suggested bet:  {suggested_bet/money*100:0.3f}%')
   
f.tight_layout()
f1.tight_layout()

f.savefig('fig1.png')
f1.savefig('fig2.png')

for odd, word in zip(distribute_odds, over_under_words):
    print(word, int(odd))