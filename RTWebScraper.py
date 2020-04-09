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
urls = rotten_tomatoes_db['urls']

main_urls = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'

def get_urls(x):
    links=[]
    links2=[]
    first_half = 'http://www.rottentomatoes.com'
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
        
        
    soup = BeautifulSoup(driver.page_source,"lxml")
    for link in soup.findAll('a', attrs={'href': re.compile("/m/")}):
        links.append(link.get('href'))
    for link in links:
        if (first_half+link) not in links2:
            links2.append(first_half+link)
            urls.insert_one({'link': first_half+link})
    driver.quit()
    print("Done Getting Links!")
   


def get_info_from_urls(x):
    p=0
    p2=0
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
                p2+=1
                print(f"Added '{movie}' to Database. {p2} movies have been added ({(p/len(x))*100}% done.).")
            
            else: 
                continue
        else:
            print("Failed to get page")
            p+=1
            continue

        time.sleep(10)

get_urls(main_urls)

num_scraped = urls.count_documents({})

websites = [urls.find()[i]['link'] for i in range(num_scraped)]


get_info_from_urls(websites)



print('FINISHED SCRAPING!!!!!!')
