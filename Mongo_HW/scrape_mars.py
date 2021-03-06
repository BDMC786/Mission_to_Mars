from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import pymongo

def scrape():
    mars_dict = {}
#News
    news_url = "https://mars.nasa.gov/news/"
    news_response = requests.get(news_url)
    news_soup = bs(news_response.text, 'html.parser')
    news_title = news_soup.find('div', class_ = "content_title").text
    news_body = news_soup.find('div', class_='rollover_description_inner').text

    mars_dict["news_title"] = news_title 
    mars_dict["news_body"] = news_body

#Images
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    image_response = requests.get(jpl_url)
    image_soup = bs(image_response.text, 'html.parser')
    image = image_soup.find('a', class_="button fancybox")
    url_end = image["data-fancybox-href"]
    image_url = 'https://www.jpl.nasa.gov' + url_end
    image_url = image_url.replace('medium', 'large')
    image_url = image_url.replace('ip', 'hires')
    mars_dict["featured_image"] = image_url

#Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(weather_url)
    weather_soup = bs(weather_response.text, 'html.parser')
    weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    weather = weather.split("Welcome",1)[0]     
    mars_dict["mars_weather"] = weather

#Facts
    facts_url = "https://space-facts.com/mars/"
    facts = pd.read_html(facts_url)
    mars_df = facts[0]
    mars_df.columns = ["Characteristic", "Description"]
    mars_df.set_index("Characteristic", inplace=True)
    mars_facts = mars_df.to_html()    
    mars_dict["mars_table"] = mars_facts

#Hemispheres
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    hemi_response = requests.get(astro_url)
    hemi_soup = bs(hemi_response.text, 'html.parser')
    hemi_image = hemi_soup.find_all('a', class_="itemLink product-item")

    hemi_images = []
    astro_url2 = 'https://astrogeology.usgs.gov'
    for image in hemi_image:
        hemi_dict = {}
        txt = image.text
        txt_Enh = txt.find("Enhance")
        title = txt[:txt_Enh]
        hemi_dict["title"] = title        
        hemi_images.append(hemi_dict)
        hemi_url = astro_url2 + image["href"]
        hemi_response = requests.get(hemi_url)
        hemi_soup = bs(hemi_response.text, 'html.parser')
        h_images = hemi_soup.find_all('img', class_="wide-image")
        for image in h_images:
            src = image["src"]
        hemi_dict["img_url"] = astro_url2 + src
    mars_dict["hemisphere_imgs"] = hemi_images


#--------------------------------------------------------------
    return mars_dict