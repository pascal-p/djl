import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ya_ms_admin.settings")
django.setup()

# with two lines above, we can now import Product
from ya_products.models import Product

## root (Django) project - consuming from 'admin_q' queue
# params = pika.URLParameters('amqp://corto:B@merSalEe@host.docker.internal.localhost:5672/')
rmq_host = os.environ['RMQ_HOST']
credentials = pika.PlainCredentials('corto', 'B@merSalEe')
params = pika.ConnectionParameters(rmq_host,  # 'host.docker.internal.localhost',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin_q', durable=True)


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(f' id: {id}')
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print(f' Product likes increased! => {product.likes}')
    return

channel.basic_consume(queue='admin_q',
                      on_message_callback=callback,
                      auto_ack=True)
print('Started Consuming / (root) Admin side...')
channel.start_consuming()

channel.close()
