from scrapy import cmdline


name = 'desktop-zol'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())