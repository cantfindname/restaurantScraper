import scrapy
import logging
from lxml.etree import XPathEvalError
import os
import re
from scrapy.loader import ItemLoader

from ..items import ScrapebackendItem

class RestaurantSpider(scrapy.Spider):
    name = "restaurant"

    current_page = None
    base_url= 'https://www.tripadvisor.com'
    count = 0

    def start_requests(self):

        urls = [
            # 'https://www.tripadvisor.com/Restaurant_Review-g34242-d6637644-Reviews-Humble_Wood_Fire-Gainesville_Florida.html'
            # 'https://www.tripadvisor.com/Restaurants-g34242-Gainesville_Florida.html'
            'https://www.tripadvisor.com/Restaurants-g34515-Orlando_Florida.html',
            # 'https://www.tripadvisor.com/Restaurants-g34438-Miami_Florida.html'

        ]
        RestaurantSpider.count = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_page)
        
# ----------------------------------------------------------------------------------------------------
    # for testing only    
    def test(self, response):
        # print(response.xpath('/html//span[@class = "pageNum current"]/following-sibling::a[1]/@href').extract())
        restaurant_address = response.xpath(
            '/html//div[@data-test-target="restaurant-detail-info"]//a[@href ="#MAPVIEW"]/text()').get()
        current_city = re.search('(\w+)_\w+.html$',response.request.url).groups()[0]
        result_list = re.search(fr'^(.+),\s{current_city}\s*\,*\s*[A-Z]{{2}}\s*([0-9]{{5}})*-*([0-9]{{4}})*$',restaurant_address)
        
        print(current_city)
        print(result_list)
        # filename = 'smthswrong.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        print('\n')
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

        restaurant_name = response.xpath(
            '/html//h1[@data-test-target ="top-info-header"]/text()').get()
        restaurant_address = response.xpath(
            '/html//div[@data-test-target="restaurant-detail-info"]//a[@href ="#MAPVIEW"]/text()').get()

        current_city = re.search('(\w+)_\w+.html$',response.request.url).groups()[0]

        five_star_count = response.xpath(
            '/html//div[@data-value = "5"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        if five_star_count != None: five_star_count = five_star_count.replace(',','')

        four_star_count = response.xpath(
            '/html//div[@data-value = "4"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        if four_star_count != None:four_star_count = four_star_count.replace(',','')

        three_star_count = response.xpath(
            '/html//div[@data-value = "3"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        if three_star_count != None:three_star_count = three_star_count.replace(',','')

        two_star_count = response.xpath(
            '/html//div[@data-value = "2"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        if two_star_count != None:two_star_count = two_star_count.replace(',','')

        one_star_count = response.xpath(
            '/html//div[@data-value = "1"]//span[@class = "row_num  is-shown-at-tablet"]/text()').get()
        if one_star_count != None:one_star_count = one_star_count.replace(',','')

        

        if restaurant_address != None:
            result_list = re.search(fr'^(.+),\s{current_city}\s*\,*\s*[A-Z]{{2}}\s*([0-9]{{5}})*-*([0-9]{{4}})*$',restaurant_address)

        if restaurant_name != None and restaurant_address != None:
            l = ItemLoader(item=ScrapebackendItem(), response=response)

            l.replace_value('name', restaurant_name)
            l.replace_value('city', current_city)

            l.replace_value('five_star', five_star_count)
            l.replace_value('four_star', four_star_count)
            l.replace_value('three_star', three_star_count)
            l.replace_value('two_star', two_star_count)
            l.replace_value('one_star', one_star_count)

            if result_list != None:
                l.replace_value('address', result_list.groups()[0])
                l.replace_value('zipcode', result_list.groups()[1])
                l.replace_value('zc_extension', result_list.groups()[2])

            return l.load_item()



    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.extensions.throttle')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)
