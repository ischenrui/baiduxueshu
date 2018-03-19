import pymysql.cursors
# 连接数据库
class Mysql(object):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Cr648546845',
        db='eds_section1',
        charset='utf8'
)
# 获取游标
    cursor = connect.cursor()

    # 关键字操作

    #获取作者相关信息
    def getAuthor(self):
        sql = "SELECT id,name,school FROM papaer_teacherList WHERE search=0"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 插入论文
    def InsertPaper(self, item):
        sql = "INSERT INTO paper VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
        params = (
        item['name'], item['url'], item['abstract'], item['org'], item['year'], item['cited_num'], item['source'],
        item['source_url'], item['keyword'], item['author'], item['author_id'], item['cited_url'], item['reference_url'], item['paper_md5'])
        self.cursor.execute(sql, params)
        self.connect.commit()

    # # 插入论文参考引用
    # def InsertPaperCiteORRef(self, item):
    #     sql = "INSERT INTO paper_citeorref VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
    #     params = (
    #         item['paper_md5'], item['citeORref'], item['name'], item['url'], item['org'], item['year'],
    #         item['cited_num'],
    #         item['source'], item['source_url'], item['keyword'], item['author'], item['abstract'])
    #     self.cursor.execute(sql, params)
    #     self.connect.commit()

    def getAuthoridlist(self):
        sql = "SELECT id FROM papaer_teacherList where search=1"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getPaperauthorlist(self):
        sql = "SELECT author_id FROM paper"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def UpdatePtlist(self,id):
        sql = "UPDATE papaer_teacherlist SET search=0 where id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()
        print("gengxing:::::", id)
    # 搜索后更新状态
    def UpdateAuthor(self,id):
        sql = "UPDATE papaer_teacherList SET search=1 where id=%s"
        params = (id)
        self.cursor.execute(sql, params)
        self.connect.commit()

    # def getTeacherList(self):
    #     sql = "SELECT id,name,school FROM teacherdata WHERE search=0"
    #     self.cursor.execute(sql)
    #     return self.cursor.fetchall()
    #
    # def InsertTeacher(self, id,name,school):
    #     sql = "INSERT INTO papaer_teacherList VALUES(%s,%s,%s,0)"
    #     params = (id,name,school)
    #     self.cursor.execute(sql, params)
    #     self.connect.commit()
    #
    #
    # def SSSS(self):
    #     sql = "SELECT author_id FROM paper GROUP BY author_id"
    #     self.cursor.execute(sql)
    #     return self.cursor.fetchall()

