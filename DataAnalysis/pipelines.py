# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class DataanalysisPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self, dbPool):
        self.dbPool = dbPool
        self.bool = 0

    @classmethod
    def from_settings(cls, settings):
        dbParams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbPool = adbapi.ConnectionPool('MySQLdb', **dbParams)
        return cls(dbPool)

    def process_item(self, item, spider):
        # 异步插入

        query = self.dbPool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常

        print(failure)

    def do_insert(self, cursor, item):
        # 所有需要处理的插入

        insert_sql, params = item.get_insert_sql()
        bool = cursor.execute(insert_sql, params)

        # 如果是基础信息表，则更新一条数据
        if bool == 1 and item.__class__.__name__ == 'jingDataBaseItem':
            update_sql, params = item.get_update_sql()
            cursor.execute(update_sql, params)

