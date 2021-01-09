import pika, json
from main import Product, db

## main (Flask) app - consuming from 'main' queue

params = pika.URLParameters('amqp://corto:B@merSalEe@host.docker.internal.localhost:5672/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main_q', durable=True)


def callback(ch, method, properties, body):
    print('Received in main app')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'],
                          image=data['image'])
        db.session.add(product)
        db.session.commit()
        print(f"Product {data['id']} Created")

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print(f"Product {data['id']} Updated")

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print(f"Product {data['id']} Deleted")
    return


channel.basic_consume(queue='main_q', on_message_callback=callback,
                      auto_ack=True)
print('Started Consuming / main App side...')
channel.start_consuming()

channel.close()
