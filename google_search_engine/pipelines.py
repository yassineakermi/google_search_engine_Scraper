# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class GoogleSearchEnginePipeline:
    def __init__(self):
        self.create_connection()

    def process_item(self, item, spider):
        print("test")
        print(item)
        self.store_db(item)
        return item

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                database = 'google',
                        )
            self.curr = self.conn.cursor()
        except Exception as ex:
            print(ex)
        
    def store_db(self, item):
        print(item)
        self.curr.execute("""insert into search_result(title,link,keywordID,type,isDone,createdAT,rank) values (%s,%s,%s,%s,%s,%s,%s)""", (
            item['title'],
            item['link'],
            item['keyword'],
            item['resultType'],
            1,
            item['createdAT'],
            item["rank"]
        ))
        self.conn.commit()
