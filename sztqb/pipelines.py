# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from sztqb import settings
from sztqb.items import SztqbItem
from scrapy import log


class SztqbPipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == SztqbItem:
            try:
                self.cursor.execute("""select * from mytable where music_url = %s""", item["music_url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update music_douban set music_name = %s,music_alias = %s,music_singer = %s,
                            music_time = %s,music_rating = %s,music_votes = %s,music_tags = %s,music_url = %s
                            where music_url = %s""",
                        (item['music_name'],
                         item['music_alias'],
                         item['music_singer'],
                         item['music_time'],
                         item['music_rating'],
                         item['music_votes'],
                         item['music_tags'],
                         item['music_url'],
                         item['music_url']))
                else:
                    self.cursor.execute(
                        """insert into music_douban(music_name,music_alias,music_singer,music_time,music_rating,
                          music_votes,music_tags,music_url)
                          value (%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (item['music_name'],
                         item['music_alias'],
                         item['music_singer'],
                         item['music_time'],
                         item['music_rating'],
                         item['music_votes'],
                         item['music_tags'],
                         item['music_url']))
                self.connect.commit()
            except Exception as error:
                log(error)
            return item

        else:
            return item
