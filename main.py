from LiveLibPub.spiders import book

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import sqlite3

configure_logging()

config = CrawlerRunner(settings={'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False})


conn = sqlite3.connect("db/book.db")
cur = conn.cursor()
cur.execute("SELECT urlBook, books, name FROM puber")

db = cur.fetchall()

cur.close()
conn.close()


@defer.inlineCallbacks
def bookParser():
    for i in db:
        yield config.crawl(book.BookSpider,i[0],int(i[1]),i[2])

bookParser()


reactor.run()