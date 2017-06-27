from scrapy.spider import Spider
from scrapy import Request
from appspider.items import AppspiderItem


class AppSpider(Spider):
    name = 'wandoujia'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://www.wandoujia.com/apps'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        parents = response.xpath('//ul[@class="app-popup tag-popup clearfix"]/li')
        for parent in parents:
            children = parent.xpath('./ul/li')
            for child in children:
                url = child.xpath('./a/@href').extract()[0]
                yield Request(url, headers=self.headers, callback=self.parse_app)

    def parse_app(self, response):
        items = AppspiderItem()
        secCatStr = response.xpath('//li[@class="current"]/strong/a/text()').extract()
        firCatStr = response.xpath('//div[@class="third"]/a/text()').extract()
        apps = response.xpath('//h2[@class="app-title-h2"]/a')
        for app in apps:
            items['appName']=app.xpath('./text()').extract()
            items['secondCat']=secCatStr
            items['firstCat']=firCatStr
            yield items

        next_url = response.xpath('//a[@class="page-item next-page "]/@href').extract()[0]
        print(next_url)
        if next_url:
            yield Request(next_url, headers=self.headers, callback=self.parse_app)