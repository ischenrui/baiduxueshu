# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from baiduxueshu.items import *
from baiduxueshu.spiders.mysql import Mysql

class BaiduxueshuPipeline(object):
    mysql = Mysql()

    def process_item(self, item, spider):
        if type(item)==PaperItem:
            self.Paper(item)

        # elif type(item)==CitedAndRefItem:
        #     self.CRPaper(item)


        return item

    def Paper(self,item):
        self.mysql.InsertPaper(item)

    # def CRPaper(self,item):
    #     self.mysql.InsertPaperCiteORRef(item)
