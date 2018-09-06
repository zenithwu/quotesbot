from scrapy import cmdline


name = 'ccgp-xpath'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())