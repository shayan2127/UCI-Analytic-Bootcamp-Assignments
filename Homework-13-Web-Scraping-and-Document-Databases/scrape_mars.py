
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # NASA Mars News #

    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    time.sleep(2)
    
    html = browser.html
    soup = bs(html,"html.parser")


    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p 
    
	# JPL Mars Space Images - Featured Image #

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(2)

    results = browser.find_by_xpath("//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img")
    img = results[0]
    img.click()
    time.sleep(2)
    
    html = browser.html
    soup = bs(html, "html.parser")

    src = soup.find("img", class_="fancybox-image")["src"]
    final_image_url = "https://jpl.nasa.gov"+src
    mars_data["featured_url"] = final_image_url
    
    # Mars Weather #

    w_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(w_url)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather

    # Mars Facts #

    facts_url = "https://space-facts.com/mars/"
    time.sleep(2)
    df = pd.read_html(facts_url)
    df = df[0]

    df.columns = ["Data", "Values"]
    df = df.set_index(["Data"])

    mars_facts_html = df.to_html()
    mars_facts_html = mars_facts_html.replace("\n", "")
    mars_data["mars_facts_html"] = mars_facts_html

    # Mars Hemisperes #

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    hemisphere_results = []
    hemisphere = {}
    
    for i in range (4):
        time.sleep(5)
        imgs = browser.find_by_tag('h3')
        imgs[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find("img", class_="wide-image")["src"]
        hemisphere_title = soup.find("h2",class_="title").text
        hemisphere_final_url='https://astrogeology.usgs.gov/'+img_url
        hemisphere = {"hemisphere_title":hemisphere_title, "hemisphere_url": hemisphere_final_url}
        hemisphere_results.append(hemisphere)
        browser.back()
    print(hemisphere_results)
    
    mars_data["hemisphere_results"] = hemisphere_results

    return mars_data