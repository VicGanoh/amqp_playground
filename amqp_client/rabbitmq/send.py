import pika

# establish connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))