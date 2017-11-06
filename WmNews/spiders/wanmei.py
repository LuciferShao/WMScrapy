# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import requests
import re

from WmNews.items import wanmeiNews
from scrapy.http import Request
from bs4 import BeautifulSoup

class WanmeiSpider(scrapy.Spider):
    name = 'wanmei'
    allowed_domains = ['wanmei.com']
    start_urls = ['http://www.wanmei.com/wmnews/wmnews2017/index.html']
    def __init__(self):
        soup = BeautifulSoup(requests.get(self.start_urls[0]).text,"lxml")
        year_urls=re.findall(r'href="(/.*?/index.html)', str(soup))
        for year_url in year_urls[1:]:
            self.start_urls.append(parse.urljoin(self.start_urls[0], year_url))

    def parse(self, response):
        page_urls = response.css(".nlist>a::attr(href)").extract()
        for page_url in page_urls[0:-1]:
            yield Request(url=parse.urljoin(response.url, page_url), callback=self.messageParse)

    def messageParse(self,response):
        message_urls = response.xpath("//html/body/div[2]/div[2]/div[1]/div/h2/a/@href").extract()
        for message_url in message_urls:
            print (parse.urljoin(response.url,message_url))
            yield Request(url=parse.urljoin(response.url,message_url),callback=self.newsParse)


    def newsParse(self,response):
        title = response.css(".left_col>h1::text").extract_first("")
        source = response.css(".left_col>h1>span::text").extract_first("").split(" ")[0]
        datetime = response.css(".left_col>h1>span::text").extract_first("").split(" ")[1]
        page_message = response.css(".news_cont").extract_first("")

        news_item = wanmeiNews()
        news_item["title"] = title
        news_item["source"] = source
        news_item["datetime"] = datetime
        news_item["page_message"] = page_message

        yield news_item