from urllib.request import urlopen
from urllib.parse import urljoin
import scrapy
import logging
import re
from scrapy.loader import ItemLoader
from thefuzz import fuzz, process
import unidecode
import requests
from bs4 import BeautifulSoup
import json


class YelpSpider(scrapy.Spider):
    name = "yelp"
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapeBackEnd.pipelines.YelpPipeline': 301
        }
    }

    # current_page = None
    current_state = 'FL'

    count = 0
    base_url = 'https://www.yelp.com'

    def start_requests(self):

        urls = [
            'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Gainesville%2C+FL'
            # 'https://www.yelp.com/search/snippet?find_desc=Restaurants&find_loc=deerfield_beach%2C+FL'
            # 'https://www.yelp.com/biz/sugar-creek-restaurant-gainesville?osq=Restaurants',
            # 'https://www.yelp.com/biz/my-pizza-place-on-main-alachua-2?osq=Restaurants',
            # 'https://www.yelp.com/biz/old-florida-cafe-micanopy-2?osq=Restaurants'
            # 'https://www.yelp.com/biz/the-yearling-restaurant-hawthorne?osq=Restaurants'

        ]
        YelpSpider.count = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_page)

# ----------------------------------------------------------------------------------------

    def test(self, response):
        # restaurant_name = response.xpath('/html//div[@data-testid = "photoHeader"]//h1[1]/text()').get()
        # print(restaurant_name)

        restaurant_list = response.xpath(
            """/html//main[@id = "main-content"]//div[@class = " container__09f24__mpR8_ hoverable__09f24__wQ_on border-color--default__09f24__NPAKY"]
            //div[contains(@class, "arrange-unit")][2]//span[@data-font-weight = "bold"]/a[@href]/@href""").extract()

        for restaurant in restaurant_list:
            print(YelpSpider.base_url+restaurant)
            yield scrapy.Request(url=YelpSpider.base_url+restaurant, callback=self.parse_all_page)
            YelpSpider.count += 1

        # filename = 'smthswrong.txt'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)


# ----------------------------------------------------------------------------------------


    def parse_all_page(self, response):

        current_city = 'Gainesville'  # change later!

        # if YelpSpider.current_page == None:
        #     YelpSpider.current_page = response.request.url

        # for restaurant in id_list:
        # print(restaurant)
        yield scrapy.Request(url=response.request.url, callback=self.parse_page_list)

        page_count = response.xpath(
            '/html//main[@id = "main-content"]//div[@role = "navigation"]//span[@class = " css-chan6m"]/text()').get()

        # data = json.loads(response.body.decode(response.encoding))
        # page_count = data['searchPageProps']['mainContentComponentsListProps'][12]['props']['totalResults']
        print(page_count)

        if page_count != None:
            page_count = page_count.replace('1 of ', '')
            print(page_count)
            print(response.request.url)

            for page_num in range(10, int(page_count)*10, 10):
                print(page_num)
                search_url = YelpSpider.base_url + \
                    f'/search?find_desc=Restaurants&find_loc={self.format_string(current_city)}%2C+{YelpSpider.current_state}&start={page_num}'
                # print(search_url)
                # print(self.get_biz_id(search_url))

                yield scrapy.Request(url=search_url, callback=self.parse_page_list)

    # def get_biz_url(self,response):
    #     print(response)
    #     jsonurl = urlopen(response)
    #     data = json.load(jsonurl)
    #     id_list = []
    #     for restaurant in data['searchPageProps']['mainContentComponentsListProps']:
    #         try:
    #             # print(restaurant['bizId'])
    #             # print(restaurant['searchResultBusiness']['isAd'])
    #             if (restaurant['searchResultBusiness']['isAd'] == False):
    #                 # print('in')
    #                 id_list.append(restaurant['bizId'])
    #         except:
    #             pass

    #     return id_list

    # def get_biz_id(self,response):
    #     print('hi')
    #     data = json.loads(response.body.decode(response.encoding))
    #     id_list = []
    #     for restaurant in data['searchPageProps']['mainContentComponentsListProps']:
    #         try:
    #             # print(restaurant['bizId'])
    #             # print(restaurant['searchResultBusiness']['isAd'])
    #             if (restaurant['searchResultBusiness']['isAd'] == False):
    #                 # print('in')
    #                 id_list.append(restaurant['bizId'])
    #         except:
    #             pass

    #     return id_list

    def format_string(self, city_str):
        city_str = city_str.replace(' ', '+')
        city_str = city_str.replace('\'', '%27')
        return city_str

    def parse_page_list(self, response):

        restaurant_list = response.xpath(
            """/html//main[@id = "main-content"]//div[@class = " container__09f24__mpR8_ hoverable__09f24__wQ_on border-color--default__09f24__NPAKY"]
            //div[contains(@class, "arrange-unit")][2]//span[@data-font-weight = "bold"]/a[@href]/@href""").extract()

        for restaurant in restaurant_list:
            print(YelpSpider.base_url+restaurant)
            yield scrapy.Request(url=YelpSpider.base_url+restaurant, callback=self.parse_page)
            YelpSpider.count += 1

        print('count: ' + str(YelpSpider.count))

    def parse_page(self, response):
        # print(response.request.url)
        restaurant_name = response.xpath(
            '/html//div[@data-testid = "photoHeader"]//h1[1]/text()').get()
        if restaurant_name == None:
            print(response.request.url)
            print(response.body)
            # self.parse_page
        else:
            print(unidecode.unidecode(restaurant_name))
        # print(restaurant_name)


# //span[@class = " css-chan6m"]/text(
