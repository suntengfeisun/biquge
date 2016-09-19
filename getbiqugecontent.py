# -*- coding: utf-8 -*-

import time
import requests
import chardet
from lxml import etree
from public.mysqlpooldao import MysqlDao
from public.headers import Headers

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    mysql_dao = MysqlDao()
    limit_m = 0
    limit_n = 10000
    while True:
        sql = 'select `id`,`url`,`name` from fiction_chapter_11 WHERE `url` <> "" limit %s,%s' % (limit_m, limit_n)
        res = mysql_dao.execute(sql)
        if len(res) == 0:
            break
        for r in res:
            try:
                id = r[0]
                url = r[1]
                title = r[2].encode('utf-8')
                headers = Headers.get_headers()
                html = requests.get(url, headers=headers).content
                selector = etree.HTML(html)
                contents = selector.xpath('//div[@id="nr1"]')
                if len(contents) > 0:
                    content = contents[0]
                    content_string = etree.tostring(content, encoding='utf8', method="html").replace('"', '\'')
                    created_at = time.strftime('%Y-%m-%d %H:%M:%S')
                    print(title)
                    sql = 'insert ignore into fiction_content_11 (`chapter_id`,`title`,`content`,`created_at`) values ("%s","%s","%s","%s")' % (
                        id, title, content_string, created_at)
                    mysql_dao.execute(sql)
            except Exception as e:
                print(e)
                print(url)
    limit_m = limit_m + limit_n
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
