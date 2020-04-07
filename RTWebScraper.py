from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pprint

client = MongoClient()
rotten_tomatoes_db=client['rotten_tomatoes']
rating = rotten_tomatoes_db['ratings']

url_main = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'
urls=[]

def get_urls(url_main):

    q = requests.get(url_main)
 
    soup = BeautifulSoup(r.text,'html.parser')

    link = soup.find()
    for tag in link:
        urls.append(tag.text)
    


def get_info_from_urls(urls)
    for url in urls:

        r = requests.get(url)

        whole_page= rotten_tomatoes_db['whole_page']
        whole_page.insert_one({'html': r.content, 'url':url, 'time_scraped':time.time()})

        soup = BeautifulSoup(r.text, 'html.parser')

        movie = soup.find('h1', class_="mop-ratings-wrap__title mop-ratings-wrap__title--top").text
        tomatometer,audience = [i for i in soup.find_all('span', class_="mop-ratings-wrap__percentage")]
        tomatometer = tomatometer.strip('\n').strip().strip('%')
        audience = audience.strip('\n').strip().strip('%')
        date = soup.find('time').text
        ratings.insert_one({'movie':movie, 'tomatometer':tomatometer, 'audience':audience, 'date':date})

        time(5)

if __name__ == '__main__':
	#run scraper and print completion time
	print('Running')
	start = time.time()
	end = time.time() - start
	print("Completed, time: " + str(end) + " secs")
