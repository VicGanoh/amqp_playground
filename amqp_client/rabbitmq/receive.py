import pika

connection_param = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(connection_param)
channel = connection.channel()

channel.queue_declare(queue="hello")

# callback function to handle incoming messages
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# start consuming messages
channel.basic_consume(
    queue="hello",
    auto_ack=True,
    on_message_callback=callback,
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

