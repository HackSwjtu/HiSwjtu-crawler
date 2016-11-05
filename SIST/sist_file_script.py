import requests
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1',
                       user='localhost',
                       passwd='123456',
                       db='swjtu',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

sql = '''CREATE TABLE if NOT EXISTS xinxi(
  fileName CHAR(50) NOT NULL ,
  fileType CHAR(30),
  filesize CHAR(20),
  date DATETIME NOT NULL ,
  url CHAR(80) NOT NULL
) CHARSET=utf8;'''

cursor.execute(sql)
conn.commit()

headers = {

    'Referer': 'http://sist.swjtu.edu.cn/download.do?action=file',
    'Host': 'sist.swjtu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; /'
                 'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) /'
                 'Chrome/53.0.2785.143 Safari/537.36',
}

class crawler(object):

    # #设置每12小时爬取一次
    # def sleep_time(self):
    #     sleep = time.sleep(12 * 60 * 60)
    #     return sleep

    # 存储数据到mysql
    def save(self, tmp_info):
        for item in tmp_info:
            date = item['date']
            title = item['title']
            link = item['link']
            print(date, title, link)
            sql = 'INSERT INTO xinxi(fileName, date, url) VALUES ("%s", "%s", "%s")' % (title, date, link)
            cursor.execute(sql)
            conn.commit()
        print('all saved!')


    #爬虫主函数
    def craw(self, start_url):

        #有异常时抛出错误并继续执行
        try:
            html = requests.get(start_url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            info = soup.select('#rightPageContent > dl > dd')
            tmp_info = []
            for item in info:
                date = item.select('span')[0].text
                title = item.select('div a')[0].text
                link = item.select('div a')[0].get('href')
                # print(date, title, link)
                data = {
                    'date': date,
                    'title': title,
                    'link': link,
                }
                tmp_info .append(data)
            #保存数据到数据库
            self.save(tmp_info)

        except Exception as e:
            print(e)

#启动爬虫
if __name__ == "__main__":
    start_url = 'http://sist.swjtu.edu.cn/download.do?action=file&navId=55'
    xinxi = crawler()
    xinxi.craw(start_url)
