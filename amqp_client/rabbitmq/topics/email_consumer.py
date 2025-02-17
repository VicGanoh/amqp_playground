from asyncio import Queue
import pika
import json
import time

class EmailConsumer:
    def __init__(self):
        self.connect_with_retry()

    def connect_with_retry(self, max_retries=5, retry_delay=5):
        """Attempt to connect to RabbitMQ with retries"""
        for attempt in range(max_retries):
            try:
                # Initialize RabbitMQ connection and channel
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host="localhost")
                )
                self.channel = self.connection.channel()

                # Declare exchange with consistent settings
                self.exchange_name = "order_events"
                self.channel.exchange_declare(
                    exchange=self.exchange_name, 
                    exchange_type="topic",
                    durable=True  # Make sure this matches the publisher
                )

                result = self.channel.queue_declare(
                    queue="email_notifications", 
                    durable=True
                )
                self.queue_name = result.method.queue

                # Bind queue to exchange with specific routing key
                binding_keys = [
                    "order.created.*",
                    "order.updated.*",
                    "order.cancelled.*",
                ]

                for binding_key in binding_keys:
                    self.channel.queue_bind(
                        queue=self.queue_name,
                        exchange=self.exchange_name,
                        routing_key=binding_key
                    )

                print(" [*] Successfully connected to RabbitMQ")
                print(" [*] Waiting for order events. To exit press CTRL+C")
                return

            except pika.exceptions.AMQPConnectionError:
                if attempt < max_retries - 1:
                    print(f" [!] Connection failed. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(" [!] Failed to connect to RabbitMQ after multiple attempts")
                    raise
    
    def simulate_email_sending(
            self, to_email: str, subject: str, body: str
    ):
       """Simulate email sending with a delay"""
       print(f"\n📧 Sending email to: {to_email}")
       print(f"Subject: {subject}")
       print(f"Content: {body}")
       time.sleep(1)  # Simulate email sending delay
       print("✅ Email sent successfully!")
    
    def process_message(
            self, ch, method, properties, body
    ):
        try:
            # Parse message body as JSON
            data = json.loads(body)
            routing_key = method.routing_key
            event_type = routing_key.split(".")[1]

            # Prepare email content based on event type
            if event_type == "created":
                subject = "Order Confirmation"
                body = f"Thank you for ordering {data['product']}! Your order (ID: {data['order_id']}) has been confirmed."
            elif event_type == "updated":
                subject = "Order Updated"
                body = f"The order with ID: {data['order_id']} has been updated."
            elif event_type == "cancelled":
                subject = "Order Cancelled"
                body = f"The order with ID: {data['order_id']} has been cancelled."
            else:
                print(f" [!] Unknown event type: {event_type}")
                return

            # Simulate sending email
            self.simulate_email_sending(
                to_email=data["email"],
                subject=subject,
                body=body
            )

            # Acknowledge message processing
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        # set prefetch count to 1 to ensure messages are processed sequentially
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message
        )
        print(" [*] Email consumer is running. Press CTRL+C to stop.")
        self.channel.start_consuming()

if __name__ == "__main__":
    try:
        consumer = EmailConsumer()
        consumer.start_consuming()
    except KeyboardInterrupt:
        print(" [*] Email consumer interrupted. Exiting...")
    except Exception as e:
        print(f" [!] Error: {e}")
