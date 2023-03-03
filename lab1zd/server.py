#!/usr/bin/env python3

import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 4444

# Globals.
CLIENTS = {}

def send_message(sender_nick: str, message: str) -> None:
  for nick, socket in CLIENTS.items():
    if nick != sender_nick:
      socket.send(f"{sender_nick}\0{message}".encode())

def handle_tcp_client(conn, addr):
  global CLIENTS

  nick = conn.recv(1024).decode()
  if nick in CLIENTS:
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    return
  CLIENTS[nick] = conn

  print(f"Client connected: ({nick})")

  while True:
    try:
      message = conn.recv(1024).decode()
      if len(message) > 0:
        send_message(nick, message.split("\0")[1])
    except socket.error:
      del CLIENTS[nick]
      conn.shutdown(socket.SHUT_RDWR)
      conn.close()

def start_tcp_server(): 
  print("Starting TCP server ...")
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((HOST, PORT))
  sock.listen(10)

  while True:
    conn, addr = sock.accept()
    Thread(target=handle_tcp_client, args=(conn, addr)).start()

def start_udp_server():
  print("Starting UDP server ...")
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((HOST, PORT))

  while True:
    data = sock.recvfrom(1024)[0].decode()
    send_message(*data.split("\0"))

def main() -> None:
  thread_tcp = Thread(target=start_tcp_server)
  thread_tcp.start()
  thread_udp = Thread(target=start_udp_server)
  thread_udp.start()

  thread_tcp.join()
  thread_udp.join()

if __name__ == "__main__":
  main()

