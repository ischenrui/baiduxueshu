# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# class CitedAndRefItem(scrapy.Item):
#     id = scrapy.Field()
#     paper_md5 = scrapy.Field()
#     citeORref = scrapy.Field()
#     name = scrapy.Field()
#     url = scrapy.Field()
#     org = scrapy.Field()
#     year = scrapy.Field()
#     cited_num = scrapy.Field()
#     source = scrapy.Field()
#     source_url = scrapy.Field()
#     keyword = scrapy.Field()
#     author = scrapy.Field()
#     abstract = scrapy.Field()

class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    abstract = scrapy.Field()
    org = scrapy.Field()
    year = scrapy.Field()
    cited_num = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    cited_url = scrapy.Field()
    reference_url = scrapy.Field()
    paper_md5 = scrapy.Field()

    pass
