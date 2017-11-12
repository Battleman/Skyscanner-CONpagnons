#ONLY NEED TO USE THE LAST FUNCTION FOR NOW

import requests
import json

from clarifai.rest import ClarifaiApp

from bs4 import BeautifulSoup
import requests
from pandas import Series,DataFrame

from collections import Counter

import pickle

import re

app = ClarifaiApp()
model = app.models.get('general-v1.3')


def count_words_wikipedia(name, words):
    startURL = 'https://en.wikipedia.org/wiki/'
    result = requests.get(startURL + name)

    c = result.content

    soup = BeautifulSoup(c, "lxml")

    city_name = soup.find(id='firstHeading').text
    text = soup.find(id='bodyContent').text

    regx = r'\b' + '|'.join(words) + r'\b'
    occ = re.findall(regx, text, re.IGNORECASE)
    occ_len = len(occ)
    article_len = len(text)
    score = float(occ_len) / float(article_len)

    return score



def find_best_words(image):
    response = model.predict_by_url(url=image)

    concepts = response['outputs'][0]['data']['concepts']
    return list(map(lambda c: c['name'], concepts))[:10]


def get_city_score(city, words):
    score = count_words_wikipedia(city, words)
    return score

def get_most_likely_cities(image, cities):
    words = find_best_words(image)
    cities_score = []
    for city in cities:
        cities_score.append((city, get_city_score(city, words)))
    return cities_score

def select_best_cities_from_image(image, citiess, number):
    words = find_best_words(image)
    print(words)
    cities_score = []
    for city in citiess:
        cities_score.append((city, get_city_score(city, words)))
    return sorted(cities_score, key=lambda tup: tup[1], reverse=True)
    #return list(map(lambda x: x[0], cities_score))[:number]


def select_best_cities_fixed(image, number):
    cities = ['Paris', 'Rome', 'Tokyo', 'London', 'Beijing', 'Seoul', 'New York', 'Cairo', 'Bergamo', 'Rio de Janeiro']
    return select_best_cities_from_image(image, cities, number)


country = 'CH'
currency = 'CHF'
locale = 'en_GB'
json_data = requests.get('http://partners.api.skyscanner.net/apiservices/geo/v1.0?apiKey=ha712564909427747796218296388326')

parsed = json.loads(json_data.text)

cont = parsed['Continents']

city_dict = {}
for continent in cont:
    for countries in continent['Countries']:
        country = countries['Name']
        for cities in countries['Cities']:
            city = cities['Name']
            airport_list = []
            for airport in cities['Airports']:
                airport_list.append(airport['Id'])
                #print(city + ', ' + country +':    ' + airports['Name'] +' '+ airports['Id'])
            city_dict[city] = airport_list

print(city_dict["Paris"])

capitals = requests.get('https://en.wikipedia.org/wiki/List_of_national_capitals_in_alphabetical_order')

soup = BeautifulSoup(capitals.content, "lxml")

table_cap = soup.find('table', {"class" : "wikitable sortable"})


capitals = []
for row in table_cap.find_all('tr'):
    cols = row.find_all('td')

    if len(cols) == 3:
        capital = cols[0].text.strip()
        #capital = regex.findall(r'[\W]+', capital)[0]
        #capital = regex.findall(r'?!a', capital)
        capitals.append((capital, cols[1].text.strip()))


def save_word_list(cities):
    ret = {}
    for city in cities:
        startURL = 'https://en.wikipedia.org/wiki/'
        result = requests.get(startURL + city)
        if result.status_code == 200:


            c = result.content

            soup = BeautifulSoup(c, "lxml")
            text = soup.find(id='bodyContent').text
            ret[city] = text.split()
            print(city)
    return ret

# ------ DUMPS CAPITAL WIKIPEDIA ARTICLES< TAKES A WHILE -------
#capitals_name = map(lambda x: x[0], capitals)
#pickle.dump(save_word_list(capitals_name), open("test.bin", "wb+"))


def get_most_likely_cities_file(image, file, num):
    ret = []
    words_list = pickle.load(open(file, 'rb'))
    words = find_best_words(image)
    for city in words_list:
        total = 0

        count = Counter(words_list[city])
        for word in words:
            total+=count[word]
        score = float(total) / float(len(words_list[city]))
        ret.append((city, score))
    return sorted(ret, key=lambda tup: tup[1], reverse=True)[:num]



beach = 'https://media-cdn.tripadvisor.com/media/photo-s/0e/85/48/e6/seven-mile-beach-grand.jpg'
counts = get_most_likely_cities_file(beach, 'capitals_wikipedia.bin')




if __name__ == '__main__':

    response = model.predict_by_url(url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Tokyo_Tower_and_around_Skyscrapers.jpg/238px-Tokyo_Tower_and_around_Skyscrapers.jpg')


    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])

    url = "https://en.wikipedia.org/wiki/Bergamo"

    country = 'CH'
    currency = 'CHF'
    locale = 'en_GB'
    json_data = requests.get('http://partners.api.skyscanner.net/apiservices/geo/v1.0?apiKey=ha712564909427747796218296388326')

    parsed = json.loads(json_data.text)

    city_dict = {}
    for continent in cont:
        for countries in continent['Countries']:
            country = countries['Name']
            for cities in countries['Cities']:
                city = cities['Name']
                airport_list = []
                for airport in cities['Airports']:
                    airport_list.append(airport['Id'])
                    #print(city + ', ' + country +':    ' + airports['Name'] +' '+ airports['Id'])
                city_dict[city] = airport_list

    print(city_dict["Paris"])

    capitals = requests.get('https://en.wikipedia.org/wiki/List_of_national_capitals_in_alphabetical_order')

    soup = BeautifulSoup(capitals.content, "lxml")

    count_words_wikipedia("https://en.wikipedia.org/wiki/Bergamo", ['was', 'bergamo'])

    #cities = ['Paris', 'Rome', 'Tokyo', 'London', 'Beijing', 'Seoul', 'New York', 'Cairo', 'Bergamo']

    image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Tokyo_Tower_and_around_Skyscrapers.jpg/238px-Tokyo_Tower_and_around_Skyscrapers.jpg'
    words = find_best_words(image)
