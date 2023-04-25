#!/usr/bin/env python3

import sys
import time
import grpc
import logging

from common_pb2 import Empty, Location

from tempsensor_pb2 import (
  TempSensor,
  ListResponse,
  GetRequest
)

from tempsensor_pb2_grpc import (
  TempSensorServiceServicer,
  TempSensorServiceStub,
  add_TempSensorServiceServicer_to_server
)

from lightswitch_pb2 import (
  LightSwitch,
  ListResponse,
  Request
)

from lightswitch_pb2_grpc import (
  LightSwitchServiceServicer,
  LightSwitchServiceStub,
  add_LightSwitchServiceServicer_to_server
)

from furnace_pb2 import Furnace

from furnace_pb2_grpc import (
  FurnaceServiceServicer,
  FurnaceServiceStub,
  add_FurnaceServiceServicer_to_server
)

def tempSensorList(stub):
  tempSensors = stub.List(Empty()).sensors
  print("ID\tLocation\tDegree")
  print("-" * 30)
  for sensor in tempSensors:
    location = Location.Name(sensor.location)
    print(f"{sensor.id: <8}{location: <16}{sensor.temperature}")

def tempSensorGet(stub, id):
  try:
    sensor = stub.Get(GetRequest(id=id))
    location = Location.Name(sensor.location)
    print(f"{sensor.id: <8}{location: <16}{sensor.temperature}")
  except grpc.RpcError as exp:
    print(exp.code(), exp.details())

def lightSwitchList(stub):
  lightSwitches = stub.List(Empty()).lightSwitches
  lightSwitches = sorted(lightSwitches, key=lambda s: s.id)
  print("ID\tLocation\tState")
  print("-" * 30)
  for switch in lightSwitches:
    location = Location.Name(switch.location)
    print(f"{switch.id: <8}{location: <16}{switch.state}")

def lightSensorGet(stub, id):
  try:
    switch = stub.Get(Request(id=id))
    location = Location.Name(switch.location)
    print(f"{switch.id: <8}{location: <16}{switch.state}")
  except grpc.RpcError as exp:
    print(exp.code(), exp.details())

def lightSensorToggle(stub, id):
  try:
    stub.Toggle(Request(id=id))
  except grpc.RpcError as exp:
    print(exp.code(), exp.details())

def furnaceGet(stub):
  furnace = stub.Get(Empty())
  state = "YES" if furnace.isWorking else "NO"
  print(f"Temperature: {furnace.currentTemp: <4}Working: {state}")

def furnaceSet(stub, temp, working):
  furnace = Furnace(currentTemp=temp, isWorking=working)
  stub.Set(furnace)

def main():
  if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
    sys.exit(1)

  host = sys.argv[1]
  port = sys.argv[2]

  with grpc.insecure_channel(f"{host}:{port}") as channel:
    tempSensorStub = TempSensorServiceStub(channel)
    lightSwitchStub = LightSwitchServiceStub(channel)
    furnaceStub = FurnaceServiceStub(channel)

    while True:
      comm = input("> ").strip().split(" ")
      args = []

      if len(comm) > 1:
        args = comm[1:]
      comm = comm[0]

      match comm:
        case "temp.list":
          tempSensorList(tempSensorStub)

        case "temp.get":
          if len(args) == 0:
            continue
          tempSensorGet(tempSensorStub, int(args[0]))

        case "light.list":
          lightSwitchList(lightSwitchStub)

        case "light.get":
          if len(args) == 0:
            continue
          lightSensorGet(lightSwitchStub, int(args[0]))

        case "light.toggle":
          if len(args) == 0:
            continue
          lightSensorToggle(lightSwitchStub, int(args[0]))

        case "furnace.get":
          furnaceGet(furnaceStub)

        case "furnace.set":
          furnaceSet(furnaceStub, int(args[0]), args[1] == "1")

        case "":
          pass

        case _:
          print("Bad command!")

if __name__ == "__main__":
  logging.basicConfig()
  main()

