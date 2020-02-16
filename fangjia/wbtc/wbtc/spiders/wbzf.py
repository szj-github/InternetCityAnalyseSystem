# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
from fontTools.ttLib import TTFont
import base64
from io import BytesIO
import re
from wbtc.items import WbtcItem


class WbzfSpider(scrapy.Spider):
    name = 'wbzf'
    allowed_domains = ['58.com']
    start_urls = ['http://58.com/']
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
        driver.get("https://www.58.com/changecity.html?catepath=chuzu&catename=%E5%87%BA%E7%A7%9F&fullpath=1,37031&PGTID=0d3090a7-0047-b370-9a23-5b295d0867b1&ClickID=2")
        sl = driver.current_url
        lists=['北京']
        print(len(lists))
        for i in lists:
            driver.find_element_by_id("selector-search-input").send_keys(i)
            driver.find_element_by_id("selector-search-btn").click()
            sa = driver.current_url
            driver.back()
            yield scrapy.Request(url=sa,callback=self.parse,dont_filter=True)
        driver.quit()

    def parse(self, response):
        #print(response.text)
        mm=response.xpath("//div[@class='search_bd']//dl[@class='secitem secitem_fist']/dd/a[position()>1]/@href").extract()
        #print(mm)
        for x in mm: 
            print(x)  
            yield scrapy.Request(url=x,callback=self.parse_1,dont_filter=True)
    def parse_1(self, response):
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
        item = WbtcItem()
       #print(response_)
        #print(selector.text)
        lists=selector.xpath("//ul[@class='house-list']//li[position() < last()]")
        city=str(selector.xpath("//div[@class='nav-top-bar']/a[1]/text()").re("(.*)58")).replace('[', '').replace(']', '').replace('\'', '')+'-'+str(selector.xpath("//div[@class='nav-top-bar']/a[4]/text()").re("(.*)出租")).replace('[', '').replace(']', '').replace('\'', '')
        #print(lists)
        for x in lists:
           #print(x)
            item['describe'] = x.xpath("./div[2]/h2/a/text()").extract_first().replace(' ', '').replace('\n', '')
            item['area'] = str(x.xpath("./div[2]/p[1]/text()").re('\xa0\xa0\xa0\xa0(.*)')).replace('[', '').replace(']', '').replace('\'', '')
            item['rent'] = x.xpath("./div[3]/div[2]/b/text()").extract_first().replace(' ', '').replace(' ', '')
            item['city']=city
            #print(item)
            yield item

        pages = response.xpath("//ul[@class='house-list']//li[last()]//a[@class='next']/@href").extract_first()
        print(pages)
        if not pages is None:
            yield scrapy.Request(url=pages,callback=self.parse_1,dont_filter=True)
