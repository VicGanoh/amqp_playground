import json
from typing import Any
import pika
import time


class OrderPublisher:
    def __init__(self):
        self.connect_with_retry()

    def connect_with_retry(self, max_retries=5, retry_delay=5):
        """Attempt to connect to RabbitMQ with retries"""
        for attempt in range(max_retries):
            try:
                # Initialize RabbitMQ connection with Docker container settings
                credentials = pika.PlainCredentials("guest", "guest")
                parameters = pika.ConnectionParameters(
                    host='localhost',
                    port=5672,
                    virtual_host='/',
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()

                # Declare the topic exchange
                self.exchange_name = "order_events"
                self.channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type="topic",
                    durable=True
                )
                print(" [*] Successfully connected to RabbitMQ")
                return

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f" [!] Connection failed: {e}")
                    print(f" [!] Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(" [!] Failed to connect to RabbitMQ after multiple attempts")
                    raise

    def publish_order_event(self, order_data: dict[str, Any], event_type: str):
        """
        Publish order events with different routing keys based on event type (e.g. "order.created", "order.updated", "order.cancelled")
        """
        try:
            # Create routing key based on event type category
            routing_key = f"order.{event_type}.{order_data['category']}"

            # Convert order data to JSON
            message = json.dumps(order_data)

            # Publish message with persistance
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2, # make delivery persistent
                    content_type="application/json",
                    content_encoding="utf-8"
                )
            )
            print(f"\n Published: {routing_key}")
            print(f"Message: {message}")
        except Exception as e:
            print(f"Error publishing order event: {e}")
    
    def close(self):
        self.connection.close()

# test the system with multiple scenarios
if __name__ == "__main__":
    publisher = OrderPublisher()

    # case 1: new electronics order
    # order1 = {
    #     "order_id": "1",
    #     "category": "electronics",
    #     "product": "Smartphone",
    #     "price": "GHS 999.99",
    #     "email": "johndoe@mail.com"
    # }
    # publisher.publish_order_event(order1, "created")

    # # case 2: new clothing order
    # order2 = {
    #     "order_id": "2",
    #     "category": "clothing",
    #     "product": "T-Shirt",
    #     "price": "GHS 39.99",
    #     "email": "marydoe@mail.com"
    # }
    # publisher.publish_order_event(order2, "created")

    # case 3: Cancelled Order
    order3 = {
        "order_id": "1",
        "category": "electronics",
        "product": "Smartphone",
        "price": "GHS 999.99",
        "email": "johndoe@mail.com"
    }
    publisher.publish_order_event(order3, "cancelled")
    
    publisher.close()