import socket
import threading
import logging
import time
import select
import sys

logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s [%(levelname)s] %(message)s",
  handlers = [
    logging.StreamHandler(sys.stdout)
  ]
)

def main():  
  localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  localSocket.connect(("localhost", 8080))
  localSocket.setblocking(0)

  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  serverSocket.connect(("localhost", 6000))
  serverSocket.setblocking(0)
  
  serverData = bytes()
  localData  = bytes()
  terminate  = False
  
  while not terminate:
    inputs  = [serverSocket, localSocket]
    outputs = []
    
    if len(serverData) > 0:
      outputs.append(serverSocket)
      
    if len(localData) > 0:
      outputs.append(localSocket)
    
    inputsReady, outputsReady, errorsReady = select.select(inputs, outputs, [], 1.0)
    for inp in inputsReady:
      if inp == serverSocket:
        try:
          data = serverSocket.recv(4096)
        except Exception as e:
          logging.info("Exception:", e)
        
        if data != None:
          if len(data) > 0:
            localData += data
            logging.info("request:"  + localData.decode('latin1'))
            
      elif inp == localSocket:
        try:
          data = localSocket.recv(4096)
        except Exception as e:
          logging.info("Exception:", e)
          
        if data != None:
          if len(data) > 0:
            serverData += data
            logging.info("response:"  + serverData.decode('latin1'))

    for out in outputsReady:
      if out == serverSocket and len(serverData) > 0:
        bytesWritten = serverSocket.send(serverData)
        if bytesWritten > 0:
          serverData = serverData[bytesWritten:]
      elif out == localSocket and len(localData) > 0:
        bytesWritten = localSocket.send(localData)
        if bytesWritten > 0:
          localData = localData[bytesWritten:]
  
  serverSocket.close()
  localSocket.close()

  logging.info("Proxy client terminated")

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print("Keyboard interrupt")

# import socket, threading, time, logging, sys

# logging.basicConfig(
#   level    = logging.INFO,
#   format   = "%(asctime)s [%(levelname)s] %(message)s",
#   handlers = [
#     logging.StreamHandler(sys.stdout)
#   ]
# )

# nextPingTime = time.time()

# host = "127.0.0.1"
# port = 6000

# serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# serverSocket.connect((host,port))
# #server.setblocking(0)



# class Forward:
#   def __init__(self):
#     self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#   def start(self, host="localhost", port=8080):
#     try:
#       self.forward.connect((host, port))
#       return self.forward
#     except Exception as e:
#       logging.error(e)
#       return False
  
#   def disconnect(self):
#     self.forward.close()

# # forward = Forward().start()

# def ping():
#   pinging  = b'GET / HTTP/1.1\r\n'
#   pinging += b'Host: localhost\r\n'
#   pinging += b'X-Action: ping\r\n'
#   pinging += b'Connection: close\r\n'
#   pinging += b'Content-Length: 0\r\n'
#   pinging += b'\r\n'

#   serverSocket.send(pinging)

# def main():   
#   nextPingTime = time.time()
#   while True:
#     time.sleep(0.001)

#     now = time.time()
#     if (now >= nextPingTime):
#       nextPingTime = now + 3.0
#       ping()

#     # data = server.recv(1024)
#     # if data:
#     #   print('Received message from the server :', str(data.decode('UTF-8')))


# if __name__ == '__main__':
#   try:
#     main()
#   except KeyboardInterrupt:
#     serverSocket.close()
#     print("Keyboard interrupt")