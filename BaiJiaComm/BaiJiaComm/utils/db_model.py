# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/4/15
# @File: db_model.py
# @Software: PyCharm
"""
peewee==2.10.1
"""
# -*- coding: utf-8 -*-


import pymysql
import peewee
import traceback
from playhouse.shortcuts import RetryOperationalError


peewee.mysql = pymysql
peewee.logger.setLevel("ERROR")


def query_author_sql(sql, params=None):
    conn = cursor = None
    try:
        conn = pymysql.connect(user="root", password="", database="", host="",
                               charset="utf8mb4")
        params = None or tuple()
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            for data in cursor:
                yield data
    except:
        print(str(traceback.format_exc()))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


class MyMySQL(RetryOperationalError, peewee.MySQLDatabase):
    pass


config = {'host': '192.168.1.114', 'password': '123456', 'port': 3306, 'user': 'root', 'charset': 'utf8mb4'}
database = MyMySQL('box_data', **config)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class BoxComment(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    content_id = peewee.CharField()
    nickname = peewee.CharField()
    cover = peewee.CharField()
    comment = peewee.CharField()
    comment_time = peewee.CharField()
    pid = peewee.IntegerField()
    source_id = peewee.CharField()

    class Meta:
        db_table = 'box_comment'
