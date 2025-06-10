import scrapy

class Product(scrapy.Item):
    scrape_date = scrapy.Field()
    data = scrapy.Field()
