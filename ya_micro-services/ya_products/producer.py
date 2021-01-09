import pika, json

## product/side - Producing on 'main' queue ==> main-app side
## send message whenever product is created/updated/deleted

params = pika.URLParameters('amqp://corto:B@merSalEe@host.docker.internal.localhost:5672/')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='ya_mservice_exc', routing_key='main',
                          body=json.dumps(body),
                          properties=properties)
