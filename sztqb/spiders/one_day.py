#!/usr/bin/python
# coding:utf-8

import scrapy
from bs4 import BeautifulSoup
from sztqb.items import SztqbItem


class OneDay(scrapy.Spider):
    name = "oneday"
    allowed_domains = ["sznews.com"]
    start_urls = [
        "http://sztqb.sznews.com/"
    ]

    def parse(self, response):
        items = []
        data = response.body
        soup = BeautifulSoup(data, "html5lib")

        ts = soup.find('div', attrs={"style": "height:730px; overflow-y:scroll; width:100%;"}) \
            .find_all('table',
                      width="100%",
                      border="0",
                      cellspacing="1",
                      cellpadding="0")

        for t in ts:
            als = t.find('table', cellspacing="0", cellpadding="1", border="0").tbody.find_all('a')
            for al in als:
                item = SztqbItem()
                if al.div.get_text() != u"广告":
                    item['title'] = al.div.get_text()
                    item['link'] = "http://sztqb.sznews.com/html/2017-03/06/" + al.get('href')
                    item['publish'] = soup.find('table', id="logoTable"). \
                        find('td', width="204", align="center", valign="top").get_text()
                    items.append(item)

        return items
