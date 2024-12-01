import math

import scrapy

from ..utils import to_number_string

BASE_URL = "https://online.metro-cc.ru/"
ITEMS_PER_PAGE = 30

# 10 - id Московского магазина
# 15 - id Питерского магазина
STORE_ID = ['10', '11', '12', '15']


class Spider(scrapy.Spider):
    name = "metro_news_spider"

    def start_requests(self):

        cookies_list = [
            {"metroStoreId": i} for i in STORE_ID
        ]

        start_url = f"{BASE_URL}category/sladosti_/konfety-podarochnye-nabory?page=1&in_stock=1"

        for cookies in cookies_list:
            yield scrapy.Request(
                url=start_url,
                cookies=cookies,
                callback=self.parse_first,
                dont_filter=True
            )

    def parse_first(self, response):
        products_count = int(to_number_string(response.css('.heading-products-count::text').get()))
        print("product count:", products_count)
        page_count = math.ceil(products_count / ITEMS_PER_PAGE)
        urls = [f"{BASE_URL}category/sladosti_/konfety-podarochnye-nabory?page={i}&in_stock=1" for i in range(1, page_count)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        products_links = response.css('#products-wrapper a::attr(href)').getall()
        yield from response.follow_all(products_links, self.parse_item)

    def parse_item(self, response):

        def extract_with_css(query: str) -> str:
            """
            Функция принимает селектор в виде строки и применяет его ко всему документу,
            возвращая "" если селектор ничего не нашел
            :param query:
            :return: "" или найденный элемент
            """

            return response.css(query).get(default="").strip()

        # Парсинг цен
        regular_cost = to_number_string(extract_with_css('.product-unit-prices__old-wrapper .product-price__sum-rubles::text'))
        if regular_cost == "":
            regular_cost = to_number_string(extract_with_css('.product-price__sum-rubles::text'))
            promo_cost = ""
        else:
            promo_cost = to_number_string(extract_with_css('.product-price__sum-rubles::text'))

        yield {
            "id": to_number_string(extract_with_css('.product-page-content__article::text')),
            "title": extract_with_css('.product-page-content__product-name ::text'),
            "ref": response.url,
            "regular_cost": regular_cost,
            "promo_cost": promo_cost,
            "brand": extract_with_css('.product-attributes__list-item:first-child .product-attributes__list-item-links a::text')
        }
