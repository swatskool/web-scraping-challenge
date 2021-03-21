from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def news(url_nasa):
    browser = init_browser()
    browser.visit(url_nasa)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = []
    news_para = []

    results= soup.find_all('li', class_ = 'slide')
    for each_result in results:
        result_title = each_result.find_all('div', class_="content_title")
        for titles in result_title:
            try:
                news_title.append(titles.text)
            except:
                print('*****************************************')
        result_p = each_result.find_all('div', class_="rollover_description_inner")
        for para in result_p:
            try:
                news_para.append(para.text)
            except:
                print('<<<<<<<<<<<<<<<<<<<')
        return(news_title,news_para)
def feature_image(url_feature):
    browser = init_browser()
    browser.visit(url_feature)
    browser.find_by_css('img.BaseImage').click()
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    feature_url = soup.find_all('img', class_= 'BaseImage')[0]['src']
    return(feature_url)

def space_facts(url_space_facts):
    browser = init_browser()
    browser.visit(url_space_facts)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    html_tables = pd.read_html(url_space_facts)
    df = html_tables[2]
    df.rename(columns={0: ' ', 1: 'Mars'}, inplace = True) 
    df.reset_index(drop=True, inplace=True)
    table_str = df.to_html()
    table_str.replace('class="dataframe"', 'class="table table-striped"')
    table_str.replace('\n','')
    return table_str

def hemisphere(url_hemi):
    browser = init_browser()
    browser.visit(url_hemi)
    hemispheres = []
    links = browser.find_by_css("a.product-item img")
    for each_link in range(len(links)):
        print(each_link)
        hemis_dict = {}
        browser.find_by_css('a.product-item img')[each_link].click()
        sample = browser.links.find_by_text('Sample').first
        print(sample)
        hemis_dict['url'] = sample['href']
        hemis_dict['title'] = browser.find_by_css('h2.title').text
        hemispheres.append(hemis_dict)
        browser.back()
    return hemispheres


def scrape():
    browser = init_browser()
    listings = {}
    head = []
    text = []
    
    url_nasa = 'https://mars.nasa.gov/news/'
    url_feature = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_space_facts = 'https://space-facts.com/mars/'
    url_hemi = 'https://marshemispheres.com/'
    head, text = news(url_nasa)
    hemispheres = hemisphere(url_hemi)
    space_table = space_facts(url_space_facts)
    featured_image = feature_image(url_feature)
    
    
    print(head)
    print('I am here')
    
    listings['heading'] = head
    listings['text'] = text
    listings['feature_image'] = featured_image
    listings['table'] = space_table
    listings['hemisphere'] = hemispheres
    
    
    
    
    
    
    
    
    
    return listings
