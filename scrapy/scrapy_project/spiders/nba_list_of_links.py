# -*- coding: utf-8 -*-
import scrapy


class Link(scrapy.Item):
    link = scrapy.Field()

# First spider fetches links to sites with particular letters
class LinkListsSpider(scrapy.Spider):
    name = 'nba_list_of_links'
    allowed_domains = ['basketball-reference.com/']
    start_urls = ['https://www.basketball-reference.com/players/?fbclid=IwAR01kEpJn6XeQOktXLatdBpYeginzTlMfdozcoVM3LkJqwEbXe3AGSMYEP0']

    def parse(self, response):
        xpath = '//a[re:test(@href, "/players/[a-z]/$")]//@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.basketball-reference.com' + s.get()
            yield l
