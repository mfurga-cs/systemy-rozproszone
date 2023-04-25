import sys, Ice

import Demo
import pickle

import IcePy

#def main():

with Ice.initialize(sys.argv) as communicator:
  proxy = communicator.stringToProxy(
    "invoke/invoke:tcp -h 127.0.0.2 -p 10000 -z : udp -h 127.0.0.2 -p 10000 -z")

  ok, outParams = proxy.ice_invoke("reverseString", Ice.OperationMode.Normal, b"\x12\x00\x00\x00\x01\x01\x0b\x61\x6c\x61\x20\x6d\x61\x20\x6b\x6f\x74\x61")

  print(ok)
  print(outParams)
  


#if __name__ == "__main__":
#  main()


