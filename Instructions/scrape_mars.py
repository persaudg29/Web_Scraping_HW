#dependencies
from splinter import Browser
import requests
import pandas as pd
import datetime
import time
from bs4 import BeautifulSoup
from pprint import pprint
import pymongo


#executable path for chromedriver
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_mars():
    #start off with an empty dictionary
    scraped_results_dict = dict()
    
    
    url = 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')
    
    imageurl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(imageurl)
    fullimage = browser.find_by_id("full_image")
    fullimage.click()
    
    try:
        result_title = soup1.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
        news_body = soup1.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
        print("The news title is " + result_title)
        print("The news body is " + news_body)
        
        except  AttributeError as Atterror:
        print(Atterror)

        scraped_results_dict["Mars_news_title"] = result_title
        scraped_results_dict["Mars_news_body"] = news_body
        pprint(scraped_results_dict)
            

        time.sleep(5)
        link_more_info = browser.find_link_by_partial_text('more info')
        link_more_info.click()
        
        fullimg_html2 = browser.html
        soup2 = BeautifulSoup(fullimg_html2, "html.parser")
        fullimg_href = soup2.find('figure', class_='lede').a['href']
        featured_image_url = "https://www.jpl.nasa.gov" + fullimg_href
        print(featured_image_url)

        scraped_results_dict["Mars_featured_image_url"] = featured_image_url
        pprint(scraped_results_dict)
        

        url3 = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url3)
        html3 = browser.html
        soup3 = BeautifulSoup(html3, 'html.parser')        

        mars_weather = soup3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        mars_weather
        scraped_results_dict["Mars_tweet_weather"] = mars_weather
    pprint(scraped_results_dict)

        
        url4 = "http://space-facts.com/mars/"
        df_marsfacts_all = pd.read_html(url4)
        df_marsfacts = df_marsfacts_all[0]
        df_marsfacts.columns = ['Mars_Facts', 'Values']  
        df_marsfacts.to_html("mars_facts.html", index=False)
       
        df_marsfacts.set_index("Mars_Facts")
 
        mars_facts_html = df_marsfacts.to_html(classes="mars_facts table table-striped")
        scraped_results_dict["Mars_facts_table"] = mars_facts_html
        pprint(scraped_results_dict)
        
        
        url5 =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(url5)
    time.sleep(10)
    html5 = browser.html
    soup5 = BeautifulSoup(html5, "html.parser")
    
    class_collap_results = soup5.find('div', class_="collapsible results")
    hemis_items = class_collap_results.find_all('div',class_='item')
    hemis_img_urls_list=list()
    img_urls_list = list()
    title_list = list()
    for h in hemis_items:
        #save title
        h_title = h.h3.text
        title_list.append(h_title)
        
        h_href  = "https://astrogeology.usgs.gov" + h.find('a',class_='itemLink product-item')['href']
        
        browser.visit(h_href)
        time.sleep(5) 
        html5   = browser.html
        soup_img = BeautifulSoup(html5, 'html.parser')
        h_img_url = soup_img.find('div', class_='downloads').find('li').a['href']
        img_urls_list.append(h_img_url)
        hemispheres_dict = dict()
        hemispheres_dict['title'] = h_title
        hemispheres_dict['img_url'] = h_img_url
        hemis_img_urls_list.append(hemispheres_dict)

    print(hemis_img_urls_list)
    print(title_list)
    print(img_urls_list)

    scraped_results_dict["Hemisphere_image_urls"] = hemis_img_urls_list
    pprint(scraped_results_dict)
    
    cur_datetime = datetime.datetime.utcnow()
    scraped_results_dict["Date_time"] = cur_datetime
    pprint(scraped_results_dict)
    
    print("just before final return of mars_info_dict")
    mars_return_dict =  {
        "News_Title": scraped_results_dict["Mars_news_title"],
        "News_Summary" :scraped_results_dict["Mars_news_body"],
        "Featured_Image" : scraped_results_dict["Mars_featured_image_url"],
        "Weather_Tweet" : scraped_results_dict["Mars_tweet_weather"],
        "Facts" : mars_facts_html,
        "Hemisphere_Image_urls": hemis_img_urls_list,
        "Date" : scraped_results_dict["Date_time"],
    }
    return mars_return_dict
    
    

        
        
        
        
        
        
        
        
        
        
        
        

                
    
    
    
    