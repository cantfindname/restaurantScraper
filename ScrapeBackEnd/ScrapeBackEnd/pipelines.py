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
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'scrapy123=',
            database = 'restaurant',
            use_unicode = True
        )
        self.curr = self.conn.cursor()

    def create_table(self):

        self.curr.execute("""DROP TABLE IF EXISTS fl_tb""")
        self.curr.execute("""CREATE TABLE fl_tb(
            name text,
            address text
        )""")

    def process_item(self, item, spider):
        self.curr.execute("""INSERT INTO fl_tb VALUES (%s,%s)""", (
            item['name'][0],
            item['address'][0]
            ))
        self.conn.commit()
        return item
            

