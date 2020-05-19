# linkedinSpider

Crawl job information from LinkedIn for data analysis.

## Install

### Dependency

    sudo apt install -y python3-pip
    pip3 install scrapy
    pip3 install pymysql
    pip3 install fake_useragent

### Config

    # Input database information in file `spiders/settings.py`
    # Create table using SQL file `create.sql`

## Usage

### Common usage
    # Input job title in table `titles`
    # Then run
    scrapy crawl linkedin
    # Data will be stored in table `positions`

### Advanced usage
    # For different project, you should create positions and titles with prefix, like `it_positions`, `it_title`
    # Then input job title in table `it_titles`
    # Then run
    scrapy crawl linkedin -a prefix=it
    # data will be stored in table `it_positions`