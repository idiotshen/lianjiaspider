# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class LianjiaspiderPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(host = '', port = 3306, user = '', password = '', database = '', charset="utf8")
        self.curs = self.db.cursor()
        print('连接成功-----------------------------------------------------')

    def process_item(self, item, spider):
        sql = "INSERT INTO home(title, price, tip_decoration, size, type, level, face, underground, housingestate, location) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (item['title'], item['price'], item['tip_decoration'], item['size'], item['type'], item['level'], item['face'],item['underground'], item['housingEstate'], item['location'])
        self.curs.execute(sql)
        self.db.commit()

    def close_spider(self, spider):
        self.curs.close()
        self.db.close()

