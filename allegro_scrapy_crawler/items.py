# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field



class AllegroScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # Primary fields
    offer_title = Field()
    price = Field()
    date_of_sale = Field()
    
    #metadata
    url = Field()


    pass
