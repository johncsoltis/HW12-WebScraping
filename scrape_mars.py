from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def scrape_news():
    
    n_url = 'https://mars.nasa.gov/news/'
    response = requests.get(n_url)
    soup = bs(response.text, 'lxml')

    n_heads = soup.find_all('div', class_ = 'content_title')
    n_text = soup.find_all('div', class_ = 'article_teaser_body')

    headlines = []
    for h in n_heads:
        h = h.text.strip()
        headlines.append(h)

    headlines = headlines[0]   
    
    
    return headlines
    
def scrape_weather():
    
    w_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(w_url)
    
    soup = bs(response.text, 'lxml')
    weather = soup.find_all('p')
    tweet = weather[4].text.strip()
    
    return tweet
    
def scrape_featured_image():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    
    html = browser.html
    soup = bs(html, 'lxml')
    image = soup.find_all('a', class_ = 'button')
    image_url = "https://www.jpl.nasa.gov" + (image[0]['data-link'])
    
    #large image:
    browser.visit(image_url)
    html = browser.html
    
    #assign to var
    soup = bs(html, 'lxml')
    links = soup.find_all('div', class_ = 'download_tiff')
    link = links[1].a['href']
    image_link = "https:" + link
    
    return image_link
    
def scrape_facts():

    facts_df = pd.read_html('https://space-facts.com/mars/')
    facts_df = facts_df[1]

    mars_facts = facts_df.to_html(header=False, index=False)
    
    return mars_facts
    
def scrape_hemispheres():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles']
    #temp lits
    h_names = []
    h_urls = []

    #loop to get all urls/titles
    for hemisphere in hemispheres:
        browser.visit(url)
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = bs(html, 'lxml')
        tempname = soup.find_all('h2', class_ = 'title')
        tempurl = soup.find_all('li')
        h_urls.append(tempurl[0].a['href'])
        h_names.append(tempname[0].text)
        
    return h_urls, h_names

def scrape_all():
    news = scrape_news()
    weather = scrape_weather()
    feat_image = scrape_featured_image()
    facts = scrape_facts()
    hemispheres = scrape_hemispheres()
    
   
    mars_data = {"news" : news, 
                       "weather" : weather,
                       "featured_image" : feat_image,
                       "fact_table" : facts,
                       "hemispheres" : hemispheres}
    
    return mars_data
    