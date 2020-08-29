#imports and dependacies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict ={}

    #Url info
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(10)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    #Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[1].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    #Mars Image to be scraped url info
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')
    #Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path

    #Mars facts to be scraped
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]
    #create HTML Table
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')
    
    #Mars hemisphere name and image info
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    #Mars hemispheres data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []
    
    for hemi in mars_hemispheres:
        #get title of pic
        hemisphere = hemi.find('div', class_="description")
        title = hemisphere.h3.text        
        #Get link for pic
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        #Create Mar Dict and store info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)

    #Assemble the dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict