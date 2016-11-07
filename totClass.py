import time
# from SIST.sist_file_script import crawler
import sys

defaultencoding = 'utf-8'

if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class File:
    fileName = ''
    fileType = ''
    fileSize = 0.0
    date = time.strftime("%Y-%m-%d", time.localtime())
    downCnt = 0
    url = ''

    def __init__(self, fn, ft, fs, da, dc, url):
        self.fileName = fn
        self.fileType = ft
        self.fileSize = fs
        self.date = da
        self.downCnt = dc
        self.url = url

    def __str__(self):
        res = 'Name: ' + self.fileName + '\n'
        if len(self.fileType) > 0:
            res = res + 'Type: ' + self.fileType + '\n'
        res += 'Size: ' + str(self.fileSize) + '\n'
        res += 'Date: ' + str(self.date) + '\n'
        res += 'Count: ' + str(self.downCnt) + '\n'
        res += 'URL: ' + str(self.url) + '\n'
        return  res

    def __repr__(self):
        res = 'Name: ' + self.fileName + '\n'
        if len(self.fileType) > 0:
            res = res + 'Type: ' + self.fileType + '\n'
        res += 'Size: ' + str(self.fileSize) + '\n'
        res += 'Date: ' + str(self.date) + '\n'
        res += 'Count: ' + str(self.downCnt) + '\n'
        res += 'URL: ' + str(self.url) + '\n'
        return  res

    #for xinxi files
    def xinxiCrawler(self):
        xinxi = crawler()
        fileXinxi = xinxi.craw()
        return fileXinxi
