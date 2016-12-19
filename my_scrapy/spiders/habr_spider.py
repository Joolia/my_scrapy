# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.linkextractor import LinkExtractor
from scrapy.http import HtmlResponse
from my_scrapy.items import MyScrapyItem


class HabrSpider(scrapy.Spider):
    name = 'articles_on_python'
    allowed_domains = ["https://habrahabr.ru/"]

    start_urls = ["https://habrahabr.ru/search/page1/?q=python&target_type=posts&flow=&order_by=relevance"]

    def start_requests(self):
        # yield scrapy.Request("https://habrahabr.ru/search/page1/?q=python&target_type=posts&flow=&order_by=relevance")

        for i in range(1, 30):
            yield scrapy.Request(
                "https://habrahabr.ru/search/page" + str(i) + "/?q=python&target_type=posts&flow=&order_by=relevance",
                self.parse)

    def parse(self, response):
        namelist = response.xpath(
            "//a[@class='post-author__link']//text()").extract()
        titlelist = response.xpath(
            "concat(//a[@class='post__title_link']//text(), //a[@class='post__title_link']//em/text())").extract()
        # titlelist = response.xpath("//li//a[@class='post-author__link']/@href").extract()

        # namelist = response.css('').extract

        lenlist = len(namelist)

        for i in range(0, lenlist):
            item = MyScrapyItem()
            item['name'] = namelist[i].strip()
            item['title'] = titlelist[i]
            yield item
