# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from items import SztqbItem  # 此句非必要，在多个items时可能需要用到


# 数据库链接
def dbHandle():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='88888888',
                                 db='sztqb',  # db亦作database，即Schema
                                 charset='utf8mb4')
    return connection


class SztqbPipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == SztqbItem:  # 此句非必要，在多个items时可能需要用到
            dbObject = dbHandle()
            cursor = dbObject.cursor()
            # 注意此处sql语句无需添加id，因为item并没有id；数据库的id会自增长；Table名为from_20160101_to_20170322
            sql = "insert into sztqb.from_20160101_to_20170322 (title,publish,link,text) values (%s,%s,%s,%s)"

            try:
                cursor.execute(sql,
                               (item['title'], item['publish'], item['link'], item['text']))
                dbObject.commit()

            finally:
                dbObject.close()

            return item
