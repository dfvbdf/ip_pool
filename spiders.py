import requests
import settings
import random
import time
from threading import Thread
import queue

# 用于爬取代理
class Spider(object):
    def __init__(self):
        # self.client = pymongo.MongoClient()
        # 用于存储html信息,格式为(index, html字符串,页码)元组
        self.queue = queue.Queue(50)

# 西刺代理爬取
    def xici_crawler(self):
        # 循环遍历爬取所有页面
        for page in range(1, 2700):
            str_page = str(page)
            url = 'http://www.xicidaili.com/nn/' + str_page
            user_agent = random.choice(settings.USER_AGENTS)
            try:
                response = requests.get(url, headers={'User-Agent': user_agent}, timeout=settings.TIME_OUT)
            except requests.RequestException as e:
                print('西刺代理第%s页请求失败' % page, e)
            else:
                if response.status_code != 200:
                    print('西刺代理第%s页请求失败' % page, response.status_code)
                else:
                    print('西刺代理第%s页已爬取完成' % page)
                html = response.text
                # 保存到MongoDB，唯一标识_id为url
                #self.mongo.save_html(0, {'_id': url, 'html': html})
                # 以网站代号, 页面html代码，页码的元组格式传入队列
                self.queue.put((0, html, str_page))
            # 爬完一个页面等待的秒数
            time.sleep(settings.TIME_DELTA)

    # 快代理爬取
    def kuai_crawler(self):
        for page in range(1, 2180):
            str_page = str(page)
            url = 'https://www.kuaidaili.com/free/inha/' + str_page
            user_agent = random.choice(settings.USER_AGENTS)
            try:
                response = requests.get(url, headers={'User-Agent': user_agent}, timeout=settings.TIME_OUT, verify=False)
            except requests.RequestException as e:
                print('快代理第%s页请求失败' % page, e)
            else:
                if response.status_code != 200:
                    print('快代理第%s页请求失败' % page, response.status_code)
                else:
                    print('快代理第%s页已爬取完成' % page)
                html = response.text
                # self.client.spider.raw_html.save({'_id': url, 'html': html, 'web': 1, 'page': page})
                self.queue.put((1, html, str_page))
            # 爬完一个页面等待的秒数
            time.sleep(settings.TIME_DELTA)

    # 66代理爬取
    def six_crawler(self):
        page = 1
        while True:
            url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=10&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
            user_agent = random.choice(settings.USER_AGENTS)
            try:
                response = requests.get(url, headers={'User-Agent': user_agent}, timeout=settings.TIME_OUT)
            except requests.RequestException as e:
                print('66代理第%s次请求失败' % page, e)
            else:
                if response.status_code != 200:
                    print('66代理第%s页请求失败' % page, response.status_code)
                else:
                    print('66代理第%s次已爬取完成' % page)
                html = response.text
                # self.client.spider.raw_html.save({'_id': url, 'html': html, 'web': 2, 'page': page})
                self.queue.put((2, html, str(page)))
            page += 1
            # 爬完一个页面等待的秒数
            time.sleep(settings.TIME_DELTA)

# 启动
    def run(self):
        # 根据设置启动相应数量的任务数
        process_list = [Thread(target=self.xici_crawler), Thread(target=self.kuai_crawler), Thread(target=self.six_crawler)]
        for process in process_list:
            process.start()
