# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags
from w3lib.html import replace_escape_chars # serve eliminare \n\t all'interno della stringa project_id




class EspacenetItem(scrapy.Item):
    titolo_brevetto=scrapy.Field()
    link_brevetto=scrapy.Field(output_processor=TakeFirst())
    id_project=scrapy.Field(output_processor=TakeFirst())
    lingua_descrizione=scrapy.Field()
    applicants=scrapy.Field()
    inventors=scrapy.Field()
    classifications_ipc=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=Join(" "))
    classifications_cpc=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=Join(" "))
    priorities=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=Join(""))
    application=scrapy.Field()
    publication=scrapy.Field()
    published_as=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=Join(" "))
    abstract=scrapy.Field(output_processor=Join(" "))
