#!/usr/bin/env python3

import pika
import sys
import time

EXCHANGE = "exchange"
EXCHANGE_TYPE = "direct"

QUEUES = [
  "cargo",
  "people",
  "satellite"
]

def callback(channel, method, properties, body):
  agency_name, order_id = body.decode().split("|")

  print(
    "Order received:\n"
    "  type       : %s\n"
    "  order id   : %s\n"
    "  agency name: %s\n"
    "running ... "
    % (method.routing_key, order_id, agency_name), end="")

  time.sleep(1)

  print("done", end="\n\n")
  channel.basic_ack(delivery_tag=method.delivery_tag,
                    multiple=False)

def main(name, order_types):
  connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost"))

  # Create channel
  channel = connection.channel()
  channel.basic_qos(prefetch_count=1)

  # Create exchange
  channel.exchange_declare(exchange=EXCHANGE,
                           exchange_type=EXCHANGE_TYPE)

  for order_type in order_types:
    # Create queue
    channel.queue_declare(queue=order_type, exclusive=False)

    # Bind queue
    channel.queue_bind(order_type, EXCHANGE, order_type)

    # Receive on queue
    channel.basic_consume(queue=order_type,
                          on_message_callback=callback,
                          auto_ack=False)

  print("Carrier %r waiting for %r, %r ..." % (name, *order_types))
  channel.start_consuming()

  channel.close()
  connection.close()

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print(
      "%s <carrier name> "
      "<cargo|people|satellite> <cargo|people|satellite>"
      % sys.argv[0])
    sys.exit(1)

  name = sys.argv[1]
  order_type_1 = sys.argv[2]
  order_type_2 = sys.argv[3]

  if order_type_1 not in QUEUES or order_type_2 not in QUEUES:
    print("Invalid order type")
    sys.exit(1)

  main(name, (order_type_1, order_type_2))

