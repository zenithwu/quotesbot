# -*- coding: utf-8 -*-

import scrapy


class CCGPSpiderXPath(scrapy.Spider):
    name = 'ccgp-xpath'
    start_urls = [
        'http://www.ccgp.gov.cn/cggg/zygg/',
    ]
    offset=1;
    effect=True;

    def parse(self, response):
        for quote in response.xpath('//ul[@class="c_list_bid"]/li'):
            self.effect=True
            yield {
                'title': quote.xpath('./a/text()').extract_first(),
                'type': quote.xpath('./em[1]/text()').extract_first(),
                'time': quote.xpath('./em[2]/text()').extract_first(),
                'area': quote.xpath('./em[3]/text()').extract_first(),
                'author': quote.xpath('./em[4]/text()').extract_first()
            }

        # next_page_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if self.effect:
            self.offset += 1
            self.effect=False
            yield scrapy.Request(self.start_urls[0]+"index_%s.htm"%str(self.offset),callback=self.parse)

