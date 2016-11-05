import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import totClass

data = []

def main():
    req = urllib2.urlopen('http://dean.swjtu.edu.cn/servlet/WebFileAction?Action=FileMore&kw=&page=1')
    html = req.read()

    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find_all("", {"class":"listLinkIndexNewsRule"})
    for ind in res:
        item_str = str(ind)
        # print item
        fileName = ind.find("a").text
        _str = re.findall(r'\xe3\x80\x90(.*?)\xe3\x80\x91', item_str)
        fileType = _str[0]
        cntAndDate = _str[1]
        downCnt = re.findall(r'\xe6\x9f\xa5\xe7\x9c\x8b:(\d+)', cntAndDate)[0]
        date = re.findall(r'\d\d\d\d-\d\d-\d\d', cntAndDate)[0]

        url = re.findall(r'<a href=\"(http://.+\.(?:doc|docx|pdf|xml))', item_str)[0]

        file_obj = totClass.File(fileName, fileType, 0, date, downCnt, url)
        data.append(file_obj)
        # print item_str

    for _ in data:
        print _



if __name__ == '__main__':
    main()


