#!/usr/bin/env python3

import os
import sys
import socket
import struct
from threading import Thread
import sys, termios

MULTI_HOST = "224.1.2.3"
MULTI_PORT = 4445
HOST = "localhost"
PORT = 4444

# Globals.
TCP_SOCK = None
NICK = None

ASCII_ART = """
 ____   __    ___  __ _  ____  ____
/ ___) /  \  / __)(  / )(  __)(_  _)
\___ \(  O )( (__  )  (  ) _)   )(
(____/ \__/  \___)(__\_)(____) (__)
"""

def print_message(data: str) -> None:
  nick, message = data.split("\0")
  if nick == NICK:
    return
  termios.tcflush(sys.stdin, termios.TCIOFLUSH)
  print(f"\r[{nick}] {message}\n# ", end="")

def recv_tcp() -> None:
  global TCP_SOCK
  assert TCP_SOCK is not None

  while True:
    data = TCP_SOCK.recv(1024).decode()
    if len(data) > 0:
      print_message(data)

def send_udp(message: str) -> None:
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(f"{NICK}\0{message}".encode(), (HOST, PORT))

def send_multicast(message: str) -> None:
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.sendto(f"{NICK}\0{message}".encode(), (MULTI_HOST, MULTI_PORT))

def send_tcp(message: str) -> None:
  TCP_SOCK.send(f"{NICK}\0{message}".encode())

def start_tcp_connection():
  global TCP_SOCK

  TCP_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  TCP_SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  TCP_SOCK.connect((HOST, PORT))
  # Send nick.
  TCP_SOCK.send(NICK.encode())
  Thread(target=recv_tcp).start()

def recv_multi():
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((MULTI_HOST, MULTI_PORT))
  mreq = struct.pack("4sl", socket.inet_aton(MULTI_HOST), socket.INADDR_ANY)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

  while True:
    data = sock.recvfrom(1024)[0].decode()
    if len(data) > 0:
      print_message(data)

def main() -> None:
  global NICK
  if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <nick>")
    os._exit(0)
  NICK = sys.argv[1]

  start_tcp_connection()
  Thread(target=recv_multi).start()

  while True:
    try:
      message = input(f"# ")
      if len(message) == 0:
        continue

      if message.startswith("!A"):
        message = ASCII_ART

      if message.startswith("!U"):
        message = message[2:].strip()
        send_udp(message)
      elif message.startswith("!M"):
        message = message[2:].strip()
        send_multicast(message)
      else:
        send_tcp(message)

      print(f"\033[1A[{NICK}] {message}\033[K")

    except KeyboardInterrupt:
      TCP_SOCK.shutdown(socket.SHUT_RDWR)
      TCP_SOCK.close()
      os._exit(0)

if __name__ == "__main__":
  main()

