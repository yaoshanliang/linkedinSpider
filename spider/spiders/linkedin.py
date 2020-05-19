# -*- coding: utf-8 -*-
import scrapy

from urllib import parse as urlparse
from spider.items import LinkedinItem
# from spider.pipelines import SpiderPipeline
from scrapy.utils.project import get_project_settings  #导入seetings配置
import pymysql
from twisted.enterprise import adbapi
from twisted.internet import defer
import sys
from datetime import datetime
import re
from http.cookies import SimpleCookie


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'

    def start_requests(self):
        self.keyword = ' '.join(self.keyword.split('+'))
        self.page = 0
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        self.db = pymysql.connect(settings['MYSQL_HOST'], settings['MYSQL_USER'], settings['MYSQL_PASSWD'], settings['MYSQL_DBNAME'])
        self.cursor = self.db.cursor()

        yield scrapy.Request('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location=Worldwide&trk=public_jobs_jobs-search-bar_search-submit&sortBy=DD&start=0&keywords=' + self.keyword)
        # yield scrapy.Request('https://www.linkedin.com/jobs/search?location=Worldwide&locationId=OTHERS.worldwide&&keywords=' + self.keyword)

    def parse(self, response):

        ids = re.findall("data-id=\"(.+?)\"", response.text)
        datatimes = re.findall("datatime=\"(.+?)\"", response.text)

        item = LinkedinItem()
        item['keywords'] = self.keyword
        item['spiderUrl'] = response.url

        print(len(ids))
        for id in ids:
            item['jobId'] = id

            sql = "SELECT `keywords` FROM `linkedin` where `jobId` = '%s'"
            self.cursor.execute(sql % (item['jobId']))
            result = self.cursor.fetchone()
            # print(result)

            if result :
                if item['keywords'] in result[0].split('|'):
                    print("跳过: ", item['keywords'], item['jobId'])
                else:
                    newKeywords = result[0] + '|' + item['keywords']
                    sql = "UPDATE `linkedin` SET `keywords` = '%s', `updatedTime` = '%s' where `jobId` = '%s'"
                    self.cursor.execute(sql % (newKeywords, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), item['jobId']))
                    self.db.commit()
                    print("更新成功: ", item['keywords'], item['jobId'], newKeywords)

                continue

            item['jobUrl'] = "https://www.linkedin.com/jobs/view/" + id
            yield scrapy.Request(url=item['jobUrl'], callback=self.detail, meta=item)

        self.page = self.page + 1
        print(item['spiderUrl'])

        cookie = {
            "bcookie":"v=2&1d6ee84e-02dc-4f68-864d-031beaec0113",
            "bscookie":"v=1&2018071716391821f46663-6999-4474-80b8-94b96fdd2251AQGt2UtvZ06GsHmEtz15GULg6ZPiYOKM",
            "_ga":"GA1.2.1425278570.1562486640",
            "li_sugr":"f3ee46e3-06ef-41a5-a8de-4a794d2b71e9",
            "lissc1":"1",
            "lissc2":"1",
            "_guid":"80ac78df-855d-447b-bfcf-ea131f952569",
            "li_oatml":"AQH1NOLABtFR5gAAAW9fnqqLj_Vr55bNfumrzlEKhB4tXQuplWjuAS50GhZS-HGZFIakL5Sroe9OVUMEBmidmDdCYwOtVkAu",
            "sdsc":"22%3A1%2C1577857235359%7ECONN%2C0GSxQpcKhSl%2B0Pti7%2Bgudf1so0l8%3D",
            "spectroscopyId":"e5991084-99aa-4cb3-8936-36085f73acfb",
            "visit":"v=1&M",
            "_lipt":"CwEAAAFvbtbuDs-GjQ0JcMgmLRRoeLoBsvuTTB6a5gO2b08ThkByKT04ciJErcWHhGxamj-bqOD5IiVyeZ-STJL9pkuKiZ7kTytlHG_TP5AximdjsDue3ajgtgPrJqXlthjYiICeFsXTX2K3qKy1mlxqzNAJdChXhM5ttrNrAdPw3-zrghZ_BcRg3xcjsfjrEm5sBMirsFy9zLsZQ-jB7eUbPs_LKOTYI_IS-6V1RUAKNC-N_b6eaIGYibg7vX4-FrHFdFP-UO97YhvxQw4ojZ4QT8jubXo2Ec8",
            "JSESSIONID":"ajax:7199985276185476361",
            "_gat":"1",
            "fid":"AQGiEh4E9x2GRAAAAW9u4mFJljzLlFKacWxBp2R7Q1JvdavcjNfGKIwvMohf6dik5vVCWyyco0ElDg",
            "fcookie":"AQGuCquxkB15BQAAAW9u4njMhEo0-PcilyikuKsGo1q5ty5OzJ75duunFcdcBGSuGcTjSZsCmDSMFjAwT0tZpO6JiQQE6WLrAc4l8gAuvkTwAQ8zBZSilWMHFtDkuVBaZKfmyh1fV2IE1sRuhDPxcmxTFqaj8xR8IxEQnNqJr7_LQ7KEsiO4Dl4_OZ7hLyEZFVY4-QgWTEKGia49il_AetKkSHfoQiJAbGxmOy4lfyRHxJhIF6tEwDRdIBczRQKfLxuudlo8zqgIaKXIcl5foQNjv4RY/iyP/4kK/fiVt6RWl/mXJx/NaGAFIzXjqsTFfl2z+X8z7liXHnaT7P7PnDf68RbBxM+sk52mzRmLF7yw==",
            "liap":"true",
            "li_at":"AQEDARVhIrkEDV97AAABb27nFuUAAAFvkvOa5VEAkWQF-BW-LcdWQyAQW2Wp3MaWS4wqMOmJzVPez8Ob0cPgtzDdDtYUoFK1wIQQoOiP6_XWF3_TLYEqK7R9zT2oebaTbKMR0lmZv2789Qb3a_mJi2eS",
            "sl":"v=1&2FIPv",
            "li_cc":"AQEy7rT56Go8AwAAAW9u5xiANT25bH0L4fmSPRyMdpHbZYDsKtwRzCK8UuVuPSB3vlizdw1t9V3B",
            "lang":"v=2&lang=en-us",
            "UserMatchHistory":"AQLPCjEbAgZxVwAAAW9vG3lfS7Dk2ZC8F8fx6JotYjTMhOV2AayF2f91ghYC_JJT2dW5bwzr63gshWld2lb2ni4CEIgWZ5LCVgHmE_vpqcMReAUWVXuyKsZDff4JCJs0kTL0VoS7w42BUuULhlo_l9mgmeX9dh1TgcA8YfGcrrwUxGFK661LPqO9T2ZydnHHGnsxvg",
            # "lidc":"b=SGST01:g=4:u=1:i=1578113642:t=1578200042:s=AQFOVLlhYD7Ob5PFGsZw9hCvSoBQxveH"
        }
        print(cookie)



        # cookies = dict(cookies)

        # if (len(ids) == 25):
        #     yield scrapy.Request(item['spiderUrl'] + '&start=' + str(self.page * 25), cookies=cookie, callback=self.parse)

    def detail(self, response):
        
        item = response.meta
        print(item['jobUrl'])

        with open('index.html', 'w') as html_file:
            html_file.write(response.text)
        yield {
            'url': response.url
        }
        item['jobTitle'] = response.css('.topcard__title::text').extract_first()
        item['companyName'] = response.css('.topcard__flavor::text').extract_first()
        item['companyAddress'] = response.css('.topcard__flavor--bullet::text').extract_first()
        description = response.css('.description__text--rich').extract_first()
        
        item['jobType'] = '领英'
        if ('职位来源于智联招聘。' in description):
            item['jobType'] = '智联'
            description = description.replace('职位来源于智联招聘。', '')
            description = description.replace('以担保或任何理由索要财物，扣押证照，均涉嫌违法。', '')
            item['companyUrl'] = ''
        else:
            item['companyUrl'] = response.css('.topcard__org-name-link::attr(href)').extract_first()
            

        item['description'] = re.compile(r'<[^>]+>',re.S).sub('', description)

        item['seniorityLevel'] = response.css('.job-criteria__item:nth-child(1) .job-criteria__text--criteria::text').extract_first()
        item['employmentType'] = response.css('.job-criteria__item:nth-child(2) .job-criteria__text--criteria::text').extract_first()
        item['jobFunction'] = ','.join(response.css('.job-criteria__item:nth-child(3) .job-criteria__text--criteria::text').extract())
        item['industry'] = response.css('.job-criteria__item:nth-child(4) .job-criteria__text--criteria::text').extract_first()


        # if (item['jobType'] == '企业'):
        #     companyUrlArray = item['companyUrl'].split('/')
        #     item['companyId'] = companyUrlArray[- 2]
        #     item['industry'] = response.css('.right-blcok-post .new-compintro li:nth-child(1) a::text').extract_first()

        #     companySize = response.css('.right-blcok-post .new-compintro li:nth-child(2)::text').extract_first()
        #     if (companySize):
        #         if (companySize[0:4] == '公司规模'):
        #             item['companySize'] = companySize[5:]
        #         if (companySize[0:4] == '公司地址'):
        #             item['companySize'] = ''
        #             item['companyAddress'] = companySize[5:]
        #     else:
        #         item['companySize'] = ''
        #         item['companyAddress'] = ''

        #     item['salary'] = response.css('.about-position .job-title-left .job-item-title::text').extract_first().split()[0]
        #     item['position'] = response.css('.about-position .job-title-left .basic-infor span a::text').extract_first()
        #     item['qualification'] = response.css('.about-position .job-item .job-qualifications span::text').extract_first()
        #     item['pubTime'] = response.css('.about-position .job-item .basic-infor time::attr(title)').extract_first()

        # else:
        #     item['companyName'] = ''
        #     item['companyUrl'] = ''
        #     item['companyId'] = ''
        #     item['companySize'] = response.css('.content-word li:nth-child(6)::text').extract_first()
        #     item['companyAddress'] = ''
        #     item['industry'] = response.css('.content-word li:nth-child(3) a::attr(title)').extract_first()
        #     item['salary'] = response.css('.about-position .job-title-left .job-main-title::text').extract_first().split()[0]
        #     item['position'] = response.css('.about-position .job-title-left .basic-infor span::text').extract_first()
        #     item['qualification'] = response.css('.about-position .resume span::text').extract_first()
        #     item['pubTime'] = response.css('.about-position  .basic-infor time::attr(title)').extract_first()

        

        # if response.css('.title-info label::text').extract_first() == '该职位已结束':
        #     item['isEnd'] = 1
        # else:
        #     item['isEnd'] = 0

        print(item)
        
        # yield item
        sql = "insert into `linkedin`(keywords,spiderUrl,jobId,jobTitle,jobUrl,companyName,description,industry,companyAddress,seniorityLevel, employmentType, jobFunction,jobType, companyUrl, createdTime,updatedTime) \
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)"

        item['createdTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute(sql, (item['keywords'], item['spiderUrl'], item['jobId'], item['jobTitle'],item['jobUrl'], item['companyName'],item['description'],item['industry'],item['companyAddress'],item['seniorityLevel'], item['employmentType'], item['jobFunction'], item['jobType'],item['companyUrl'], item['createdTime'],item['updatedTime']))
        self.db.commit()
        print("新增成功: ", item['keywords'], item['jobId'])
