import re

import scrapy

BASE_URL = "https://online.metro-cc.ru/"
PAGE_NUMBER = 20


class Spider(scrapy.Spider):
    name = "metro_news_spider"
    start_urls = [f"{BASE_URL}category/sladosti_/konfety-podarochnye-nabory?page={i}&in_stock=1" for i in range(1, 2)]

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

        def to_number_string(cost_string: str) -> str:

            """
            Функция заменяет все нецифровые символы в строке на ""
            :param cost_string:
            :return: обработанная строка
            """

            return re.sub(r'\D', '', cost_string)

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
