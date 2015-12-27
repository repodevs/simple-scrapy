# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

logger = logging.getLogger('MentalFlossLogger')



class MongoDBPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		for data in item:
			if not data:
				raise DropItem("Missing Data Broh")
		self.collection.update({'url': item['url']}, dict(item), upsert=True)
		logger.info("========= Big Questions added to MongoDB database successfully ! ==============\n\n")
		return item

