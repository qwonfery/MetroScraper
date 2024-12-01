BOT_NAME = "metro_scraper"

SPIDER_MODULES = ["metro_scraper.spiders"]
NEWSPIDER_MODULE = "metro_scraper.spiders"

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 ' \
             'Safari/537.36 OPR/45.0.2552.888 '
# USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1
# Safari/537.1"


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   "metro_scraper.pipelines.MetroScraperPipeline": 300,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    'news.json': {'format': 'json', 'overwrite': True}
}
