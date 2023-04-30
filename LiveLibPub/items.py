# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Card(scrapy.Item):
    
    name = scrapy.Field()
    books = scrapy.Field()
    description = scrapy.Field()
    city = scrapy.Field()
    lastChange = scrapy.Field()
    url = scrapy.Field()
    urlBook = scrapy.Field()
    siteUrl = scrapy.Field()

class Book(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    genre = scrapy.Field()
    publisher = scrapy.Field()
    
