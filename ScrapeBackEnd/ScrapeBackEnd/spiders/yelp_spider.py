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

from ..items import YelpBackendItem


class YelpSpider(scrapy.Spider):
    name = "yelp"
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapeBackEnd.pipelines.YelpPipeline': 301
        }
    }

    # headers = {
    #     'accept': '*/*',
    #     'accept-encoding': 'gzip, deflate, br',
    #     'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    #     'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    # }

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
            # 'https://www.yelp.com/biz/the-top-gainesville?osq=Restaurants',
            # 'https://www.yelp.com/biz/ten-seconds-yunnan-rice-noodles-gainesville?osq=Restaurants'
            # 'https://www.yelp.com/biz/paris-banh-mi-gainesville-gainesville?osq=Restaurants'
            # 'https://www.yelp.com/biz/sebastian-alexander-gainesville-2?osq=Restaurants'
            # 'https://www.yelp.com/biz/the-burger-den-eustis'
            # 'https://www.yelp.com/biz/taco-s-352-gainesville?osq=Restaurants'

        ]

        YelpSpider.count = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_page)

# ----------------------------------------------------------------------------------------

    def test(self, response):
        # restaurant_name = response.xpath('/html//div[@data-testid = "photoHeader"]//h1[1]/text()').get()
        # print(restaurant_name)

        rating_count = response.xpath(
            '/html//div[@data-testid = "review-summary"]//div[@class = " rating-text__09f24__VDRkR padding-t0-5__09f24__lDQoQ border-color--default__09f24__NPAKY"]/p/text()').get()
        print(rating_count)

        if rating_count != None:
            rating_count = rating_count.replace(' reviews', '')
            rating_count = rating_count.replace(' review', '')
            print(rating_count)

            stars = response.xpath(
                '/html//section[@aria-label= "Recommended Reviews"]//div[@data-testid = "review-summary"]//div[@data-testid = "review-summary-bar"]/div[2]/div/div/@style').extract()
            print(stars)

            total_percent = 0
            separate_ratings = []
            for star in stars:
                star = star.replace('width:', '')
                star = star.replace('%', '')
                separate_ratings.insert(0, float(star))
                total_percent += float(star)
                print(star)

            perPercent = int(rating_count) / total_percent
            print(perPercent)

        filename = 'smthswrong.txt'
        with open(filename, 'wb') as f:
            f.write(response.body)


