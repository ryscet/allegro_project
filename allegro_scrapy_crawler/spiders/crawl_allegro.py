# -*- coding: utf-8 -*-

import scrapy
from unidecode import unidecode

from allegro_scrapy.items import  AllegroScrapyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class AllegroCrawl(scrapy.Spider):
    """Crawls history of allegro sales and retrieves information from the index pages. 
    This information includes the date of sale and price of a macbook. 
    Also it contains a title of the auction, but this will not be used."""

    name = 'allegro_crawl'
    allowed_domains = ['web']

    # List of index pages, spanning back in history. First index are the most recently closed auctions.
    n_pages = 1000
    start_urls = ['http://archiwum.allegro.pl/szukaj/macbook%20pro%2015' + '/' + str(i) for i in range(1,n_pages)]

    def parse(self, response):

        l = ItemLoader(item = AllegroScrapyItem(), response = response)
        # Find the price identified by the offer belonging to the laptopy category (because the searching for macbook pro also returns accessories)
        l.add_xpath('price', '//a[contains(@href, "laptopy")]/../following-sibling::div[@class = "price"]/p[@class = "price-value"]/node()[1]',
            MapCompose(unicode.strip,
                       lambda i: i.replace(',', '.'),
                       lambda i: i.replace(' ', ''),
                       float
                       ))
        #Find their date of sale
        l.add_xpath('date_of_sale','//a[contains(@href, "laptopy")]/../following-sibling::div[@class = "end"]/text()',
            MapCompose(unicode.strip, 
                        unidecode, #converts unicode foreign characters like u015 to closest ascii 
                        format_date # convert long format, 'zakonczona 11 wrzesnia o 11.30'
                        ))#
        #Find the auction title
        l.add_xpath('offer_title','//a[contains(@href, "laptopy")]/../preceding-sibling::h4//span[@itemprop = "name"]/text()',
            MapCompose(unicode.strip, 
                        unidecode, #converts unicode foreign characters like u015 to closest ascii 
                        ))

        # metadata
        l.add_value('url', response.url)

        return l.load_item()

def format_date(long_form):
    """Parses the date paragraph into a string easy to parse into datetime object"""
    month_list=['stycznia',
                'lutego',
                'marca',
                'kwietnia',
                'maja',
                'czerwca',
                'lipca',
                'sierpnia',
                'wrzesnia',
                'pazdziernika',
                'listopada',
                'grudnia' 
                ]

    date_parts = long_form.split()

    year = date_parts[3]
    month = str(month_list.index(date_parts[2])+1).zfill(2) # + 1 because index of 'stycznia' is 0. .zfill(2) single month indices to zero padded.
    day = date_parts[1]

    
    return ('%s/%s/%s') % (year, month, day) 

 
    