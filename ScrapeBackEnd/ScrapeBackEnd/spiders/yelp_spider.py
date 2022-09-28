
from urllib.parse import urljoin
import scrapy
import logging
import re
from scrapy.loader import ItemLoader
from thefuzz import fuzz, process
import unidecode
import requests
from bs4 import BeautifulSoup

class YelpSpider(scrapy.Spider):
    name = "yelp"
    custom_settings = {
        'ITEM_PIPELINES':{
            'ScrapeBackEnd.pipelines.YelpPipeline' : 301
        }
    }
    current_page = None
    base_url= 'https://www.yelp.com'

    start_urls = ['https://www.yelp.com/biz/jajaja-plantas-mexicana-new-york-2?osq=Vegetarian+Food']
    count = 0

    headers = {
        "User-Agent":"Mozilla/5.0"

    }

    def parse(self,response):
        print(response.body)





    def parse_api(self, response):
        print(response.body)
        pass




        

        
