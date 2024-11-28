import pika

connection_param = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(connection_param)
channel = connection.channel()

channel.queue_declare(queue="hello")