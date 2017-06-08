# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tutorial.spiders.TabeLog import domain
import os
import json

class TutorialPipeline(object):

    def __init__(self):
        pwd = os.getcwd()
        if not os.path.exists(pwd+"/"+domain):
            os.mkdir(pwd+"/"+domain)
        os.chdir(pwd+"/"+domain)

    def process_item(self, item, spider):
        if not os.path.exists(str(item['num'])):
            os.mkdir(str(item['num']))
        os.chdir(str(item['num']))
        file = open('items.txt', 'w')
        line = "name : " + item['name'] + "\n"
        file.write(line)
        line = "link : "+item['link'] + "\n"
        file.write(line)
        line = "image_urls : " + str(item['image_urls']) + "\n"
        file.write(line)
        os.chdir('../')
        return item
