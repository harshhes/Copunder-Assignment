# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class CopunderdogPipeline:
    key = open("copunderdog/key.txt").read()

    def open_spider(self,spider):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = self.key,
            database = 'copunderdog'
        )
        self.c = self.connection.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS sneakers(
            Item_url            TEXT,
            Name                TEXT,
            Price               TEXT,
            Sizes_Available     TEXT,
            SKU                 TEXT,
            Categories          TEXT,
            Description         TEXT,
            All_image_URLs      TEXT
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO sneakers 
            (Item_url, Name, Price, Sizes_Available, SKU, Categories, Description, All_image_URLs) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            item.get('Item_url'),
            item.get('Name'),
            item.get('Price'),
            item.get('Sizes_Available'),
            item.get('SKU'),
            item.get('Categories'),
            item.get('Description'),
            item.get('All_image_URLs')
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()
        self.c.close()