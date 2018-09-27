# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest
from slashdot.items import SlashdotItem


class EasySpider(CrawlSpider):
    name = 'login'
    allowed_domains = ['slashdot.org']

    def start_requests(self):
        return [FormRequest("https://slashdot.org/my/login", formdata={"op": "userlogin", "returnto": "", "unickname": "<username>", "upasswd": "<passwd>", "userlogin": "Log+In"})]

    start_urls = start_requests

    rules = (
        #Rule to crawl through the various pages(pagination rules)
        Rule(LinkExtractor(restrict_xpaths='//div[@id="fh-paginate"]/a[2]')),
        #Rule to crawl into the various story titles and retrieve the required information
        Rule(LinkExtractor(restrict_xpaths='//span[@class="story-title"]/a'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = SlashdotItem()
        item['title'] = response.xpath('//h2[@class="story"]/span[@class="story-title"]/a/text()').extract()
        item['views'] = response.xpath('//span[@class="comment-bubble"]//a/text()').extract()
        return item
