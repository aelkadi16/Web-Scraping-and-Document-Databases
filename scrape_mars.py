

# Dependencies
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pymongo
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the latest Mars news.
    
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    
    # Add the news title and summary to the dictionary
    
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph


    # ## JPL Mars Space Images - Featured Image
    # ------
    # - Visit the url for JPL's Featured Space [Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # - Use splinter to navigate the site and find the full size jpg image url for the current Featured Mars Image.
    # - Save a complete url string for this image


    # While chromedriver is open go to JPL's Featured Space Image page. 
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
  
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA23202-640x350.jpg"
    
    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url


    # ## Mars Weather 
    # ------
    # - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the latest Mars weather tweet from the page.
    # - Save the tweet text for the weather report.
    # Setup Tweepy API Authentication
 
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html = browser.html
    soup = bs(html, 'lxml')
    mars_weather = soup.find('p', class_='TweetTextSize').text
    

    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather

    ### Mars Facts

    url4 = "https://space-facts.com/mars/"
    table = pd.read_html(url4)
    table[0]
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])
    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    
    
    # Add the Mars facts table to the dictionary
    mars_data["mars_html_table"] = mars_html_table


    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemispheres=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemispheres.append(dictionary)
        browser.back()

        mars_data['mars_hemispheres'] = mars_hemispheres
    # Return the dictionary
        return mars_data

