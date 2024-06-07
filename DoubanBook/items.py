# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBookItem(scrapy.Item):
    # define the fields for your item here like:
    bookname = scrapy.Field()
    author=scrapy.Field()
    image_urls =scrapy.Field()
    