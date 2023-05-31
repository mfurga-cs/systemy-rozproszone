#!/usr/bin/env python3

import pika
import sys
import uuid

EXCHANGE = "exchange"
EXCHANGE_TYPE = "direct"

QUEUES = [
  "cargo",
  "people",
  "satellite"
]

COLLERATION_ID = str(uuid.uuid4())

def callback(channel, method, properties, body):
  print("Response: %s" % body.decode())

def main(name, order_id, order_type):
  connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost"))
  channel = connection.channel()

  # Create private queue for response
  queue = channel.queue_declare(queue="", exclusive=True)
  channel.basic_consume(queue=queue.method.queue,
                        on_message_callback=callback,
                        auto_ack=True)

  # Send order
  channel.basic_publish(exchange=EXCHANGE,
                        routing_key=order_type,
                        properties=pika.BasicProperties(
                          reply_to=queue.method.queue,
                          correlation_id=COLLERATION_ID,
                        ),
                        body="%s|%s" % (name, order_id),
                        mandatory=True)

  # Wait for response
  connection.process_data_events(time_limit=None)

  channel.close()
  connection.close()

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print("Usage: %s <agency_name> <order_id> <cargo|people|satellite>")
    sys.exit(1)

  name = sys.argv[1]
  order_id = sys.argv[2]
  order_type = sys.argv[3]

  if order_type not in QUEUES:
    print("Invalid order type")
    sys.exit(1)

  main(name, order_id, order_type)

