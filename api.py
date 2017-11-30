from flask import Flask
import json
import redis
import settings

app = Flask(__name__)
redis_client = redis.Redis(**settings.REDIS_PARAM)


@app.route('/')
def ip():
    result = redis_client.rpop(settings.QUALIFIED_QUEUE)
    if not result:
        return 'ip队列为空！'
    ip_info = json.loads(result)
    print(ip_info)
    return ip_info


if __name__ == '__main__':
    app.run(port=8000)