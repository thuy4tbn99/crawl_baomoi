import scrapy
import re
from ..items import BaomoiItem

class BaomoiSpiderSpider(scrapy.Spider):

    name = 'baomoi'
    page_number = 2
    allowed_domains = ['baomoi.com']
    start_urls = [
        'https://baomoi.com/'

    ]


    def parse(self, response):
        # các chủ đề thoisu.epi, ...
        all_topic = response.css('.nav .container :nth-child(1)').css('::attr(href)').extract()

        for topic in all_topic:
            topic = response.urljoin(topic)
            print("Topic:" + topic)
            yield scrapy.Request(topic, callback=self.crawlTopic)

    def crawlTopic(self, response):
        print("crawTopic note"+ response.request.url)
        # các bài báo cụ thể trong chủ đề /thoi-su.epi báo: 1234.epi, ...
        all_paper = response.css('.story__heading a').css('::attr(href)').extract()

        for index, paper in enumerate(all_paper):
            id_epi = re.findall('(\d+).epi', str(paper))[0] +'.epi'
            # print(id_epi)
            url = 'https://baomoi.com/a/c/' + id_epi
            # print(url)

            # debug limit loop
            # if index == 2:
            #     break
            yield scrapy.Request(url, callback=self.crawlPaper)

        next_page = response.css('.btn-primary::attr(href)').get()
        next_page = response.urljoin(next_page)
        page_number = int(re.findall('([a-z]+)(\d+)', next_page)[0][1])
        if next_page is not None and page_number < 31:
            yield scrapy.Request(next_page, callback=self.crawlTopic)

        # pass

    def crawlPaper(self, response):
        items = BaomoiItem()
        print('crawPaper note')
        id = re.findall('(\d+).epi', str(response.url))[0]
        category = response.css('.cate').css('::text').extract()
        time = response.css('.time').css('::text').extract()
        content = response.css('.body-text').css('::text').extract()
        header = response.css('.article__header').css('::text').extract()
        keyword = response.css('.keyword').css('::text').extract()

        items['id'] = id
        items['time'] = time
        items['category'] = category
        items['content'] = content
        items['header'] = header
        items['keyword'] = keyword

        # print(str(items['id']))

        yield items






