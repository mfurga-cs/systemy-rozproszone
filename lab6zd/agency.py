#!/usr/bin/env python3

import pika
import sys

EXCHANGE = "exchange"
EXCHANGE_TYPE = "direct"

QUEUES = [
  "cargo",
  "people",
  "satellite"
]

def main(name, order_id, order_type):
  connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost"))
  channel = connection.channel()

  channel.basic_publish(exchange=EXCHANGE,
                        routing_key=order_type,
                        body="%s|%s" % (name, order_id),
                        mandatory=True)

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

