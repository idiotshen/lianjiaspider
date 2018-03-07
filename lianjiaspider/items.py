# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Home(scrapy.Item) :
    title = scrapy.Field()
    price = scrapy.Field()
    tip_decoration = scrapy.Field()
    size = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    face = scrapy.Field()
    underground = scrapy.Field()
    housingEstate = scrapy.Field()
    location = scrapy.Field()
