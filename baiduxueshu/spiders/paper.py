# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
from urllib import parse
from baiduxueshu.items import *
from baiduxueshu.spiders import mysql

class PaperSpider(scrapy.Spider):
    name = 'paper'
    allowed_domains = []
    start_urls = ['http://www.baidu.com/']


    #查询 导师姓名和学习，并 加入爬取队列
    def parse(self, response):
        # self.renewSearch()
        author_list = mysql.Mysql().getAuthor()
        for node in author_list:
            id = node[0]
            teacher_name = node[1]
            org = node[2]

            url = "http://xueshu.baidu.com/s?wd=%22" + teacher_name + "%22+%22" + org + "%22+author%3A%28" + teacher_name + "%29&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2"
            yield scrapy.Request(url, lambda arg1=response, arg2=id: self.PaperList(arg1, arg2))

        # #----test-----
        # id = 1
        # teacher_name = "蒋青"
        # org = "北京大学"
        # url = "http://xueshu.baidu.com/s?wd=%22" + teacher_name + "%22+%22" + org + "%22+author%3A%28" + teacher_name + "%29&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2"
        # yield scrapy.Request(url, lambda arg1=response, arg2=id: self.PaperList(arg1, arg2))
        # print(id,"search=1")

    # 百度学术list页面，对于每个项，保存一部分信息，然后请求具体信息
    def PaperList(self, response,id):
        list = response.xpath("//div[@class='result sc_default_result xpath-log']")

        for node in list:
            item = PaperItem()
            item['author_id'] = id
            #文章名字 + url
            item['name'] = self.setValue(node.xpath("./div[1]/h3/a/text()"),"",0)
            item['url'] = "http://xueshu.baidu.com"+self.setValue(node.xpath("./div[1]/h3/a/@href"), "", 0)
            #文章发表期刊
            item['org'] = self.setPaperOrg(node)
            #文章年份
            item['year'] = self.setValue(node.xpath("./div[1]/div[1]/span[3]/text()"),"",0)
            #文章被引数
            item['cited_num'] = int(self.setValue(node.xpath("./div[1]/div[1]/span[4]/a/text()"),0,0))
            #来源 + url
            # item['source'] = self.setValue(node.xpath("./div[1]/div[2]/div/span[2]/a/text()"),"",0)
            # item['source_url'] = self.setValue(node.xpath("./div[1]/div[2]/div/span[2]/a/@href"),"",0)
            #关键词
            item['keyword'] = ",".join(node.xpath("./div[2]/div[1]/a/text()").extract())
            yield scrapy.Request(item['url'], lambda arg1=response, arg2=item: self.PaperInfo(arg1, arg2))
            # print('抓取PaperInfo页面')

        a = response.xpath("//a[@class='n']")
        if not a:mysql.Mysql().UpdateAuthor(id)
        sflag = 0
        for node in a:
            b = self.setValue(node.xpath("./text()"), "", 0)
            # print(b)
            if b == "下一页>":
                sflag = 1
                url = "http://xueshu.baidu.com" + self.setValue(node.xpath("./@href"), "", 0)
                # print(url)
                page = re.findall(r"pn=([1-9])",url)[0]
                # print(page)
                if int(page)<6:
                    # print ("翻页")
                    yield scrapy.Request(url, lambda arg1=response, arg2=id: self.PaperList(arg1, arg2))
        if sflag == 0: mysql.Mysql().UpdateAuthor(id)


    #每篇文章的具体信息页面，保存部分信息，解析参考&引用的json，请求源url以获取摘要
    def PaperInfo(self,response,item):

        # #文章作者+机构，以 json 格式存储
        # paper_author = ",".join(response.xpath("//div[@class='author_wr']/p[2]/a/text()").extract())
        # item['author'] = paper_author.replace("\r\n        ","")
        paper_author_list = response.xpath("//div[@class='author_wr']/p[2]/a")
        item['author'] = self.getAuthorOrg(paper_author_list)

        #获取构造json链接的   相关字段
        paper_md5 = re.findall(r"paperuri:\((.+)\)",str(response.body,'utf-8'))[0]
        item['paper_md5'] = paper_md5

        paper_time = str(int(time.time()*1000))
        paper_sourceURL = self.setValue(response.xpath("//div[@class='subinfo_tool']/a[1]/@data-url"),"",0)
        # item['source_url'] = paper_sourceURL
        # item['source'] = self.setValue(response.xpath("//div[@class='source']/a/text()"),"",0)

        item['source_url'] = ""
        #由于万方有请求限制，所以不要万方的url
        source_list = response.xpath("//div[@class='allversion_content']/span")
        for node in source_list:
            source = self.setValue(node.xpath("./a/span[2]/text()"), "", 0)
            if source != "万方":
                item['source_url'] = self.setValue(node.xpath("./a/@data-url"), "", 0)
                item['source'] = source
                break
        #可能 源url只有万方，或者为空
        if len(source_list) and item['source_url']=="":
            item['source_url'] = paper_sourceURL
            item['source'] = "万方"
        elif len(source_list) is None:
            item['source_url'] = paper_sourceURL
            item['source'] = ""
        #构造 引用、参考链接
        item['cited_url'] = "http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery110209415027881771602_"+paper_time+"&wd=refpaperuri:("+paper_md5+")&req_url="+paper_sourceURL+"&type=citation&rn=10&page_no=1&_="+paper_time
        item['reference_url'] = "http://xueshu.baidu.com/usercenter/data/schpaper?callback=jQuery110209415027881771602_"+paper_time+"&wd=citepaperuri:("+paper_md5+")&req_url="+paper_sourceURL+"&type=reference&rn=10&page_no=1&_="+paper_time
        yield scrapy.Request(item['source_url'], lambda arg1=response, arg2=item: self.PaperAbstract(arg1, arg2))

        # yield scrapy.Request(item['cited_url'], lambda arg1=response, arg2=item, arg3="cite": self.requestJsonlist(arg1, arg2, arg3))
        # yield scrapy.Request(item['reference_url'], lambda arg1=response, arg2=item, arg3="ref": self.requestJsonlist(arg1, arg2, arg3))

        # mysql.Mysql().UpdateAuthor(item['author_id'])

    # #解析json，获取页码，并且获取list
    # def requestJsonlist(self,response,item,citeORref):
    #     paper_json = str(response.body, 'utf-8')
    #     temphead = re.findall("jQuery\w+\(", paper_json)[0]
    #     paper_json = paper_json.rstrip(')').lstrip(temphead)  # 去掉左右不符合json格式的字符
    #     jsonlist = json.loads(paper_json)
    #
    #     try:
    #         totalPageNum = jsonlist['data']['totalPageNum']
    #
    #         for i in range(1,totalPageNum+1):
    #             url = response.url.replace('page_no=1','page_no='+str(i))
    #             yield scrapy.Request(url, lambda arg1=response, arg2=item, arg3=citeORref: self.Analysis_Json(arg1, arg2, arg3),dont_filter=True)
    #     except:
    #         print("没有json页面")

    # #解析json，获取参考 & 引用的信息
    # def Analysis_Json(self,response,item,citeORref):
    #
    #     paper_json = str(response.body,'utf-8')
    #     temphead = re.findall("jQuery\w+\(", paper_json)[0]
    #     paper_json = paper_json.rstrip(')').lstrip(temphead)    #去掉左右不符合json格式的字符
    #     jsonlist = json.loads(paper_json)
    #
    #     listj = jsonlist['data']['resultList']
    #
    #     for node in listj:
    #         try:
    #             critem = CitedAndRefItem()
    #             critem['paper_md5'] = item['paper_md5']
    #             critem['citeORref'] = citeORref
    #             critem['name'] = node['meta_di_info']['sc_title'][0]
    #             critem['org'] = self.setJsonOrg(node)
    #             critem['year'] = node['meta_di_info']['sc_time'][0]
    #             critem['cited_num'] = int(node['meta_di_info']['sc_cited'][0])
    #             critem['source'] = node['meta_di_info']['sc_source'][0]
    #             critem['source_url'] = node['meta_di_info']['url']
    #             critem['keyword'] = self.setJsonKeyword(node)
    #             critem['author'] = self.setJsonAuthor(node)
    #             critem['url'] = "http://xueshu.baidu.com/s?wd=paperuri%3A("+node['meta_di_info']['sc_longsign'][0]+")&filter=sc_long_sign&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_ks_para=q%3D"+node['meta_di_info']['sc_title'][0]
    #             yield scrapy.Request(critem['source_url'],lambda arg1=response, arg2=critem: self.PaperAbstract(arg1, arg2))
    #         except:
    #             print("解析json出错")

    def PaperAbstract(self, response, item):
        if item['source']=="知网":
            if len(re.findall('http://kns', response.url)) > 0:
                item['abstract'] = self.setValue(response.xpath("//span[@id='ChDivSummary']/text()"), "", 0)
                if item['author'] == "":    #如果之前作者为空，则在源链接里面再存一遍作者和单位
                    author_list = response.xpath("//div[@class='author']/span/a/text()").extract()
                    item['author'] = self.getAbstractAuthor(author_list)
            else:
                #存储摘要
                item['abstract'] = self.setValue(response.xpath("//div[@class='xx_font'][1]/text()"),"",1)
                if item['author'] == "":    #如果之前作者为空，则在源链接里面再存一遍作者和单位
                    author_list = response.xpath("//div[@id='content']/div[2]/div[3]/a/text()").extract()
                    item['author'] = self.getAbstractAuthor(author_list)
        elif item['source']=="万方":
            #有两种类型的链接，分类处理
            if len(re.findall('http://d.g', response.url)) > 0:
                item['abstract'] = self.setValue(response.xpath("//div[@class='abstract']/textarea/text()"), "", 0)
                if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                    author_list = response.xpath("//table[@id='perildical_dl']/tr[1]/td/a/text() | //table[@id='perildical2_dl']/tr[1]/td/a/text()").extract()
                    item['author'] = self.getAbstractAuthor(author_list)
            else:
                item['abstract'] = self.setValue(response.xpath("//div[@class='abstract']/textarea/text()"), "", 0)
                if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                    author_list = response.xpath("//div[@class='row row-author']/span[2]/a/text()").extract()
                    item['author'] = self.getAbstractAuthor(author_list)
        elif item['source']=="维普":
            # 存储摘要
            item['abstract'] = self.setValue(response.xpath("//td[@class='sum']/text()"),"",2)
            if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                list = response.xpath("//span[@class='detailtitle']/strong/i/a/text()").extract()
                author_list = []
                for i in range(0, len(list)):
                    if len(list[i]) in range(1, 4):
                        author_list.append(list[i])
                item['author'] = self.getAbstractAuthor(author_list)
        else:
            item['abstract'] = ""
        yield item


    def getAbstractAuthor(self,author_list):
        if len(author_list) > 0:
            paper_author_out = "{"
            for a in author_list:
                if len(a.strip())>0 :
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (a, "")
            return paper_author_out.rstrip(',') + '}'
        else:
            return ""

    # 解析 作者和机构，如果没有就返回空
    def getAuthorOrg(self, paper_author_list):
        name_list = paper_author_list.xpath("./text()").extract()
        url_list = paper_author_list.xpath("./@href").extract()
        if (len(name_list) == len(url_list) and len(name_list) < 6):
            paper_author_out = "{"
            for i in range(0, len(url_list)):
                t = re.findall(r'[\u4E00-\u9FA5]+', parse.unquote(url_list[i]))
                if len(t) == 2:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (t[0], t[1])
                elif len(t) == 1:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (t[0], "")
                elif len(t) == 0:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (
                    name_list[i].replace("\r\n        ", ""), "")
                else:
                    return ""
            return paper_author_out.rstrip(',') + '}'
        else:
            return ""

            # 解析json 作者和组织
    def setJsonKeyword(self, node):
        try:
            return ",".join(node['meta_di_info']['sc_research'])
        except:
            return ""

    # 解析json 作者和组织
    def setJsonAuthor(self,node):
        try:
            paper_author_out = "["
            for a in node['meta_di_info']['sc_author']:
                org = a['sc_affiliate'][0].replace('','')
                paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"},"%(a['sc_name'][0],org)

            return paper_author_out.rstrip(',')+']'
        except:
            return ""

    #解析json 文章投递机构
    def setJsonOrg(self,node):
        try:
            return node['meta_di_info']['sc_publish'][0]['sc_journal'][0]
        except:
            try:
                return node['meta_di_info']['sc_publish'][0]['sc_publisher'][0]
            except:
                return ""

    #取文章发表的期刊机构
    def setPaperOrg(self,node):
        data = node.xpath("./div[1]/div[1]/span[2]/a")
        if len(data):
            return data.xpath('string(.)').extract()[0].strip()
        else:
            return self.setValue(node.xpath("./div[1]/div[1]/span[2]/em/text()"), "", 0)

    #判断xpath取值是否为空，若为空则返回空字符（避免异常）
    def setValue(self, node, value, index):
        if len(node):
            return node.extract()[index].strip()
        else:
            return value

    #将 papaer_teacherlist表中search=1 但没有论文作者的id在paper中的search重设为0
    def renewSearch(self):
        alist = mysql.Mysql().getAuthoridlist()
        plist = mysql.Mysql().getPaperauthorlist()

        tidlist = [x[0] for x in alist]
        pidlist = [x[0] for x in plist]

        resetlist = list(set(tidlist) - set(pidlist))
        print(resetlist)

        for node in resetlist:
            mysql.Mysql().UpdatePtlist(node)
