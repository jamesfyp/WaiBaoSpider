# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import traceback

from utils.db_model import BoxComment, database
from items import BaijiacommItem

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
DEFAULT_CACHE_SIZE = 20


class BaijiacommPipeline(object):
    def __init__(self, cache_size=DEFAULT_CACHE_SIZE):
        self._cache = []
        self._cache_size = cache_size

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        try:
            cache_size = int(settings["MX_LIVE_CACHE_SIZE"])
        except (KeyError, ValueError, TypeError):
            cache_size = DEFAULT_CACHE_SIZE
        return cls(cache_size)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self._flush_data()

    @staticmethod
    def _set_default_value(data):
        for attr in BaijiacommItem.fields:
            if attr not in data:
                data[attr] = None

    def process_item(self, item, spider):
        if isinstance(item, BaijiacommItem):
            try:
                d = dict(item)
                self._cache.append(d)
                if len(self._cache) >= self._cache_size:
                    self._flush_data()
            except Exception:
                logger.info(str(traceback.format_exc()))

        return item

    def _flush_data(self):
        if len(self._cache) == 0:
            return
        sql, params = (BoxComment.insert_many(self._cache)).sql()
        sql = sql.lower().replace("insert", "insert ignore")
        try:
            length = len(self._cache)
            database.execute_sql(sql, params)
            logger.info("Uploaded %d items to Mysql." % length)
        except:
            logger.error(str(traceback.format_exc()))
        finally:
            self._cache = []
