# -*- coding: utf-8 -*-


from scrapy import cmdline


name = 'wandoujia'
cmd = 'scrapy crawl {0} -o wdj.csv'.format(name)
cmdline.execute(cmd.split())