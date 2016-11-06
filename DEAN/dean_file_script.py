import urllib
from urllib import request
import re
from bs4 import BeautifulSoup
import totClass

data = []

def checkTheMaxPage():
    url = 'http://dean.swjtu.edu.cn/servlet/WebFileAction?Action=FileMore'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Connection': 'keep-alive'
    }
    req = request.Request(url, headers = headers)
    html = request.urlopen(req).read()
    MaxPage = re.findall(r'var allPage = \"([0-9]{1,3})\"', str(html))[0]

    return int(MaxPage)


def crawler(maxPage):
    for i in range(1, maxPage):

        req = urllib.request.urlopen('http://dean.swjtu.edu.cn/servlet/WebFileAction?Action=FileMore&kw=&page=' + str(i))


        html = req.read()
        soup = BeautifulSoup(html, 'html.parser')

        res = soup.find_all("", {"class":"listLinkIndexNewsRule"})
        for ind in res:
            item_str = str(ind)
            fileName = ind.find("a").text
            _str = re.findall(r'【(.*?)】', item_str)
            fileType = _str[0]
            cntAndDate = _str[1]

            downCnt = re.findall(r'查看:(\d+)', cntAndDate)[0]
            date = re.findall(r'\d\d\d\d-\d\d-\d\d', cntAndDate)[0]

            url = re.findall(r'<a href=\"(http://.+\.(?:doc|docx|pdf|xml))', item_str)
            if (len(url) > 0):
                file_obj = totClass.File(fileName, fileType, 0, date, downCnt, url[0])
            # print(file_obj)
            data.append(file_obj)

    for _ in data:
        print (_)

    print('一共 ', str(len(data)), ' 条数据')


if __name__ == "__main__":
    maxPage = checkTheMaxPage()
    crawler(maxPage)

