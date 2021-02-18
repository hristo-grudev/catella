import scrapy

from scrapy.loader import ItemLoader
from ..items import CatellaItem
from itemloaders.processors import TakeFirst


class CatellaSpider(scrapy.Spider):
	name = 'catella'
	start_urls = ['https://www.catella.com/en/newsroom/news-and-pressreleases']

	def parse(self, response):
		post_links = response.xpath('//div[@class="articlelist-item pure-box"]')
		for post in post_links:
			url = post.xpath('.//h2[@class="articlelist-heading"]/a/@href').get()
			date = post.xpath('.//div[@class="date"]/text()').get().split('|')[0]
			yield response.follow(url, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="pure-g"]//text()[normalize-space() and not(ancestor::a)]|//div[@class="informationblock-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=CatellaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
