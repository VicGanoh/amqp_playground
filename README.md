# RabbitMQ Messaging Example

This project demonstrates a simple work queue using RabbitMQ and Python's Pika library. It includes a producer that sends tasks and a worker that processes them.

- **Producer (Sender)**: The producer encapsulates tasks as messages and sends them to a queue.
- **Worker (Consumer)**: The worker processes these tasks. To handle resource-intensive tasks efficiently, the workload is distributed among multiple workers (consumers).

### Prerequisites
- Python 3.x
- RabbitMQ server

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/vicganoh/amqp_playground.git
   cd amqp_playground
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start RabbitMQ with Docker

1. Pull the RabbitMQ Docker image:
   ```bash
   docker pull rabbitmq:4.0-management
   ```

2. Run the RabbitMQ container:
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
   ```

   - The RabbitMQ management interface will be available at `http://localhost:15672` with the default username and password (`guest`/`guest`).

### Run the Worker and Producer

1. Run the worker:
   ```bash
   python amqp_client/rabbitmq/work_queues/worker.py
   ```

2. Run the producer (in a separate terminal):
   ```bash
   python amqp_client/rabbitmq/work_queues/new_task.py
   ```

## Testing

To test the project, you can send tasks using the producer and observe the worker processing them.

## Configuration

Ensure RabbitMQ is running on `localhost` with default settings. Modify `worker.py` if your setup differs.
