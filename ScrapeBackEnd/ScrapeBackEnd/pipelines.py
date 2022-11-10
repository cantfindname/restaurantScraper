# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from enum import unique
from venv import create
from itemadapter import ItemAdapter
import mysql.connector
from thefuzz import fuzz, process


class ScrapebackendPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_resta_table()
        self.create_TA_table()
        # self.find_id()
        # self.find_id_exact()

    def find_id_exact(self, item):
        self.curr.execute(
            f"""SELECT unique_id FROM restaurant.restaurant_info where name ="{item.name[0]}" and address = "{item.address[0]}" """)
        records = self.curr.fetchall()
        if len(records) > 1:
            for row in records:
                print(row[0])
        return records[0][0]

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='scrapy123=',
            database='restaurant',
            use_unicode=True
        )
        self.curr = self.conn.cursor()

    def create_resta_table(self):

        self.curr.execute("""DROP TABLE IF EXISTS restaurant_info""")
        self.curr.execute("""CREATE TABLE restaurant_info (
            unique_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name text,
            address text,
            city text,
            zipcode int,
            zc_extension int
        )""")

    def create_TA_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS TA_info""")
        self.curr.execute("""CREATE TABLE TA_info(
            unique_id INT,
            five_star int,
            four_star int,
            three_star int,
            two_star int,
            one_star int
            )
        """)

    def process_item(self, item, spider):

        self.curr.execute("""INSERT INTO restaurant_info
        (name, address, city, zipcode, zc_extension)
        VALUES (%s,%s,%s,%s,%s)""", (
            item.name[0],
            item.address[0],
            item.city[0],
            item.zipcode[0],
            item.zc_extension[0]
        ))
        self.conn.commit()

        self.curr.execute("""INSERT INTO TA_info
        (unique_id,five_star, four_star, three_star, two_star, one_star)
        VALUE (%s,%s,%s,%s,%s,%s)""", (
            self.find_id_exact(item),
            item.five_star[0],
            item.four_star[0],
            item.three_star[0],
            item.two_star[0],
            item.one_star[0]
        ))

        self.conn.commit()
        return item


class YelpPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_yelp_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='scrapy123=',
            database='restaurant',
            use_unicode=True
        )
        self.curr = self.conn.cursor()

    def create_yelp_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS yelp_info""")
        self.curr.execute("""CREATE TABLE yelp_info(
            unique_id INT,
            yl_tags text,
            yl_rating_count int,
            yl_five_star int,
            yl_four_star int,
            yl_three_star int,
            yl_two_star int,
            yl_one_star int,
            yl_first_review text,
            yl_second_review text,
            yl_third_review text
            )""")

    def find_id(self, item):
        self.curr.execute(
            f"""
                SELECT unique_id, name, address FROM restaurant.restaurant_info where city = "{item.city[0]}" and zipcode = "{item.zipcode[0]}"
            """)

        records = self.curr.fetchall()
        all_restaurants = []
        for row in records:
            all_restaurants.append(row[1])

        fuzzy_search = process.extract(
            item.name[0], all_restaurants, limit=1, scorer=fuzz.partial_ratio)
        if fuzzy_search != []:
            index = all_restaurants.index(fuzzy_search[0][0])
            address = []
            current_add = records[index][2]
            # print(current_add)
            address.append(current_add)
            # print('current address: ' + address[0])
            fuzzy_search_address = process.extract(
                item.address[0], address, limit=1, scorer=fuzz.partial_ratio)
            print(fuzzy_search_address)
        print(fuzzy_search)

        if fuzzy_search == [] or fuzzy_search[0][1] + fuzzy_search_address[0][1] <= 140:
            self.curr.execute("""
            INSERT INTO restaurant_info (name, address, city, zipcode)
            VALUES (%s,%s,%s,%s)""", (
                item.name[0],
                item.address[0],
                item.city[0],
                item.zipcode[0],
            ))
            self.conn.commit()

            self.curr.execute("""
                SELECT unique_id FROM restaurant.restaurant_info ORDER BY unique_id DESC LIMIT 1
            """)
            current_unique_id = self.curr.fetchall()

            return current_unique_id[0][0]

        else:
            index = all_restaurants.index(fuzzy_search[0][0])
            unique_id = records[index][0]
            return unique_id

    def process_item(self, item, spider):

        self.curr.execute("""INSERT INTO yelp_info
        (unique_id, yl_tags, yl_rating_count, yl_five_star, yl_four_star, yl_three_star,
        yl_two_star, yl_one_star, yl_first_review, yl_second_review, yl_third_review)
        VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            self.find_id(item),
            item.tags[0],
            item.rating_count[0],
            item.five_star[0],
            item.four_star[0],
            item.three_star[0],
            item.two_star[0],
            item.one_star[0],
            item.first_review[0],
            item.second_review[0],
            item.third_review[0]
        ))
        self.conn.commit()
        return item
