# -*- coding: utf-8 -*-
import scrapy

limit_to_100 = True
if limit_to_100:
    limiter = 101
else:
    limiter = -1


class Player(scrapy.Item):
    nameAndSurname        = scrapy.Field()
    games                 = scrapy.Field()
    points                = scrapy.Field()
    rebounds              = scrapy.Field()
    assists               = scrapy.Field()
    fieldGoalPercentage   = scrapy.Field()
    threeFieldGoal        = scrapy.Field()
    freeThrowPercentage   = scrapy.Field()
    effectiveFieldGoal    = scrapy.Field()
    playerEfficiency      = scrapy.Field()
    winShares             = scrapy.Field()




class LinksSpider(scrapy.Spider):
    name = 'players'
    allowed_domains = ['basketball-reference.com/']
    try:
        with open("players_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:limiter]
    except:
        start_urls = []
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["nameAndSurname", "games", "points", "rebounds", "assists", "fieldGoalPercentage",
                               "threeFieldGoal", "freeThrowPercentage", "effectiveFieldGoal", "playerEfficiency",
                               "winShares"],

    }

    def parse(self, response):
        p = Player()

        name_xpath          = '//h1/span/text()'
        games_xpath         = '//div[span[@data-tip="Games"]]/p[2]/text()'
        points_xpath        = '//*[@data-tip="Points"]/following-sibling::p[2]/text()'
        totalRebounds_xpath = '//*[@data-tip="Total Rebounds"]/following-sibling::p[2]/text()'
        assists             = '//*[@data-tip="Assists"]/following-sibling::p[2]/text()'
        fieldGoalPercentage = '//*[@data-tip="Field Goal Percentage"]/following-sibling::p[2]/text()'
        threeFieldGoal      = '//*[@data-tip="3-Point Field Goal Percentage"]/following-sibling::p[2]/text()'
        freeThrowPercentage = '//*[@data-tip="Free Throw Percentage"]/following-sibling::p[2]/text()'
        effectiveFieldGoal  = '//*[contains(@data-tip, "Effective Field Goal Percentage")]/following-sibling::p[2]/text()'
        playerEfficiency    = '//*[contains(@data-tip, "Player Efficiency Rating")]/following-sibling::p[2]/text()'
        winShares           = '//*[contains(@data-tip, "Win Shares")]/following-sibling::p[2]/text()'


        p['nameAndSurname']        = response.xpath(name_xpath).getall()
        p['games']                 = response.xpath(games_xpath).getall()
        p['points']                = response.xpath(points_xpath).getall()
        p['rebounds']              = response.xpath(totalRebounds_xpath).getall()
        p['assists']               = response.xpath(assists).getall()
        p['fieldGoalPercentage']   = response.xpath(fieldGoalPercentage).getall()
        p['threeFieldGoal']        = response.xpath(threeFieldGoal).getall()
        p['freeThrowPercentage']   = response.xpath(freeThrowPercentage).getall()
        p['effectiveFieldGoal']    = response.xpath(effectiveFieldGoal).getall()
        p['playerEfficiency']      = response.xpath(playerEfficiency).getall()
        p['winShares']             = response.xpath(winShares).getall()

        yield p
