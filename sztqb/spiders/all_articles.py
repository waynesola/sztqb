#!/usr/bin/python
# coding:utf-8

import scrapy
from bs4 import BeautifulSoup
from sztqb.items import SztqbItem
import arrow
import urlparse
import datetime


class AllArticles(scrapy.Spider):
    name = "all"
    allowed_domains = ["sznews.com"]
    start_urls = [
        "http://sztqb.sznews.com"
    ]

    # 爬取指定天数，通过range(n)指定天数
    def parse(self, response):

        # # 方法一：使用list表示要爬虫的url
        # urls = ["http://sztqb.sznews.com/html/2017-03/07/node_642.htm",
        #         "http://sztqb.sznews.com/html/2017-03/06/node_642.htm",
        #         "http://sztqb.sznews.com/html/2017-03/05/node_642.htm"]
        # for u in urls:
        #     yield scrapy.Request(u, callback=self.parse_item)

        # # 方法二：使用range()循环指定一定数量的url，并用arrow指定url中的日期
        # # crawl today
        # c_date = arrow.now()
        # c_ym = c_date.format('YYYY-MM')
        # c_d = c_date.format('DD')
        # url = "http://sztqb.sznews.com/html/" + c_ym + "/" + c_d + "/node_642.htm"
        # yield url
        # # crawl [count] days
        # for count in range(2):
        #     c_date = c_date.replace(days=-1)
        #     c_ym = c_date.format('YYYY-MM')
        #     c_d = c_date.format('DD')
        #     url = "http://sztqb.sznews.com/html/" + c_ym + "/" + c_d + "/node_642.htm"
        #     yield scrapy.Request(url, callback=self.parse_item)

        # 方法三：用arrow指定日期区间
        start = datetime.datetime(2017, 3, 1)
        end = datetime.datetime(2017, 3, 31)
        c_date = arrow.now()
        c_ym = c_date.format('YYYY-MM')
        c_d = c_date.format('DD')
        url = "http://sztqb.sznews.com/html/" + c_ym + "/" + c_d + "/node_642.htm"
        yield url
        for r in arrow.Arrow.range('day', start, end):
            c_ym = r.format('YYYY-MM')
            c_d = r.format('DD')
            url = "http://sztqb.sznews.com/html/" + c_ym + "/" + c_d + "/node_642.htm"
            yield scrapy.Request(url, callback=self.parse_item)

    # 爬取当天所有非广告文章
    def parse_item(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        # 找出所有<table>标签
        ts = soup.find('div', attrs={"style": "height:730px; overflow-y:scroll; width:100%;"}) \
            .find_all('table',
                      width="100%",
                      border="0",
                      cellspacing="1",
                      cellpadding="0")
        for t in ts:
            # 找出所有<a>标签
            als = t.find('table', cellspacing="0", cellpadding="1", border="0").tbody.find_all('a')
            for al in als:
                item = SztqbItem()
                if al.div.get_text() != u"广告":
                    item['title'] = al.div.get_text()
                    # 根据当前url（当天首页）和文章相对路径，补全绝对路径
                    link = urlparse.urljoin(response.url, al.get('href'))
                    item['link'] = link
                    item['publish'] = soup.find('table', id="logoTable"). \
                        find('td', width="204", align="center", valign="top").get_text()
                    request_article = scrapy.Request(link, callback=self.parse_article)
                    request_article.meta['item'] = item
                    yield request_article

    # 爬取某篇文章正文内容
    def parse_article(self, response):
        item = response.meta['item']
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        item['text'] = soup.find('founder-content').get_text()
        yield item
