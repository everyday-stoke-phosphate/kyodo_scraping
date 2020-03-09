# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # 設定の変更 基本的にsetting.pyに記述
    # 特に何か変えるときには設定内容を指定
    settings = get_project_settings()  # FEED_URI='results.json')
    process = CrawlerProcess(settings)
    spider_name = "kyodo_articles_scraping"
    process.crawl(spider_name)
    process.start()
