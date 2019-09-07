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
    n_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

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
    facts_url = 'https://space-facts.com/mars/
    facts_df = pd.read_html('https://space-facts.com/mars/')
    facts_df_html = facts_df.to_html(header=False, index=False)

    #Hemispheres Images
    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(h_url)
    urls = [(a.text, a['href']) for a in browser.find_by_css('div[class="description"] a')]

    h_urls_dict = []

    for title, url in urls:
        h_dict = {}
        h_dict['title'] = title
        browser.visit(url)
        img_url = browser.find_by_css('img[class="wide-image"]')['src']
        h_dict['img_url'] = img_url
        h_urls_dict.append(h_dict)

    mars_data ={
		'news_title' : news_title,
		'summary': news_p,
		'featured_image': featured_image_url,
		'featured_image_title': featured_image_title,
		'weather': tweets,
		'fact_table': fact_df_html,
		'hemisphere_image_urls': h_image_urls,
        'news_url': n_url,
        'jpl_url': pic_url,
        'weather_url': weather_url,
        'fact_url': facts_url,
        'hemisphere_url': h_url,
        }

	collection.insert(mars_data)