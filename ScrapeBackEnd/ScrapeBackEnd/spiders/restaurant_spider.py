import scrapy
import logging
import unidecode

from ..items import ScrapebackendItem

class RestaurantSpider(scrapy.Spider):
    name = "restaurant"

    current_page = None
    base_url= 'https://www.tripadvisor.com'
    count = 0

    def start_requests(self):

        urls = [
            'https://www.tripadvisor.com/Restaurants-g34242-Gainesville_Florida.html',
            'https://www.tripadvisor.com/Restaurants-g34515-Orlando_Florida.html',
            'https://www.tripadvisor.com/Restaurants-g34438-Miami_Florida.html'

        ]
        RestaurantSpider.count = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_page)
        
# ----------------------------------------------------------------------------------------------------
    # for testing only    
    def test(self, response):
        # print(response.xpath('/html//span[@class = "pageNum current"]/following-sibling::a[1]/@href').extract())
        print('reached test')
        items = ScrapebackendItem()
        items['name'] ='love you'
        items['address'] = 'route zero'
        yield items

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
            '/html//h1[@data-test-target ="top-info-header"]/text()').extract()
        restaurant_address = response.xpath(
            '/html//div[@data-test-target="restaurant-detail-info"]//a[@href ="#MAPVIEW"]/text()').extract()

        #print(restaurant_name)
        #print(restaurant_address)

        if restaurant_name != [] and restaurant_address != []:
            items['name'] = restaurant_name
            items['address'] = restaurant_address
            yield items


    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.extensions.throttle')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)
