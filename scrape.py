#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:36:54 2020

@author: joachim
"""


import requests
from bs4 import BeautifulSoup as bs
import time
import pickle 

texts = []
for year in range(1972, 2022):
	if year == 1976:
		url = f'https://dansketaler.dk/tale/h-m-dronning-margrethe-iis-nytaarstale-1976/print/'
	elif year == 2012:
		url = f'https://dansketaler.dk/tale/dronningens-nytarstale-2012/print'
	elif year == 2016:
		url = 'https://dansketaler.dk/tale/dronningens-nytaartale-2016/print'
	elif year == 2017:
		url = 'https://dansketaler.dk/tale/h-m-dronningens-nytaarstale-2017/print'
	elif year == 2018:
		url = 'https://dansketaler.dk/tale/hendes-majestaet-dronningens-nytaarstale-2018/print'
	elif year == 2019:
		url = 'https://dansketaler.dk/tale/h-m-dronning-margrethe-iis-nytaarstale-2019/print'
	elif year == 1979:
		url = f'https://dansketaler.dk/tale/christian-9-palae-amalienborg/print'
	elif year == 2020:
		url = 'https://dansketaler.dk/tale/h-m-dronning-margrethe-iis-nytaarstale-2020/print'
	elif year == 2021:
		url = 'https://dansketaler.dk/tale/h-m-dronning-margrethe-iis-nytaarstale-2021-2/print'
	else:
		url = f'https://dansketaler.dk/tale/dronningens-nytaarstale-{year}/print/'

	print(f'downlading {year}...')
	r = requests.get(url)
	# time.sleep(0.5)
	soup = bs(r.text)
	text = soup.find('div', class_='entry-content').text
	texts.append(text)

	with open(f'./taler/{year}.txt', 'w') as file:
		file.write(text)

texts = [text.replace('\n', ' ').strip().lower() for text in texts]

with open('texts', 'wb') as file:
	pickle.dump(texts, file)