# ----------------------------------------------------------------------------------------


    def parse_all_page(self, response):

        current_city = 'Gainesville'  # change later!

        yield scrapy.Request(url=response.request.url, callback=self.parse_page_list)

        page_count = response.xpath(
            '/html//main[@id = "main-content"]//div[@role = "navigation"]//span[@class = " css-chan6m"]/text()').get()

        print(page_count)

        if page_count != None:
            page_count = page_count.replace('1 of ', '')
            print(page_count)
            print(response.request.url)

            for page_num in range(10, int(page_count)*10, 10):
                print(page_num)
                search_url = YelpSpider.base_url + \
                    f'/search?find_desc=Restaurants&find_loc={self.format_string(current_city)}%2C+{YelpSpider.current_state}&start={page_num}'

                yield scrapy.Request(url=search_url, callback=self.parse_page_list)

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
            print('ummmm, yelp being mean again')
            print(response.request.url)
            # self.parse_page
        else:
            # print(unidecode.unidecode(restaurant_name))

            # get street address, city, zipcode
            restaurant_address = response.xpath(
                '/html//address[@class]/p[@class = " css-r9996t"]/a/span[@class]/text()').get()
            restaurant_sec_address = response.xpath(
                '/html//address[@class]/p[@class = " css-1sb02f4"]/span[@class]/text()').get()
            restaurant_cityZip = response.xpath(
                '/html//address[@class]/p[@class = " css-qgunke"]/span[@class]/text()').get()
            # print(restaurant_cityZip)
            # city = restaurant_cityZip.split(', ')[0]
            # zipcode = restaurant_cityZip.split(', ')[1].split(' ')[1]

            # get restaurant tags
            restaurant_tags = response.xpath(
                '/html//div[@data-testid = "photoHeader"]//span[span[@class = " css-1fdy0l5"]]//a[@class = "css-1m051bw"]/text()'
            ).extract()
            if restaurant_tags != None:
                tags = ', '.join(str(tag) for tag in restaurant_tags)

            # get total and separate rating counts
            rating_count = response.xpath(
                '/html//div[@data-testid = "review-summary"]//div[@class = " rating-text__09f24__VDRkR padding-t0-5__09f24__lDQoQ border-color--default__09f24__NPAKY"]/p/text()').get()

            # print(rating_count)
            if rating_count != None:
                rating_count = rating_count.replace(' reviews', '')
                rating_count = rating_count.replace(' review', '')

                stars = response.xpath(
                    '/html//section[@aria-label= "Recommended Reviews"]//div[@data-testid = "review-summary"]//div[@data-testid = "review-summary-bar"]/div[2]/div/div/@style').extract()

                total_percent = 0
                separate_ratings = []
                for star in stars:
                    star = star.replace('width:', '')
                    star = star.replace('%', '')
                    separate_ratings.insert(0, float(star))
                    total_percent += float(star)

                perPercent = int(rating_count) / total_percent
            # five_star_count = separate_ratings[4] * perPercent
            # four_star_count = separate_ratings[3] * perPercent
            # three_star_count = separate_ratings[2] * perPercent
            # two_star_count = separate_ratings[1] * perPercent
            # one_star_count = separate_ratings[0] * perPercent

            first_review = response.xpath(
                '/html//section[@aria-label = "Recommended Reviews"]//ul[@class = " undefined list__09f24__ynIEd"]/li//span[@lang = "en"]/text()').extract()
            # print(' '.join(unidecode.unidecode(each) for each in first_review))

            second_review = response.xpath(
                '/html//section[@aria-label = "Recommended Reviews"]//ul[@class = " undefined list__09f24__ynIEd"]/li[2]//span[@lang = "en"]/text()').extract()
            # print(' '.join(unidecode.unidecode(each)
            #       for each in second_review))

            third_review = response.xpath(
                '/html//section[@aria-label = "Recommended Reviews"]//ul[@class = " undefined list__09f24__ynIEd"]/li[3]//span[@lang = "en"]/text()').extract()
            # print(' '.join(unidecode.unidecode(each) for each in third_review))

            if restaurant_name != None and restaurant_address != None and restaurant_cityZip != None:
                current_item = ItemLoader(
                    item=YelpBackendItem(), response=response)

                current_item.replace_value(
                    'name', unidecode.unidecode(restaurant_name))

                if restaurant_sec_address != None:
                    current_item.replace_value(
                        'address', restaurant_address + ' ' + restaurant_sec_address)
                else:
                    current_item.replace_value(
                        'address', restaurant_address)

                current_item.replace_value(
                    'city', restaurant_cityZip.split(', ')[0])

                current_item.replace_value(
                    'zipcode', restaurant_cityZip.split(', ')[1].split(' ')[1])

                if restaurant_tags != None:
                    current_item.replace_value('tags', tags)

                current_item.replace_value('rating_count', rating_count)

                if rating_count != None:
                    current_item.replace_value(
                        'five_star', round(separate_ratings[4] * perPercent))
                    current_item.replace_value(
                        'four_star', round(separate_ratings[3] * perPercent))
                    current_item.replace_value(
                        'three_star', round(separate_ratings[2] * perPercent))
                    current_item.replace_value(
                        'two_star', round(separate_ratings[1] * perPercent))
                    current_item.replace_value(
                        'one_star', round(separate_ratings[0] * perPercent))

                if first_review != None:
                    current_item.replace_value(
                        'first_review', ' '.join(
                            unidecode.unidecode(each) for each in first_review)
                    )

                if second_review != None:
                    current_item.replace_value(
                        'second_review', ' '.join(
                            unidecode.unidecode(each) for each in second_review)
                    )
                if third_review != None:
                    current_item.replace_value(
                        'third_review', ' '.join(
                            unidecode.unidecode(each) for each in third_review)
                    )
                return current_item.load_item()

        # print(restaurant_name)
