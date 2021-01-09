import pika, json

## main app - Producing on 'admin' queue ==> product/side

params = pika.URLParameters('amqp://corto:B@merSalEe@host.docker.internal.localhost:5672/')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='ya_mservice_exc', routing_key='admin',
                          body=json.dumps(body),
                          properties=properties)
