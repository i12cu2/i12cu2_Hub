import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading
class P(threading.Thread):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}
    def __init__(self, qu, pu, *args, **kwargs):
        super(P, self).__init__(*args, **kwargs)
        self.qu = qu
        self.pu = pu
    def run(self):
        while True:
            if self.qu.empty():
                break
            url = self.qu.get()
            self.parse_page(url)
    def parse_page(self,url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            a = re.sub(r'[\?？\.。!，！\*]', '',alt)                                                 #对文件命名格式的加工避免出错
            suffix = os.path.splitext(img_url)[1]
            # filename = a + suffix                                                                       #最终加工后的图片名
            # self.pu.put((img_url, filename))
            filename = alt + '.jpg'                                                                       #最终加工后的图片名
            self.pu.put((img_url, filename))
class C(threading.Thread):
    def __init__(self, qu, pu, *args, **kwargs):
        super(C, self).__init__(*args, **kwargs)                                              #避免输入错误 加入字典
        self.qu = qu
        self.pu = pu
    def run(self):
        while True:
            if self.pu.empty() and self.qu.empty():                                      #尽头停止
                break
            img_url,filename = self.pu.get()
            request.urlretrieve(img_url,'images/'+filename)
            print( "已下载"+filename )                                                               #对已经下好的文件进行输出回馈
def main():
    qu = Queue(100)
    pu = Queue(100)
    for x in range(1, 101):                                                                             #代码网址换页
        url = 'http://www.doutula.com/photo/list/?page=%d' % x
        qu.put(url)
    for x in range(5):
        t =P(qu,pu)
        t.start()
    for x in range(5):
        t = C(qu,pu)
        t.start()
if __name__ == '__main__':
    main()