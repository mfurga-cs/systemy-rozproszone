import socket
import struct

serverIP = "127.0.0.1"
serverPort = 9009

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg_bytes = (300).to_bytes(4, byteorder='little')

client.sendto(msg_bytes, (serverIP, serverPort))


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort + 1))

buff, address = serverSocket.recvfrom(4)

print(struct.unpack(">L", buff)[0])



