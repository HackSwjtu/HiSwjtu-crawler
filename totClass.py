import time

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
        print ('Name: ' + self.fileName)
        if len(self.fileType) > 0:
            print ('Type: ' + self.fileType)
        print ('Size: ' + str(self.fileSize))
        print ('Date: ' + str(self.date))
        print ('Count: ' + str(self.downCnt))
        print ('URL: ' + self.url)


