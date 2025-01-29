import pika

class Publisher:
    def __init__(self):
        # Step 1: Initialize connection parameters
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

        # Step 2: Declare the topic exchange
        self.exchange_name = "order_events"
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type="topic",
            durable=True
        )
    