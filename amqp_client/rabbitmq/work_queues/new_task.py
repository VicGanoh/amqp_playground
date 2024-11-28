import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)

channel.exchange_declare(exchange="task_fanout", exchange_type="fanout")

message = " ".join(sys.argv[1:]) or "Hello, World!"

channel.basic_publish(
    exchange="task_fanout",
    routing_key="",
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,
    ),
)

print(f" [x] Sent {message}")

connection.close()
