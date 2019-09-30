import requests
from html import unescape
from html import escape
from bs4 import BeautifulSoup
import bs4
import time
import json


# naver place data crolling

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def download(method, url, param=None, data=None,
             headers = None, maxretries=4 ):
    try :
        resp = requests.request(method, url, params = param,
                                data=data,headers = headers )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= e.response.status_code < 600 and maxretries > 0 :
            print(maxretries)
            resp = download(method, url, param, data, maxretries - 1)
        else :
            print(e.response.status_code)
            print(e.response.reason)
    return resp


# 디비 연동
import sqlite3


conn = sqlite3.connect('zeropay.db')
cur = conn.cursor()

cur.executescript('''
        DROP TABLE pay_info;

    CREATE TABLE pay_info(
        ID          INTEGER NOT NULL PRIMARY KEY,
        NAME        TEXT NOT NULL,
        DESC        TEXT NOT NULL,
        IMAGE_URL   TEXT ,
        ROAD_ADDR   TEXT NULL,
        COMMON_ADDR TEXT NULL,
        ADDR        TEXT NULL
    );
''')
conn.commit()




# 크롤링
import re
import json

MAX_PAGE_NO = 100 # 최대 페이지 번호
url = "https://store.naver.com/attractions/list"


for i in range(1, MAX_PAGE_NO+1):
    try:
        html = download("get", url, param={'page':i, 'query':'제로페이가맹점', 'region':'서울시'},headers=headers)
        html.encoding = 'utf-8'
        dom = BeautifulSoup(html.text, "html.parser")
        jsonData = re.search('window\.PLACE_STATE=(.*)', dom.prettify()).group(1)
        jsonData = json.loads(jsonData)
        queue = jsonData['businesses']['queue']
        items = jsonData['businesses'][queue[0]]['items']
        for item in items:
            try:
                itemId = item['id']
                name = item['name']
                desc = item['desc']
                imageSrc=item['imageSrc']
                roadAddr, commonAddr, addr = item['roadAddr'], item['commonAddr'], item['addr']

                cur.execute('''
                    INSERT INTO pay_info(ID, NAME, DESC, IMAGE_URL, ROAD_ADDR, COMMON_ADDR, ADDR)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (itemId, name, desc,imageSrc, roadAddr, commonAddr, addr))
                conn.commit()
            except:
                continue
    except:
        continue


cur.close()
conn.close()

url = "https://store.naver.com/attractions/list"
html = download("get", url, param={'query':'제로페이가맹점', 'region':'서울시'},headers=headers)
dom = BeautifulSoup(html.text, "html")

html.encoding = 'utf-8'