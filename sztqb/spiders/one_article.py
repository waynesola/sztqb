#!/usr/bin/python
# coding:utf-8

import scrapy
from bs4 import BeautifulSoup
from sztqb.items import SztqbItem


class OneArticle(scrapy.Spider):
    name = "onearticle"
    allowed_domains = ["sznews.com"]
    start_urls = [
        "http://sztqb.sznews.com/html/2017-03/05/content_3737273.htm"
    ]

    def parse(self, response):
        items = []
        data = response.body
        soup = BeautifulSoup(data, "html5lib")

        item = SztqbItem()
        item['title'] = soup.head.title.get_text()
        item['link'] = response.url
        item['publish'] = soup.find('span', attrs={"class": "default"}).get_text()
        item['text'] = soup.find('founder-content').get_text()
        items.append(item)

        return items
