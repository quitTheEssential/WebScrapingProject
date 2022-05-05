# -*- coding: utf-8 -*-
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'nba_players_links'
    allowed_domains = ['basketball-reference.com/']
    try:
        with open("list_of_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
    #start_urls = ['https://www.basketball-reference.com/players/a/']
    def parse(self, response):
        print(response)
        xpath = '//a[re:test(@href, "\/players\/[a-zA-Z]\/[a-zA-Z\d]*.html*")]//@href'
        selection = response.xpath(xpath)[0:20]
        for s in selection:
            l = Link()
            l['link'] ='https://www.basketball-reference.com' + s.get()
            print(l)
            yield l
