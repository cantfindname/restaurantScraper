from urllib.parse import urljoin
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
            # 'https://www.tripadvisor.com/Restaurant_Review-g34127-d491231-Reviews-Celebration_Town_Tavern-Celebration_Orlando_Florida.html'
            # 'https://www.tripadvisor.com/Restaurants-g34242-Gainesville_Florida.html',
            # 'https://www.tripadvisor.com/Restaurants-g34515-Orlando_Florida.html',
            # 'https://www.tripadvisor.com/Restaurants-g34438-Miami_Florida.html'
            'https://www.tripadvisor.com/Restaurants-g28930-Florida.html'

        ]
        RestaurantSpider.count = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_state_pg)
        
# ----------------------------------------------------------------------------------------------------
    # for testing only    

        def test(self, response):
            print('\n')

        # filename = 'smthswrong.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)


# -----------------------------------------------------------------------------------------------------

    def get_state_pg(self, response):
        city_list = response.xpath('/html//div[@class="geos_grid"]//div[@class ="geo_name"]/a[@href]/@href').extract()
        for city in city_list:
            # city = city.replace('\n','')
            # print(urljoin(RestaurantSpider.base_url, city))
            yield scrapy.Request(url= urljoin(RestaurantSpider.base_url, city), callback=self.parse_all_page)

        second_page = response.xpath(
            '/html//span[@class = "pageNum current"]/following-sibling::a[1]/@href').get()
        yield scrapy.Request(url=RestaurantSpider.base_url+second_page, callback=self.parse_state_page)


    def parse_state_page(self, response):
        total_city = response.xpath(
            '/html//div[@class="pagination"]/span[@class="pgCount"]/text()[2]').get()
        total_city = total_city.replace(' ','')

        city_list_url = response.request.url
        city_list_url = city_list_url.replace('oa20','oa0')

        for i in range(20, int(total_city), 20):
            city_list_url = city_list_url.replace(f'oa{i-20}', f'oa{i}')
            # print(city_list_url)
            yield scrapy.Request(url= city_list_url, callback=self.parse_city_list)

    def parse_city_list(self, response):
        city_list = response.xpath('/html//ul[@class="geoList"]/li/a/@href').extract()
        for city in city_list:
            yield scrapy.Request(url= urljoin(RestaurantSpider.base_url, city), callback=self.parse_all_page)
            # print(urljoin(RestaurantSpider.base_url, city))

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


        # current_city = re.search('(\w+)_\w+.html$',response.request.url).groups()[0]
        # current_city = current_city.replace('_',' ')

        current_city = response.xpath(
            '/html//ul[@data-test-target="breadcrumbs"]/li[last()-1]/a/span/text()').get()
        current_city = current_city.replace(' Restaurants','')


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

            result_list = re.search(
                fr'^(.+),\s{current_city}\s*\,*\s*\w*\,*\s*[A-Z]{{2}}\s*([0-9]{{5}})*-*([0-9]{{4}})*$',restaurant_address)
            # if result_list.groups()[1] == None:


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

