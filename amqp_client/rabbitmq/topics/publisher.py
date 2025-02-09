import json
from typing import Any
import pika

class OrderPublisher:
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
        except Exception as e:
            print(f"Error publishing order event: {e}")
    
    def close(self):
        self.connection.close()