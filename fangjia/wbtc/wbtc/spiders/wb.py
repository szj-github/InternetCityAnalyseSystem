# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
from fontTools.ttLib import TTFont
import base64
from io import BytesIO
import re
from wbtc.items import WbtcItem


class WbSpider(scrapy.Spider):
    name = 'wb'
    allowed_domains = ['58.com']
    start_urls = ['https://tongling.58.com/chuzu/?PGTID=0d0090a7-0000-0536-a09c-7040df96ca04&ClickID=1']
    def start_requests(self):
        sleep(2)
        #options = webdriver.Chrome()
        # 创建chrome参数对象
        options = webdriver.ChromeOptions()
         # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        options.set_headless()
        prefs={
        'profile.default_content_setting_values': {
        'images': 2,
        'javascript':2}
         }
        options.add_experimental_option('prefs',prefs)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://www.58.com/changecity.html?catepath=ershoufang&catename=%E4%BA%8C%E6%89%8B%E6%88%BF&fullpath=1,12&PGTID=0d30000c-0091-5ef7-eca1-15d6313f0e5f&ClickID=1")
        sl = driver.current_url
        lists=['乌鲁木齐', '呼和浩特', '嘉兴', '兰州', '中山', '海口']
        print(len(lists))
        for i in lists:
            driver.find_element_by_id("selector-search-input").send_keys(i)
            driver.find_element_by_id("selector-search-btn").click()
            sa = driver.current_url
            driver.back()
            yield scrapy.Request(url=sa,callback=self.parse,dont_filter=True)
        driver.quit()

    def parse(self, response):
       # print(response.text)
        mm=response.xpath("/html/body/div[5]/div[2]/dl[1]/dd//a/@href").extract()
        for x in mm:
            if re.match('/',x)is not None :
                if re.match('/ershoufang',x)is None:    
                    yield scrapy.Request(url='https://sz.58.com'+x,callback=self.parse_1,dont_filter=True)

    
#常熟#张家港

    def parse_1(self, response):
        item = WbtcItem()
        lists=response.xpath("/html/body/div[5]/div[5]/div[1]/ul/li")
        item['city']=str(response.xpath("/html/body/div[5]/div[1]/a[1]/text()").re('(.*)58')).replace('[', '').replace(']', '').replace('\'', '')+'-'+str(response.xpath("/html/body/div[5]/div[4]/a[2]/span/text()").re('(.*)二手房')).replace('[', '').replace(']', '').replace('\'', '')

        for x in lists:
            item['describe'] =x.xpath("./div[2]/h2/a/text()").extract_first().replace('\xa0', '').replace('[', '').replace(']', '').replace(',', '')
            item['area']=x.xpath("./div[2]/p[1]/span[2]/text()").extract_first().replace('[', '').replace(']', '').replace('\xa0', '')
            item['rent']=x.xpath("./div[3]/p[2]/text()").extract_first().replace('[', '').replace(']', '').replace('\xa0', '')
            yield item
        url=response.xpath("/html/body/div[5]/div[5]/div[1]/div[2]/a[@class='next']/@href").extract_first()
        print(url)
        if not url is None:
            yield scrapy.Request(url='https://sz.58.com'+url,callback=self.parse_1)
            

'''
       #print(response.text)
        base64_str = re.search("base64,(.*?)'\\)",response.text).group(1)
       # print(base64_str)
        b = base64.b64decode(base64_str)
        font = TTFont(BytesIO(b))
        bestcmap = font["cmap"].getBestCmap()
        newmap = dict()
        for key in bestcmap.keys():
            value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
            key = hex(key)
            newmap[key] = value
        print(newmap)
        response_ = response.text
        for key,value in newmap.items():
            key_ = key.replace('0x','&#x') + ';'
            if key_ in response_:
                response_ = response_.replace(key_,str(value))
        selector=scrapy.Selector(text=response_)
        #print(response_)
        item = WbtcItem()
        lists = selector.xpath("//ul[@class='house-list']//li[position() < last()]")
        print(len(lists))
        for i in lists:
            item['describe'] = str(i.xpath("./div[@class='des']//a[@class='strongbox']/text()").extract_first()).replace(' ', '').replace('[', '').replace(']', '').replace('\n', '')
            item['area'] = str(i.xpath(".//div[@class='des']//p[@class='room']").re('\\xa0\\xa0\\xa0\\xa0(.*)</p>')).replace('[', '').replace(']', '').replace('\'', '')
            item['rent'] = str(i.xpath(".//div[@class='list-li-right']//b/text()|.//div[@class='list-li-right']//div[@class='money']/text()").extract()).replace('\\n', '').replace(' ', '').replace('[', '').replace(']', '').replace('\'', '').replace(',', '')
            item['city'] = str(response.xpath("//*[@id='tab-default']/text()").re('(.*)出租')).replace('[', '').replace(']', '').replace('\'', '')
            yield item

            #print(area)
            #print(rent)
        pages = response.xpath("//ul[@class='house-list']//li[last()]//a[@class='next']/@href").extract_first()
        print(pages)
        if not pages is None:
            yield scrapy.Request(url=pages,callback=self.parse,dont_filter=True)'''