from spiders import Spider
from parsers import Parser
from checkers import Checker
from threading import Thread
import redis
import settings
import sys


def run():
    # 添加项目目录到环境变量
    sys.path.append(settings.BASE_DIR)
    # 连接redis，实例化spider， parse， checker
    redis_cli = redis.Redis(**settings.REDIS_PARAM)
    spider = Spider()
    parser = Parser(spider.queue, redis_cli)
    checher = Checker(redis_cli)
    # 创建并启动线程
    thread_list = [Thread(target=spider.run), Thread(target=parser.run), Thread(target=checher.run)]
    for thread in thread_list:
        thread.start()


if __name__ == '__main__':
    run()
