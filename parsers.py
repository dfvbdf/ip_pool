from lxml import etree
import re
import settings
import json


class Parser(object):
    def __init__(self, html_queue, redis_cli):
        # spider爬取的原始html页面队列，以(index, html字符串, 页码)格式存储
        self.html_queue = html_queue
        # 解析完成的ip队列， 以（类型， ip端口）的形式存储
        #self.queue = Queue(200)
        # redis连接池
        self.cli = redis_cli

    def parse_xici(self, html_str):
        html = etree.HTML(html_str)
        ip_tr_list = html.xpath('//table[@id="ip_list"]//tr[@class="odd"]')
        for tr in ip_tr_list:
            td_list = tr.xpath('.//td')
            ip_type = td_list[5].text.strip().lower()
            ip = td_list[1].text.strip()+td_list[2].text.strip()
            if ip_type == 'http' or ip_type == 'https':
                ip_info = (ip_type, ip)
                #self.queue.put(ip_info)
                ip_json = json.dumps(ip_info)
                self.cli.lpush(settings.QUALIFIED_QUEUE, ip_json)
                print('西刺代理%s-%s已添加到待验证队列' % (ip_type, ip))

    def parse_kuai(self, html_str):
        html = etree.HTML(html_str)
        ip_list = html.xpath('//table[@class="table table-bordered table-striped"]/tbody//tr')
        for tr in ip_list:
            td_list = tr.xpath('.//td')
            ip_type = td_list[3].text.strip().lower()
            ip = '%s:%s' % (td_list[0].text.strip(),td_list[1].text.strip())
            ip_info = (ip_type, ip)
            # self.queue.put(ip_info)
            ip_json = json.dumps(ip_info)
            self.cli.lpush(settings.QUALIFIED_QUEUE, ip_json)
            print('快代理%s-%s已添加到待验证队列' % (ip_type, ip))

    def parse_six(self, html_str):
        ip_list = re.findall(r'\t+(.*?)<br />', html_str, re.S)
        for ip in ip_list:
            #self.queue.put(('http', ip))
            ip_json = json.dumps(('http', ip))
            self.cli.lpush(settings.QUALIFIED_QUEUE, ip_json)
            print('66代理%s已添加到待验证队列' % ip)

    def run(self):
        methods = [self.parse_xici, self.parse_kuai, self.parse_six]
        while True:
            #html = self.client.spider.raw_html.find_one_and_delete({})
            # 从原始html队列里取出一个
            html_info = self.html_queue.get()
            # 调用index相对应的解析方法, 传入html字符串
            index = html_info[0]
            html_str = html_info[1]
            methods[index](html_str)
