# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MentalflossItem(Item):
    # define the fields for your item here like:
    title = Field()
    content = Field()
    url = Field()
    author = Field()
    date = Field()