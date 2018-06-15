# -*- coding: utf-8 -*-
import scrapy

class BricksetSpider(scrapy.Spider):
    name = 'brickset'
    allowed_domains = ['brickset.com']
    start_urls = ['https://brickset.com/sets/year-2016']

    def parse(self, response):
        for brickset in response.css("article.set"):
            meta = brickset.css("div.meta")
            # セット番号、セット名、画像URL、テーマ、発売年等の情報を取得
            number = meta.css("h1 span::text").re_first(r'(.+): ')
            name = brickset.css("div.highslide-caption h1::text").extract_first()
            image = brickset.css("img::attr(src)").re_first('(.*)\?')
            theme = meta.css(".tags a")[1].css("a::text").extract_first()
            subtheme = meta.css(".tags a.subtheme::text").extract_first()
            year = meta.css("a.year::text").extract_first()
            rating = meta.css(".rating::attr(title)").extract_first()
            owner = brickset.css("dl.admin dd").re_first("(\d+) own this set")
            want_it = brickset.css("dl.admin dd").re_first("(\d+) want it")
            pieces = meta.xpath(".//dt[text()='Pieces']/following-sibling::dd").css("::text").extract_first()
            minifigs = meta.xpath(".//dt[text()='Minifigs']/following-sibling::dd").css("::text").extract_first()
            price = meta.xpath(".//dt[text()='RRP']/following-sibling::dd/text()")
            us_price = price.re_first("\$(\d+\.\d+)")
            eu_price = price.re_first("(\d+\.\d+)€")

            yield{
                "number": number, "name": name, "image": image, "theme": theme, "subtheme": subtheme,
                "year": year, "rating": rating, "owner": owner, "want_it": want_it,
                "pieces": pieces, "minifigs": minifigs, "us_price": us_price, "eu_price": eu_price,
            }
        # 次のページを取得する
        next_url = response.css('li.next a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url)


