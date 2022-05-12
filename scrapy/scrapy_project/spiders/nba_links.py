# -*- coding: utf-8 -*-
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

# Second spider fetches links to sites with particular players
class LinksSpider(scrapy.Spider):
    name = 'nba_players_links'
    allowed_domains = ['basketball-reference.com/']
    try:
        with open("list_of_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
    def parse(self, response):
        print(response)
        xpath = './/tbody/tr/th//a[re:test(@href, "\/players\/[a-zA-Z]\/[a-zA-Z\d]*.html*")]//@href'
        # reading only 20 first records
        selection = response.xpath(xpath)[0:20]
        for s in selection:
            l = Link()
            l['link'] ='https://www.basketball-reference.com' + s.get()
            print(l)
            yield l
