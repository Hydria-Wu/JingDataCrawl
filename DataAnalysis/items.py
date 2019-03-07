# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from settings import SQL_DATETIME_FROMAT


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
            ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['product_id'], self['product_name'], self['product_brief'], self['start_date_desc'],
            self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params


class jingDataBaseItem(scrapy.Item):
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    product_brief = scrapy.Field()
    start_date_desc = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jingdata_base(product_id, product_name, product_brief, start_date_desc, crawl_time)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['product_id'], self['product_name'], self['product_brief'], self['start_date_desc'],
            self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params

    def get_update_sql(self):
        update_sql = """
            UPDATE jingdata_spider SET start_date_desc=0 where product_id={};
        """.format(self['product_id'])

        return update_sql, ()


class jingDataFinanceItem(scrapy.Item):
    product_id = scrapy.Field()
    finance = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jingdata_finance(product_id, finance, crawl_time)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
        """

        params = (
            self['product_id'], self['finance'], self['crawl_time'].strftime(SQL_DATETIME_FROMAT),
        )

        return insert_sql, params