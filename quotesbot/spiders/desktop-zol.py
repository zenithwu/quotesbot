# -*- coding: utf-8 -*-
import os
from urlparse import urljoin

import scrapy

from quotesbot.items import ImgItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'desktop-zol'
    start_urls = [
        'http://desk.zol.com.cn/',
    ]
    localSavePath = "/Users/zenith/data/"
    count = 0

    if not os.path.isdir(localSavePath):
        os.makedirs(localSavePath)

    def parse(self, response):
        for type_url in response.xpath('//div[@id="main"]/dl[1]/dd[1]/a'):
            t = type_url.xpath("@href").extract_first()
            if not t == '/pc/':
                t_name = str(t).replace("/", "")
                if not os.path.isdir(os.path.join(self.localSavePath, t_name)):
                    os.makedirs(os.path.join(self.localSavePath, t_name))
                yield scrapy.Request(url=response.urljoin(t), meta={"t_name": t_name}, callback=self.parse_type)

    def parse_type(self, response):

        t_name = response.meta['t_name']
        for pic_url in response.xpath('//a[@class="pic"]'):
            pic_url_full = urljoin(self.start_urls[0], pic_url.xpath("@href").extract_first())
            self.count = self.count + 1
            yield scrapy.Request(response.urljoin(pic_url_full), meta={"t_name": t_name}, callback=self.parse_pic)

        next_page_url = response.xpath('//a[@id="pageNext"]/@href').extract_first()
        if next_page_url is not None:
            # print(urljoin(self.start_urls[0],next_page_url))
            yield scrapy.Request(urljoin(self.start_urls[0], next_page_url), meta={"t_name": t_name},
                                 callback=self.parse_type)

    def parse_pic(self, response):
        urls = []
        t_name = response.meta['t_name']
        for img_url in response.xpath('//ul[@id="showImg"]/li/a[1]/img[1]'):
            img_url_full = str(
                img_url.xpath("@src | @srcs").extract_first())  # .replace("t_s144x90c5","t_s2880x1800c5")
            urls.append((t_name,img_url_full))
        item = ImgItem()
        item['urls'] = urls
        return item
