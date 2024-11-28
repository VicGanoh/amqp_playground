import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="task_exchange", exchange_type="fanout")

channel.queue_declare(queue="task_queue", durable=True)

channel.queue_bind(exchange="task_exchange", queue="task_queue")

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b"."))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue="task_queue",
    auto_ack=True,
    on_message_callback=callback,
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
