# -*- coding: utf-8 -*-
import scrapy
from lxml import etree

from Name.items import NameItem


class NameSpider(scrapy.Spider):
    name = 'name'
    allowed_domains = ['resgain.net']
    start_urls = ['http://www.resgain.net/xmdq.html?tdsourcetag=s_pctim_aiomsg']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        yield scrapy.Request(url='http://www.resgain.net/xmdq.html?tdsourcetag=s_pctim_aiomsg',
                             headers=headers,
                             method='GET',
                             callback=self.parse,
                             )

    def parse(self, response):

        resutls = response.css(".col-xs-12 .btn")
        for name in resutls:
            name_item = NameItem()
            name_item['first_name'] = name.css("::text").extract_first()
            name_item['url'] =name.css("::attr('href') ").extract_first()
            yield name_item
