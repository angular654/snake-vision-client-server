import pika


class MessagesController:
    connection = ""
    channel = ""
    def __init__(self):
        self.__init_connection()

    def __init_connection(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=5672))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='models-logs')

    def push_message(self, msg: str):
        self.__init_connection()
        self.channel.basic_publish(exchange='', routing_key='models-logs', body=f'{msg}')
        self.connection.close()
