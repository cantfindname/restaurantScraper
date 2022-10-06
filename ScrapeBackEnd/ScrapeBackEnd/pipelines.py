# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class ScrapebackendPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_resta_table()
        self.create_TA_table()
        # self.find_id()
        # self.find_id_exact()

    def find_id(self, item):
        self.curr.execute(
            f"""
                SELECT unique_id, name, address FROM restaurant.restaurant_info where city = "{item.city[0]}" and zipcode = "{item.zipcode[0]}"
            """)

        records = self.curr.fetchall()

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
    """A pipeline for filtering out items which contain certain words in their
        description"""

    def __init__(self):
        self.create_connection()

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
            
            
            )""")

    def process_item(self, item, spider):
        return item
