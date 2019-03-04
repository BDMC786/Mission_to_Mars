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
    news_paragraph = news_soup.find('div', class_='rollover_description_inner').text

    mars_dict["news_title"] = news_title 
    mars_dict["news_paragraph"] = news_paragraph

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

    # Mars Weather
    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.
#Weather
    # Collects most recent tweet from Mars weather twitter account
    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(weather_url)
    weather_soup = bs(weather_response.text, 'html.parser')
    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather = mars_weather.split("Welcome",1)[0] 
    
    mars_dict["mars_weather"] = mars_weather

#Mars Facts
    facts_url = "https://space-facts.com/mars/"
    mars_info = pd.read_html(facts_url)
    mars_df = mars_info[0]
    mars_df.columns = ["Characteristic", "Description"]
    mars_df.set_index("Characteristic", inplace=True)
    mars_facts = mars_df.to_html()
    
    mars_dict["mars_table"] = mars_facts

# Mars Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    hemi_response = requests.get(hemi_url)
    hemi_soup = bs(hemi_response.text, 'html.parser')

    hem_image = hemi_soup.find_all('a', class_="itemLink product-item")

    hem_images = []
    hem_piece = 'https://astrogeology.usgs.gov'
    for image in hem_image:
        hem_dict = {}
        string = image.text
        remove = string.find("Enhance")
        title = string[:remove]
        hem_dict["title"] = title
        
        hem_images.append(hem_dict)
        hem_url = hem_piece + image["href"]
        picresponse = requests.get(hem_url)
        img_soup = bs(picresponse.text, 'html.parser')
        pictures = img_soup.find_all('img', class_="wide-image")
        for picture in pictures:
            imgtext = picture["src"]
        hem_dict["img_url"] = hem_piece + imgtext
    
    # Save the hemisphere image information within mars info dictionary
    mars_dict["hemisphere_imgs"] = hem_images

    # Return the dictionary
    return mars_dict