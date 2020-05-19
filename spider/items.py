import scrapy



class LinkedinItem(scrapy.Item):
    keywords = scrapy.Field()
    spiderUrl = scrapy.Field()
    jobId = scrapy.Field()
    jobUrl = scrapy.Field()
    jobType = scrapy.Field()
    jobTitle = scrapy.Field()
    companyName = scrapy.Field()
    companyUrl = scrapy.Field()
    jobFunction = scrapy.Field()
    description = scrapy.Field()
    industry = scrapy.Field()
    seniorityLevel = scrapy.Field()
    companyAddress = scrapy.Field()
    employmentType = scrapy.Field()
    createdTime = scrapy.Field()
    updatedTime = scrapy.Field()
    pass