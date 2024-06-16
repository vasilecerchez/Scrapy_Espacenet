import scrapy
import pandas as pd
from scrapy_playwright.page import PageMethod
from espacenet.items import EspacenetItem
from scrapy.loader import ItemLoader


class SpiderEspacenetSpider(scrapy.Spider):
    name = "spider_espacenet"
    allowed_domains = ["worldwide.espacenet.com"]
    #start_urls = ["https://worldwide.espacenet.com/patent/search/family/047528706/publication/US2015192928A1?q=US201314417435A"]
    def start_requests(self):
        #df=pd.read_excel('/home/vasile/incontro_6_wsl/espacenet/espacenet/spiders/mini_proj_con_brevetti.xlsx')
        df=pd.read_excel('/home/vasile/incontro_6_wsl/espacenet/espacenet/spiders/proj_con_brevetti.xlsx')
        #urls=df['epoPubUrl']
        #for i in urls:
        for index, row in df.iterrows():
            #url=row["epoPubUrl"]
            url=row["epoAppUrl"]
            id_project=row["projectID"]
            yield scrapy.Request(url=url, meta={
                "playwright":True,
                "playwright_page_methods":[
                    #PageMethod("wait_for_load_state","domcontentloaded")
                     #PageMethod("wait_for_timeout",8000)
                     PageMethod("wait_for_selector",'//h5[@id="biblio-title-content"]'),
                     PageMethod("wait_for_selector",'//div[@id="biblio-abstract-content"]')
                    ]},
                
                cb_kwargs={'id_project':id_project},
                 dont_filter=True
                    
                    )

    def parse(self, response,id_project):
        item=ItemLoader(item=EspacenetItem(), response=response, selector=response)#response=response,
        #  item.add_xpath("titolo","//h1/text()")
        item.add_xpath("titolo_brevetto",'//h5[@id="biblio-title-content"]/text()')
        item.add_value("link_brevetto",response.url)
        item.add_value("id_project",id_project)
        item.add_xpath("lingua_descrizione",'//div[contains(@class,"language-set")]/button/span//text()')
        item.add_xpath("applicants",'//h5[contains(text(),"Applicants")]/../div//span[@id="biblio-applicants-content"]//text()')
        item.add_xpath("inventors",'//h5[contains(text(),"Inventors")]/../div/span[@id="biblio-inventors-content"]//text()')
        item.add_xpath("classifications_ipc",'//h5[contains(text(),"Classifications")]/../div[1]//text()')
        item.add_xpath("classifications_cpc",'//h5[contains(text(),"Classifications")]/../div[2]//text()')
        
        item.add_xpath("priorities",'//h5[contains(text(),"Priorities")]/../div/div//a//text()[normalize-space()]')
        item.add_xpath("application",'//h5[contains(text(),"Application")]/../span//text()')
        item.add_xpath("publication",'//h5[contains(text(),"Publication")]/../span//text()')
        item.add_xpath("published_as",'//h5[contains(text(),"Published")]/../span//text()')
        #item.add_xpath("abstract",'//h5[contains(text(),"Abstract")]/../div[contains(@class,"abstract__text")]//text()')
        item.add_xpath("abstract",'//h5[contains(text(),"Abstract")]/../div[contains(@class,"abstract__text") and contains(@id,"abstract")]//text()')
        
        yield item.load_item()

        
        #titolo_brevetto=response.xpath('//h5[@id="biblio-title-content"]/text()').getall()
        #applicants=response.xpath('//h5[contains(text(),"Applicants")]/../div//span[@id="biblio-applicants-content"]//text()').getall()
        #inventors=response.xpath('//h5[contains(text(),"Inventors")]/../div/span[@id="biblio-inventors-content"]//text()').getall()
        #classifications=response.xpath('//h5[contains(text(),"Classifications")]/../div/div//text()').getall()
        #priorities=response.xpath('//h5[contains(text(),"Priorities")]/../div/div//a//text()[normalize-space()]').getall()
        #application=response.xpath('//h5[contains(text(),"Application")]/../span//text()').getall()
        #publication=response.xpath('//h5[contains(text(),"Publication")]/../span//text()').getall()
        #published_as=response.xpath('//h5[contains(text(),"Published")]/../span//text()').getall()
        #abstract=response.xpath('//h5[contains(text(),"Abstract")]/../div[contains(@class,"abstract__text")]//text()').getall()
        #
        #
        ##print(titolo_brevetto)
        #yield {"titolo_brevetto":titolo_brevetto,
        #       "applicants":applicants,
        #        "inventors":inventors,
        #        "classifications":classifications,
        #        "priorities":priorities,
        #        "application":application,
        #        "publication":publication,
        #        "published_as":published_as,
        #        "abstract":abstract}
