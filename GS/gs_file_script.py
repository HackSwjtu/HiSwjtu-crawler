# coding: utf-8
# !usr/bin/env python

import pymysql
import requests
import re
from bs4 import BeautifulSoup


class gs(object):

    def __init__(self, db_info):
        self.file_list_url = 'http://gs.swjtu.edu.cn/ucenter/public/sheet/list_item/pmt_article_file'
        self.exist_file_set = set()  # 已爬取文件url
        self.db_info = db_info  # 数据库信息
        self.conn = None  # 数据库连接对象
        self.cur = None  # 数据库光标对象
        self.headers = {
            'Host': 'gs.swjtu.edu.cn',
            'Referer': 'http://gs.swjtu.edu.cn/ws/gs/di',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        self.data = {
            'w_l_title': '',
            'page_size': '20',
            'data_orderby': '',
            'data_orderbymethod': '',
            'page_index': ''
        }

    def get_exist_file(self, get_page):

        # 从数据库中获取已爬取文件列表, 回调 get_page
        #  :return: 已爬取文件url集合

        sql = "SELECT url FROM gs;"
        self.cur.execute(sql)
        url_list = self.cur.fetchall()
        self.conn.commit()
        for url in url_list:
            self.exist_file_set.add(url[0])

        return get_page(self.get_file)

    def get_page(self, get_file):

        #  获取最大页数， 回调 get_url
        #  :return: 返回最大页数

        data = self.data
        data['page_index'] = '1'
        r = requests.session()
        res = r.post(self.file_list_url, headers=self.headers, data=data)
        max_page = re.search('共(\d)页', res.text).group(1)

        return get_file(max_page)

    def get_file(self, max_page):

        #  遍历每页文件列表，并保存到数据库
        #  :param max_page: 最大页数
        #  :param save: save函数，保存到数据库
        #  :return: 文件信息列表，元素为字典

        data = self.data
        file = []
        r = requests.session()
        # 遍历每个文件下载列表页面
        for i in range(1, int(max_page) + 1):
            data['page_index'] = i
            res = r.post(self.file_list_url, headers=self.headers, data=data)
            res = BeautifulSoup(res.text, 'lxml')
            # 遍历下载页面中的每个文件
            for one in res.find_all('div', {'class': 'down_list'}):
                url = 'http://gs.swjtu.edu.cn' + one.find('a', {'target': '_blank'}).attrs['href']
                # 文件查重
                if url in self.exist_file_set:
                    continue
                title = one.find('div', {'class': 'title'}).text
                info_div = one.find('div', {'class': 'remark'})
                file_type = info_div.span.text
                time = re.search('(?<=发布时间：)\d{4}-\d{2}-\d{2}', info_div.text).group(0)
                dnt = re.search('(?<=下载次数：)\d*', info_div.text).group(0)
                file.append(
                    {
                        'title': title,
                        'url': url,
                        'type': file_type,
                        'time': time,
                        'dnt': dnt
                    }
                )

        # 保存到数据库, gs表列为 file_id, fileName, fileType, fileSize, date. url

        # 数据插入
        sql = 'INSERT gs VALUES(DEFAULT, %s, %s, 0, %s, %s)'
        for one in file:
            self.cur.execute(sql, (one['title'], one['type'], one['time'], one['url']))
            self.conn.commit()
        print('新增%s条记录' % len(file))

    def start(self):

        # 数据库连接
        self.conn = pymysql.connect(**self.db_info)
        self.cur = self.conn.cursor()
        try:
            sql = '''CREATE TABLE IF NOT EXISTS `gs` (
      `file_id` int(11) NOT NULL AUTO_INCREMENT,
      `fileName` varchar(100) NOT NULL,
      `fileType` varchar(50) DEFAULT NULL,
      `fileSize` varchar(30) DEFAULT NULL,
      `date` datetime DEFAULT NULL,
      `url` varchar(80) DEFAULT NULL,
      PRIMARY KEY (`file_id`),
      UNIQUE KEY `url_UNIQUE` (`url`)
    ) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8;'''
            self.cur.execute(sql)
            self.conn.commit()
            # 开始爬取
            self.get_exist_file(self.get_page)
        finally:
            # 连接关闭
            self.cur.close()
            self.conn.close()

if __name__ == '__main__':
    # 数据库信息
    default_db_info = {'host': 'localhost', 'user': 'root', 'passwd': '12345678', 'db': 'swjtu', 'charset': 'utf8'}
    test = gs(default_db_info)
    test.start()

