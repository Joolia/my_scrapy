# -*- coding: utf-8 -*-

# Define your item pipelines here`
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

connection = None


class MyScrapyPipeline(object):
    def __init__(self):
        self.setupDBConnection()
        self.createTables()

    def setupDBConnection(self):
        self.connection = sqlite3.connect('./test.db')
        self.cursor = self.connection.cursor()

    def createTables(self):
        self.dropHabrTable()
        self.createHabrTable()

    def dropHabrTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS authors")

    def closeDB(self):
        self.connection.close()

    def __del__(self):
        self.closeDB()

    def createHabrTable(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY NOT NULL, name TEXT, title TEXT)''')

    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def storeInDb(self, item):
        print item['name']

        self.cursor.execute("INSERT INTO authors(name, title) VALUES (?,?)",
                            (item['name'].decode('utf-8'),
                             item['title']))
        print ("==============")
        print ("data stored")
        print ("==============")
        self.connection.commit()
