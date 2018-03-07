# coding=utf-8
import scrapy
import time
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule

from lianjiaspider.items import Home


class LianjiaSpider(scrapy.Spider):
    name = 'Lianjiaspider'

    # 上海按地区筛选所要加的路径
    areas = ['pudong', 'minhang', 'baoshan', 'xuhui', 'putuo', 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu', 'jingan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian']
    ranges = ['rp1', 'rp2', 'rp3', 'rp4', 'rp5', 'rp6', 'rp7'] # 用价格筛选条件 需要添加的路径

    def start_requests(self):
        for area in self.areas:
            for rangePrice in self.ranges:
                url = "https://sh.lianjia.com/zufang/"+area+"/"+rangePrice+"/"
                yield scrapy.Request(url, meta = {'area': area, 'rangePrice' : rangePrice}, callback = self.getPage)

    # 获取此次筛选条件下，网页显示数据的页数
    def getPage(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tag = soup.find(attrs={"class" : "page-box house-lst-page-box"})
        if(tag is not None) :
            pageData = eval(tag['page-data'])
            pageCount = pageData['totalPage']

            area = response.meta['area']
            rangePrice = response.meta['rangePrice']

            i = 1
            while i < pageCount:
                url = url = "https://sh.lianjia.com/zufang/" + area + "/" + "pg" + str(i) + rangePrice + "/"
                yield scrapy.Request(url, self.getDetailPage)
                i += 1

    # 获取房屋信息的详细页
    def getDetailPage(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        nextUrls = soup.find_all(attrs={"class": "info-panel"})
        for nexturl in nextUrls:
            yield Request(nexturl.h2.a["href"],callback=self.parse_res)

    # 提取数据并放入数据库
    def parse_res(self,response):
        select = scrapy.Selector(response)
        home = Home(title = select.css('body > div:nth-child(7) > div.title-wrapper > div > div.title > h1::text').extract_first()
                    ,price = select.css('body > div:nth-child(7) > div.overview > div.content.zf-content > div.price > span.total::text').extract_first()
                    ,tip_decoration = select.css('body > div:nth-child(7) > div.overview > div.content.zf-content > div.price > span.tips.decoration::text').extract_first()
                    ,size = select.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[1]/text()').extract_first()
                    ,type = select.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[2]/text()').extract_first()
                    ,level = select.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[3]/text()').extract_first()
                    ,face = select.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[4]/text()').extract_first()
                    ,underground = select.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[5]/text()').extract_first()
                    ,housingEstate = select.css('body > div:nth-child(7) > div.overview > div.content.zf-content > div.zf-room > p:nth-child(7) > a:nth-child(2)::text').extract_first()
                    ,location = select.css('body > div:nth-child(7) > div.overview > div.content.zf-content > div.zf-room > p:nth-child(8) > a:nth-child(2)::text').extract_first() + ' ' + select.css('body > div:nth-child(7) > div.overview > div.content.zf-content > div.zf-room > p:nth-child(8) > a:nth-child(3)::text').extract_first())

        yield home
