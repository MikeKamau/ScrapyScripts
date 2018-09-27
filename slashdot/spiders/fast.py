# -*- coding: utf-8 -*-
import scrapy
from slashdot.items import SlashdotItem
from scrapy.http import Request
try:
    from urllib.parse import urljoin
except ImportError:
     from urlparse import urljoin

class GeekSpider(scrapy.Spider):
    name = 'fast'
    allowed_domains = ['slashdot.org']
    start_urls = ['http://slashdot.org/']

    def parse(self, response):
        #Get the next index URLs and yield Requests
        next_selector = response.xpath('//div[@id="fh-paginate"]/a[2]/@href').extract()
        for url in next_selector:
            yield Request(urljoin(response.url, url))

        #Get item URLs and yield Requests
        story_selectors = response.xpath('//h2[@class="story"]')
        for selector in story_selectors:
            yield self.parse_item(selector, response)


    def parse_item(self, selector, response):
        #pass
        item = SlashdotItem()
        item['title'] = response.xpath('//span[@class="story-title"]/a/text()').extract()
        item['views'] = response.xpath('//span[@class="comment-bubble"]//a/text()').extract()
