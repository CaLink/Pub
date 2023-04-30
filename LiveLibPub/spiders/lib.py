import sqlite3
import os

def dbInit():
    if(not os.path.exists("db")):
        os.mkdir("db")
    if(not os.path.exists("db/log")):
        os.mkdir("db/log")

def writeLog(name, resp):

        if(resp.status != 200):
            with open(f"db/{name}Log.txt",'a',encoding='utf8') as fp:
                fp.write(f"{resp.status}\t{resp.url}\t{resp.request.headers.get('Referer', None)}\n")
        else:
            with open(f"db/{name}Success.txt",'a',encoding='utf8') as fp:
                fp.write(f"{resp.url}\n")


def initDB(name):
    connection = sqlite3.connect(f'db/{"book"}.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
                        name TEXT, books TEXT, description TEXT, city TEXT, lastChage TEXT, url TEXT, urlBook TEXT, urlSite TEXT
                        )''')
    connection.commit()
    cursor.close()

def dbADD(name, pub):
    connection = sqlite3.connect(f'db/{"book"}.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {name} VALUES (?,?,?,?,?,?,?,?)",
                    (pub.name, pub.books, pub.description, pub.city, pub.lastChange, pub.url, pub.urlBook, pub.siteUrl))
    connection.commit()
    connection.close()