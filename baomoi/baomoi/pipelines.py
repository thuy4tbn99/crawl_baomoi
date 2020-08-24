# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3

class BaomoiPipeline:

    def __init__(self):
        self.create_connector()
        self.create_table()

    def create_connector(self):
        self.conn = sqlite3.connect('baomoi.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""drop table if exists paper """)
        self.curr.execute("""create table paper (
                            id text,
                            time datetime,
                            category text,
                            header text,
                            content text,
                            keyword text
                            )""")

    def store_db(self, item):
        for i in item['time']:
            print("time test:" + i)
        self.curr.execute("""insert into paper values (?, ?, ?, ?, ?, ?)""", (
            str(item['id']),
            item['time'][0],
            ', '.join(item['category']),
            item['header'][0],
            item['content'][0],
            ', '.join(map(lambda x: x.replace("\n", '').lstrip(" "), item['keyword']))
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
