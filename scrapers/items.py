import scrapy


class ProductItem(scrapy.Item):
    store = scrapy.Field()
    barcodes = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    package = scrapy.Field()
    image_url = scrapy.Field()
    branch = scrapy.Field()
    stock = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
