import os, pika, json

## main app - Producing on 'admin' queue ==> product/side

# params = pika.URLParameters('amqp://corto:B@merSalEe@host.docker.internal.localhost:5672/')
rmq_host = os.environ['RMQ_HOST']
credentials = pika.PlainCredentials('corto', 'B@merSalEe')
params = pika.ConnectionParameters(rmq_host,
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='ya_mservice_exc',
                          routing_key='admin',
                          body=json.dumps(body),
                          properties=properties)
