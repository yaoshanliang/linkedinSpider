import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置
from datetime import datetime
from spider.items import LiepinItem
from twisted.internet import defer
class SpiderPipeline(object):

    def __init__(self):
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  #读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  #编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        #**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    def close_spider(self, spider):
        self.dbpool.close()

    # pipeline默认调用
    def process_item(self, item, spider):
        # query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        # query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):
        sql = "insert into `position`(keywords,spiderUrl,jobId,jobTitle,jobType,jobUrl,companyId,companyUrl,companyName,salary,position,pubTime,qualification,description,industry,companySize,companyAddress,isEnd,createdTime,updatedTime) \
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        item['createdTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        params = (item['keywords'], item['spiderUrl'], item['jobId'], item['jobTitle'], item['jobType'],item['jobUrl'],item['companyId'],item['companyUrl'],
        item['companyName'],item['salary'],item['position'],item['pubTime'],item['qualification'],item['description'],item['industry'],
        item['companySize'],item['companyAddress'],item['isEnd'],item['createdTime'],item['updatedTime'])
        # print(sql)
        # print(params)
        tx.execute(sql, params)
        print("新增成功: ", item['keywords'], item['jobId'])


    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print('--------------database operation exception!!-----------------')

        print(failue)

    
