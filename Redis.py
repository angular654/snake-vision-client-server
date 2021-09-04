import redis

class Redis:
    client = ''
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=0)
    def send_data(self, data: str):
        self.client.publish('logger',data)