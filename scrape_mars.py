from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import pandas as pd
from flask import Flask, render_template
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

# Scrape Data 

executable_path = {'executable_path': 'chromedriver.exe'}

def scrape():

    collection.drop()

    #NASA Article
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    #JPL Image
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(pic_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.find_link_by_text('800 x 600').first
    featured_image_url = browser.url


    #Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    wbrow = browser.html
    w_soup = BeautifulSoup(wbrow, 'lxml')
    tweets = w_soup.find("div", class_="js-tweet-text-container").text.strip()

    #Facts Table

    facts_df = pd.read_html('https://space-facts.com/mars/')

    #Hemispheres Images
    hemis = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    urls = []

    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(h_url)
    for i in hemis:
        browser.click_link_by_partial_text(i)
        time.sleep(2)
        browser.click_link_by_partial_text('Sample')
        time.sleep(2)
        urls.append(browser.url)

    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    h_response = requests.get(h_url)
    h_soup = BeautifulSoup(h_response.text, 'lxml')
    soup_list = h_soup.find_all('h3')
    names = []
    for i in soup_list:
        names.append(i.text) 

    h_names = [i.rsplit(' ', 1)[0] for i in names]

    hemi_dict = dict(zip(h_names,urls))

