#!/usr/bin/env python3

from concurrent import futures
from threading import Thread
import grpc
import time

from common_pb2 import Empty, Location

from tempsensor_pb2_grpc import (
  TempSensorServiceServicer,
  add_TempSensorServiceServicer_to_server
)

from tempsensor_pb2 import (
  TempSensor,
  ListResponse
)

SERVER1_PORT = "50051"
SERVER2_PORT = "50052"

class TempSensorService(TempSensorServiceServicer):

  def __init__(self):
    self.sensors = [
      TempSensor(id=1, location=Location.LIVINGROOM, temperature=10)
    ]

  def Get(self, request, context):
    result = [sensor for sensor in self.sensors if sensor.id == request.id]

    if len(result) == 0:
      context.set_code(grpc.StatusCode.NOT_FOUND)
      return GetResponse()
    else:
      return result[0]

  def List(self, request, context):
    return ListResponse(sensors=self.sensors)

def main():
  tempSensorService = TempSensorService()

  server1 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  server2 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

  add_TempSensorServiceServicer_to_server(tempSensorService, server1)
  add_TempSensorServiceServicer_to_server(tempSensorService, server2)

  server1.add_insecure_port("[::]:" + SERVER1_PORT)
  server1.start()

  server2.add_insecure_port("[::]:" + SERVER2_PORT)
  server2.start()

  print("Server 1 started, listening on " + SERVER1_PORT)
  print("Server 2 started, listening on " + SERVER2_PORT)

  server1.wait_for_termination()
  server2.wait_for_termination()

if __name__ == '__main__':
  main()

