import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


channel.exchange_declare(exchange="logs", exchange_type="fanout") # fanout means the message will be broadcast to all the queues bound to it

result = channel.queue_declare(queue="", exclusive=True) # exclusive=True means the queue will be deleted when the connection is closed
queue_name = result.method.queue # get the queue name

channel.queue_bind(exchange="logs", queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
