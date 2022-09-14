import scrapy
import logging
from lxml.etree import XPathEvalError
import os

from ..items import ScrapebackendItem

class RestaurantSpider(scrapy.Spider):
    name = "restaurant"

    current_page = None
    base_url= 'https://www.tripadvisor.com'
    count = 0

    def start_requests(self):

        urls = [
            'https://www.tripadvisor.com/Restaurants-g34242-Gainesville_Florida.html'
            # 'https://www.tripadvisor.com/Restaurants-g34515-Orlando_Florida.html',
            # 'https://www.tripadvisor.com/Restaurants-g34438-Miami_Florida.html'

        ]
        RestaurantSpider.count = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_page)
        
# ----------------------------------------------------------------------------------------------------
    # for testing only    
    def test(self, response):
        # print(response.xpath('/html//span[@class = "pageNum current"]/following-sibling::a[1]/@href').extract())
        five_star_review = response.xpath(
            '/html//div[@data-value = "5"]//span[@class = "row_num  is-shown-at-tablet"]/text()').extract()
        print(five_star_review)
        
        # filename = 'smthswrong.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

# -----------------------------------------------------------------------------------------------------

    def parse_all_page(self, response):

        if RestaurantSpider.current_page == None:
            RestaurantSpider.current_page = response.request.url

        yield scrapy.Request(url=RestaurantSpider.current_page, callback=self.parse_page_list, dont_filter=True)

        # parse all pages with restaurant lists 
        next_page = response.xpath(
            '/html//span[@class = "pageNum current"]/following-sibling::a[1]/@href').extract()

        if next_page != []:
            RestaurantSpider.current_page = RestaurantSpider.base_url+str(next_page[0])
            yield scrapy.Request(url=RestaurantSpider.current_page,callback=self.parse_all_page)
        


    # parse list items from all list pages
    def parse_page_list(self, response):
        restaurant_list = response.xpath(
            '/html//div[@data-test-target = "restaurants-list"]//div[@data-test]/descendant::*[@href][1]/@href').extract()
        
        # Scrape info from all restaurant homepages
        for restaurant in restaurant_list:
            yield scrapy.Request(url=RestaurantSpider.base_url+restaurant, callback = self.parse_page)
            RestaurantSpider.count +=1 

        print('count:'+ str(RestaurantSpider.count))
        
    # input restaurant homepage and parse information
    def parse_page(self, response):
        items = ScrapebackendItem()

        restaurant_name = response.xpath(
            '/html//h1[@data-test-target ="top-info-header"]/text()').get()
        restaurant_address = response.xpath(
            '/html//div[@data-test-target="restaurant-detail-info"]//a[@href ="#MAPVIEW"]/text()').get()

        five_star_count = response.xpath(
            '/html//div[@data-value = "5"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        four_star_count = response.xpath(
            '/html//div[@data-value = "4"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        three_star_count = response.xpath(
            '/html//div[@data-value = "3"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        two_star_count = response.xpath(
            '/html//div[@data-value = "2"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        one_star_count = response.xpath(
            '/html//div[@data-value = "1"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        #print(restaurant_name)
        #print(restaurant_address)

        if restaurant_name != None and restaurant_address != None:
            items['name'] = restaurant_name
            items['address'] = restaurant_address

            if five_star_count == None:
                items['five_star'] = 0
            else:
                items['five_star'] = int(five_star_count)
            if four_star_count == None: 
                items['four_star'] = 0
            else:
                items['four_star'] = int(four_star_count)
            if three_star_count == None: 
                items['three_star'] = 0
            else:
                items['three_star'] = int(three_star_count)
            if two_star_count == None: 
                items['two_star'] = 0
            else:
                items['two_star'] = int(two_star_count)
            if one_star_count == None: 
                items['one_star'] = 0
            else:
                items['one_star'] = int(one_star_count)

            yield items


    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.extensions.throttle')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)
