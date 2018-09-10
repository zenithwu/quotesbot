# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import urllib2


class QuotesbotPipeline(object):
    def process_item(self, item, spider):
        return item


class DownLoadImgPipeline(object):
    count = 0

    def process_item(self, item, spider):
        for tag,url in item['urls']:
            cont = urllib2.urlopen(url).read()
            patter = '[0-9]*\.jpg';
            match = re.search(patter, url);
            if match:
                print '正在下载文件：', match.group()
                filename = os.path.join(spider.localSavePath,tag,match.group())
                f = open(filename, 'wb')
                f.write(cont)
                f.close()
                self.count = self.count + 1
            else:
                print 'no match'

        return item

    def close_spider(self, spider):
        print(self.count)
