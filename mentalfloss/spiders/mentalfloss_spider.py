from scrapy import Spider, Request
from scrapy.selector import Selector

from mentalfloss.items import MentalflossItem


class MentalflossSpider(Spider):
	name = "mentalfloss"
	allowed_domains = ["mentalfloss.com"]
	start_urls = [
		"http://mentalfloss.com/big-questions"
	]

	def parse(self, response):
		datas = Selector(response).xpath('//header/hgroup/h1/a/@href')

		for url in datas:
			full_url = response.urljoin(url.extract())
			yield Request(full_url, callback=self.parse_data)			

	def parse_data(self, response):
		item = MentalflossItem()
		item['title'] = response.xpath('//h1[@class="title"]/span/text()').extract()
		item['url'] = response.url
		item['author'] = response.xpath('//div[@class="field-item even"]/a/text()').extract()[0]
		item['content'] = "\n ".join(response.css('#content-content p::text').extract())
		# item['content'] = response.xpath('//div[@class="field-item even"]/p/text()').extract()
		item['date'] = response.xpath('//span[@class="date-display-single"]/text()').extract()

		yield item
		print "==================================\n"

