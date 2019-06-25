import scrapy
from scrapy.http.response.text import TextResponse

from scrapy_lianjia_ershoufang.items import ScrapyLianjiaErshoufangItem


class ErshoufangSpider(scrapy.Spider):
    name = 'ErshoufangSpider'

    def start_requests(self):
        city = getattr(self, 'city', 'sz')
        self.allowed_domains = ['%s.lianjia.com' % city]
        urls = ['https://%s.lianjia.com/ershoufang/pg%d/' % (city, i)
                for i in range(1, 101)]
        for url in urls:
            yield scrapy.Request(url, self.parse, headers={'Referer': url})

    def parse(self, response: TextResponse):
        items = response.css('ul.sellListContent li')
        for li in items:
            '''
            title = scrapy.Field()
            room = scrapy.Field()
            area = scrapy.Field()
            orientation = scrapy.Field()
            elevator = scrapy.Field()
            location = scrapy.Field()
            flood = scrapy.Field()
            follow_number = scrapy.Field()
            look_number = scrapy.Field()
            pub_duration = scrapy.Field()
            total_price = scrapy.Field()
            unit_price = scrapy.Field()
            '''
            item = ScrapyLianjiaErshoufangItem()
            item['title'] = li.css('div.title a::text').get()
            house_infos = li.css('div.address .houseInfo::text').re(
                r'\|\s+(.*)\s+\|\s+(.*)平米\s+\|\s+(.*)\s+\|\s+(.*)\s+\|\s+(.*)')
            item['room'] = house_infos[0]
            item['area'] = house_infos[1]
            item['orientation'] = house_infos[2]
            item['decoration'] = house_infos[3]
            item['elevator'] = house_infos[4]
            item['xiaoqu'] = li.css('div.address a::text').get()
            item['flood'] = li.css('div.flood .positionInfo::text').get().replace('-', '').strip()
            item['location'] = li.css('div.flood .positionInfo a::text').get()
            follow_infos = li.css('div.followInfo::text').re(r'(.*)人关注\s+/\s+共(.*)次带看\s+/\s+(.*)发布')
            item['follow_number'] = follow_infos[0]
            item['look_number'] = follow_infos[1]
            item['pub_duration'] = follow_infos[2]
            item['total_price'] = li.css('div.priceInfo div.totalPrice span::text').get()
            item['unit_price'] = li.css('div.priceInfo .unitPrice span::text').get()
            item['unit'] = li.css('div.totalPrice::text').get()
            yield item