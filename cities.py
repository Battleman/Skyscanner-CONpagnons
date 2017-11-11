#ONLY NEED TO USE THE LAST FUNCTION FOR NOW

import requests
import json

from clarifai.rest import ClarifaiApp

from bs4 import BeautifulSoup
import requests
from pandas import Series,DataFrame

from collections import Counter

import regex

app = ClarifaiApp()
model = app.models.get('general-v1.3')


def find_best_words(image):
    response = model.predict_by_url(url=image)


    concepts = response['outputs'][0]['data']['concepts']
    ret = []
    for concept in concepts[-13:-3]:
        ret.append(concept['name'])
    return ret

def count_words_wikipedia(name, words):
    startURL = 'https://en.wikipedia.org/wiki/'
    result = requests.get(startURL + name)

    c = result.content

    soup = BeautifulSoup(c, "lxml")

    city_name = soup.find(id='firstHeading').text
    text = soup.find(id='bodyContent').text

    regx = r'\b' + '|'.join(words) + r'\b'
    occ = regex.findall(regx, text, regex.IGNORECASE)
    occ_len = len(occ)
    article_len = len(text)
    score = float(occ_len) / float(article_len)

    return score


def get_city_score(city, words):
    score = count_words_wikipedia(city, words)
    return score


def select_best_cities_from_image(image, cities, number):
    words = find_best_words(image)
    cities_score = []
    for city in cities:
        cities_score.append((city, get_city_score(city, words)))
    cities_score = sorted(cities_score, key=lambda tup: tup[1], reverse=True)
    return list(map(lambda x: x[0], cities_score)[:number]

# -------------------------------------- USE THIS -----------------------------------------------
def select_best_cities_fixed(image, number):
    cities = ['Paris', 'Rome', 'Tokyo', 'London', 'Beijing', 'Seoul', 'New York', 'Cairo', 'Bergamo']
    return select_best_cities_from_image(image, cities, number)
