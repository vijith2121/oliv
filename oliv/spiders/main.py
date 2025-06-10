import scrapy
# from oliv.items import Product
from lxml import html

class OlivSpider(scrapy.Spider):
    name = "oliv"
    start_urls = ["https://example.com"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        print("Visited:", response.url)
