# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mentalfloss.items import MentalflossItem


class MentalflossCrawlerSpider(CrawlSpider):
    name = 'mentalfloss_crawler'
    allowed_domains = ['mentalfloss.com']
    start_urls = ['http://www.mentalfloss.com/big-questions']

    rules = (
        Rule(LinkExtractor(allow=r'load_more/get_page/big_questions\?page=[0-9]'), 
            callback='parse', 
            follow=True),
    )

    def parse(self, response):
        datas = response.xpath('//header/hgroup/h1/a/@href')

        for url in datas:
            full_url = response.urljoin(url.extract())
            yield Request(full_url, callback=self.parse_item)           


    def parse_item(self, response):
        item = MentalflossItem()
        item['title'] = response.xpath('//h1[@class="title"]/span/text()').extract()
        item['url'] = response.url
        item['author'] = response.xpath('//div[@class="field-item even"]/a/text()').extract()[0]
        item['content'] = "\n ".join(response.css('#content-content p::text').extract())
        # item['content'] = response.xpath('//div[@class="field-item even"]/p/text()').extract()
        item['date'] = response.xpath('//span[@class="date-display-single"]/text()').extract()

        yield item

        # i = MentalflossItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i

    # def parse_data(self, response):
    #     item = MentalflossItem()
    #     item['title'] = response.xpath('//h1[@class="title"]/span/text()').extract()
    #     item['link'] = response.url
    #     item['author'] = response.xpath('//div[@class="field-item even"]/a/text()').extract()[0]
    #     item['content'] = "\n ".join(response.css('#content-content p::text').extract())
    #     # item['content'] = response.xpath('//div[@class="field-item even"]/p/text()').extract()
    #     item['date'] = response.xpath('//span[@class="date-display-single"]/text()').extract()

    #     yield item
    #     print "==================================\n"