import scrapy
import unidecode

class ResturantSpider(scrapy.Spider):
    name = "restaurant"
    start_urls = [
        'https://www.tripadvisor.com/Restaurants-g34242-Gainesville_Florida.html'
    ]

    def parse(self, response):
        # for resturantPage in response.css(''):

        # find the first href link in every div with data-test attribute
        restaurant_list = response.xpath('/html//div[@data-test-target = "restaurants-list"]//div[@data-test]/descendant::*[@href][1]/@href').extract()
        
        restaurant_list[0]
        # for url in restaurant_list:
            
        # for restaurant in restaurant_list:

        #     restaurant = restaurant_list.xpath('//div[@data-test]//a/@href').extract()
        #     print(restaurant)
        #print(restaurant_list[0])
        # with open('tte.txt','w') as f:
        #     f.write(unidecode.unidecode(restaurant_list[0]))
        # for restaurant in restaurant_list.xpath('/html//div[@data-test = r"list_item"]').extract():
        #     print("\n\n\n\n\n")
        #     print(restaurant)


     
