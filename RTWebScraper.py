from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pprint

client = MongoClient()
rotten_tomatoes_db=client['rotten_tomatoes']
rating = rotten_tomatoes_db['ratings']

url = 

r = requests.get(url)

whole_page= rotten_tomatoes_db['whole_page']
whole_page.insert_one({'html': r.content, 'url':url, 'time_scraped':time.time()})

soup = BeautifulSoup(r.text, 'html.parser')

movie = soup.find('h1', class_="mop-ratings-wrap__title mop-ratings-wrap__title--top").text
tomatometer = soup.find('span', class_="mop-ratings-wrap__percentage").text
audience
ratings.insert_one({'movie':movie, 'tomatometer':tomatometer, 'audience':audience})