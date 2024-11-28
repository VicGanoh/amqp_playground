import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue")

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b"."))
    print(" [x] Done")

channel.basic_consume(
    queue="task_queue",
    auto_ack=True,
    on_message_callback=callback,
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
