# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
import scrapy


class BaijiacommItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content_id = Field()
    nickname = Field()
    cover = Field()
    comment = Field()
    comment_time = Field()
    pid = Field()
    source_id = Field()