# -*- coding: utf-8 -*-

import scrapy


class KyodoArticlesScrapingSpider(scrapy.Spider):
    name = 'kyodo_articles_scraping'
    allowed_domains = ['this.kiji.is']
    start_urls = [
        # 'https://this.kiji.is/607729369421317217'
    ]

    def start_requests(self):
        with open('starts_urls.txt') as urls:
            for url in urls:
                # urlは文字列で渡す
                yield scrapy.Request(url)

    def parse(self, response):
        root_xpath = response.xpath(
            '/html/body[@class=\'page\']/div[@class=\'page__wrapper\']/'
            'div[@class=\'page__contentsWrapper page__contentsWrapper--detail\']/div[@class=\'main\']')

        for KyodoArticlesItem in root_xpath:
            # root_xpath = response.xpath(
            #     "/html/body[@class='page']/div[@class='page__wrapper']/"
            #     "div[@class='page__contentsWrapper page__contentsWrapper--detail']/"
            #     "div[@class='main']/")
            yield {"text": response.xpath('//*[@id="js-detailBody"]/'
                                          'div[1]/article/p/text()').extract(),
                   "label": response.xpath(
                       "/html/body/div[1]/div[2]/div/div[4]/div/div[2]/div/div[2]/ul/li/a/p/text()").extract(),
                   "url": response.xpath("/html/head/link[@rel ='canonical']/@href").extract()
                   }

        pass
