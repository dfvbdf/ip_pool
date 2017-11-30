from threading import Thread
import time
import requests
import pymysql
import queue

class Clean(object):

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 " \
                          "Safari/537.36 2345Explorer/8.8.3.16721"
        self.mysql_params = {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'dfvbdf11',
                             'db': 'ip_daili'}
        self.check_url = "http://ip.chinaz.com/getip.aspx"
        self.queue = queue.Queue()
        self.conn = pymysql.connect(**self.mysql_params)
        self.cur = self.conn.cursor()

    def put_to_queue(self):
        sql = 'select type,ip,port from checked'
        self.cur.execute(sql)
        for item in self.cur.fetchall():
            self.queue.put(item)
        print('所有数据已添加到队列')

    def handle(self):
        while not self.queue.empty():
            ip_info = self.queue.get()
            p = {ip_info[0].lower(): '%s://%s:%s' % (ip_info[0].lower(), ip_info[1], ip_info[2])}
            try:
                response = requests.get(self.check_url, proxies=p, timeout=3)
            except requests.Timeout:
                print(ip_info, '超时', sep='  --  ')
            except:
                print(ip_info, '异常', sep='  --  ')
            else:
                if response.text != "{ip:'27.212.83.229',address:'山东省淄博市 联通'}":
                    print(ip_info, '正常', response.status_code, response.text, sep='  --  ')

    def run(self):
        for i in range(10):
            t = Thread(target=self.handle)
            t.start()

if __name__ == "__main__":
    c = Clean()
    c.put_to_queue()
    c.run()
