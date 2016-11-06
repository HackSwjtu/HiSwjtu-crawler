import urllib
from urllib import request
import re
from bs4 import BeautifulSoup
import totClass

data = []

def network():

    req = urllib.request.urlopen('http://dean.swjtu.edu.cn/servlet/WebFileAction?Action=FileMore&kw=&page=1')

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

        url = re.findall(r'<a href=\"(http://.+\.(?:doc|docx|pdf|xml))', item_str)[0]

        file_obj = totClass.File(fileName, fileType, 0, date, downCnt, url)
        # print(file_obj)
        data.append(file_obj)

    for _ in data:
        print (_)



if __name__ == "__main__":
    network()

