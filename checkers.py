import requests
from threading import Thread
import settings
import json
import time
import random


class Checker(object):
    def __init__(self, redis_cli):
        self.cli = redis_cli
        # 保证不重复的ip
        self.set = set()

    def check(self):
        print('check start')
        while True:
            ip_info = self.cli.lpop(settings.QUALIFIED_QUEUE)
            if not ip_info:
                time.sleep(0.5)
                continue
            ip_type, ip = json.loads(ip_info)
            proxy = {
                ip_type: '%s://%s' % (ip_type, ip)
            }
            headers = {'use-agent': random.choice(settings.USER_AGENTS)}
            try:
                response = requests.get(settings.CHECK_URL, timeout=settings.TIME_OUT, proxies=proxy)
            except requests.RequestException:
                print('ip请求超时', '%s://%s' % (ip_type, ip))
            else:
                if response.status_code == 200:
                    # 将验证通过的ip信息rpush到redis队列
                    self.cli.rpush(settings.QUALIFIED_QUEUE, ip_info)
                    print('%s://%s已验证通过，添加到redis队列' % (ip_type, ip))
                else:
                    print('无效代理')
            time.sleep(settings.TIME_DELTA)

    def run(self):
        for i in range(10):
            t = Thread(target=self.check)
            t.start()





