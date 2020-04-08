from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pprint
import time
import json
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import re

client = MongoClient()
rotten_tomatoes_db=client['rotten_tomatoes']
rating = rotten_tomatoes_db['ratings']

url_main_page = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'

def get_urls(x):
    driver = webdriver.Chrome(executable_path='./src/chromedriver')
    driver.get(x)
    time.sleep(15)
    show_more_button = driver.find_element_by_class_name("btn.btn-secondary-rt.mb-load-btn")
    
    while(True):
           
        try:
            show_more_button.click()
            time.sleep(2)
            
        except ElementNotVisibleException:
            break
        except TimeoutException:
            break
        except StaleElementReferenceException:
            break
        
        
    #record each movie title and its url inside dict
    soup = BeautifulSoup(driver.page_source,"lxml")
    links=[]
    for link in soup.findAll('a', attrs={'href': re.compile("/m/")}):
        links.append(link.get('href'))
    links2=[]
    for link in links:
        if link not in links2:
            links2.append(link)
    #movies = soup.find_all('h3', {'class' :"movieTitle"})
    #movies= [movie.text for movie in movies]
    return links2
    driver.quit()

def get_full_urls(x):
    full_urls = []
    first_half = 'http://www.rottentomatoes.com'
    for url in x:
        full_urls.append(first_half+url)
    return full_urls
   


def get_info_from_urls(x):
    p=0
    for url in x:
        
        r = requests.get(url)
        if r.status_code ==200:
            soup = BeautifulSoup(r.text, 'html.parser')

            movie = soup.find('h1', class_="mop-ratings-wrap__title mop-ratings-wrap__title--top").text
            rating_tags = soup.find_all('span', class_="mop-ratings-wrap__percentage")
            if len(rating_tags)==2:
                tomatometer,audience = [i for i in rating_tags]
                tomatometer = tomatometer.text.strip('\n').strip().strip('%')
                audience = audience.text.strip('\n').strip().strip('%')
                date = soup.find('time').text
                rating.insert_one({'movie':movie, 'tomatometer':tomatometer, 'audience':audience, 'date':date})
                p+=1
                print(f"Added {movie} to Database ({(p/len(x))*100}% done.)")
            
            else: 
                continue
        else:
            continue

        time.sleep(10)

if __name__ == '__main__':
	#run scraper and print completion time
	print('Running')
	start = time.time()
	end = time.time() - start
	print("Completed, time: " + str(end) + " secs")
