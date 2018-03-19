# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from baiduxueshu.spiders import mysql
from baiduxueshu.items import *
class PaperSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = []
    # start_urls = ['http://xueshu.baidu.com/s?wd=%E6%B1%9F%E8%83%9C+%E5%8D%8E%E4%B8%AD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2']
    start_urls = ['http://xueshu.baidu.com/s?wd=paperuri%3A%28a72af683bc174adec26f1a2055490c38%29&filter=sc_long_sign&sc_ks_para=q%3D%E4%B8%8D%E5%90%8C%E6%8A%95%E8%B5%84%E8%80%85%E8%A1%8C%E4%B8%BA%E5%AF%B9%E6%8A%95%E8%B5%84%E9%A1%B9%E7%9B%AE%E7%9A%84%E5%BD%B1%E5%93%8D&sc_us=516139647507627672&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8']

    page = 1

    def parse(self, response):
        pass















        # # 数据库姓名处理
        # a = mysql.Mysql().getTeacherList()
        #
        # teacherList = {}
        #
        #
        # for node in a:
        #     if len(node[1])==0:
        #         pass
        #     elif len(node[1])<4 and len(node[1])>1:
        #
        #         if len(re.findall(r'[\u4E00-\u9FA5] [\u4E00-\u9FA5]', node[1])) > 0:
        #             t =node[1].replace(' ','')
        #             mysql.Mysql().InsertTeacher(node[0],t,node[2])
        #             print(node[0],t,node[2])
        #         else:
        #             mysql.Mysql().InsertTeacher(node[0], node[1], node[2])
        #             print(node[0],node[1],node[2])
        #         pass
        #     elif len(node[1])>3:
        #         #如果包含中文
        #         if len(re.findall(r'[\u4E00-\u9FA5]', node[1])) > 0:
        #             t = "".join(re.findall(r'[\u4E00-\u9FA5]|·', node[1]))
        #             t= t.replace("兼职","").replace("讲师","").replace("实验师","").replace("博导","").replace("简介","").replace("院士","").replace("研究员","").replace("教师","")
        #             mysql.Mysql().InsertTeacher(node[0], t, node[2])
        #             pass
        #         #只有英文
        #         else:
        #             print(node[0], node[1], node[2])








#判断xpath取值是否为空，若为空则返回空字符（避免异常）
    def setValue(self, node, value, index):
        if len(node):
            return node.extract()[index].strip()
        else:
            return value


