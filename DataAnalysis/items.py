# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from DataAnalysis.settings import SQL_DATETIME_FROMAT


class DataanalysisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class jingDataItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class jingDataArticleItem(scrapy.Item):
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    product_brief = scrapy.Field()
    start_date_desc = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jingdata_spider(product_id, product_name, product_brief, start_date_desc, crawl_time)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE product_name=VALUES(product_name), product_brief=VALUES(product_brief),
            start_date_desc=VALUES(start_date_desc), crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['product_id'], self['product_name'], self['product_brief'], self['start_date_desc'],
            self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params


class ProjectItem(scrapy.Item):
    project_id = scrapy.Field()
    project_name = scrapy.Field()
    project_des = scrapy.Field()
    industry = scrapy.Field()
    city = scrapy.Field()
    year = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into project(project_id, project_name, project_des, industry, city, year, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE project_name=VALUES(project_name), project_des=VALUES(project_des),
            industry=VALUES(industry), city=VALUES(city), year=VALUES(year), crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['project_id'], self['project_name'], self['project_des'], self['industry'], self['city'],
            self['year'], self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params

    def get_update_sql(self):
        update_sql = """
            UPDATE jingdata_spider SET start_date_desc=0 where product_id={}
        """.format(self['project_id'])

        return update_sql, ()


class FinanceRoundItem(scrapy.Item):
    project_id = scrapy.Field()
    round_num = scrapy.Field()
    round_year = scrapy.Field()
    financing_round = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into financing_round(project_id, round_num, round_year, financing_round, crawl_time)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['project_id'], self['round_num'], self['round_year'], self['financing_round'],
            self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params


class ProjectLabelItem(scrapy.Item):
    project_id = scrapy.Field()
    label_num = scrapy.Field()
    label = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into project_label(project_id, label_num, label, crawl_time)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['project_id'], self['label_num'], self['label'],
            self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params