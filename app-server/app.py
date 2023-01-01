#!/usr/bin/env python
import socket, threading, time, logging, sys
from ingress import IngressServer

logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s [%(levelname)s] %(message)s",
  handlers = [
    logging.StreamHandler(sys.stdout)
  ]
)

user = ('host.docker.internal', 8080)

class Forward:
  def __init__(self):
    self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def start(self, host, port):
    try:
      self.forward.connect((host, port))
      return self.forward
    except Exception as e:
      logging.info(e)
      return False

class ProxyServer(threading.Thread):
  threads = []
  channel = {}

  def __init__(self, host, port):
    threading.Thread.__init__(self)

    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server.bind((host, port))
    self.server.listen(200)
    self.active = True

  def run(self):
    logging.info("Proxy server started.")

    while self.active:
      time.sleep(0.0001)
      clientSocket, clientAddress = self.server.accept()

      newthread = self.ClientThread(clientAddress, clientSocket)
      newthread.start()
      self.threads.append(newthread)
    
  class ClientThread(threading.Thread):
    HTTP_HEADER_DELIMITER = b'\r\n\r\n'
    CONTENT_LENGTH_FIELD  = b'Content-Length:'
    ONE_BYTE_LENGTH       = 1

    def __init__(self,clientAddress, clientsocket):
      threading.Thread.__init__(self)
      self.csocket = clientsocket
      self.client  = clientAddress

    def run(self):
      logging.info("New proxy request connection from: " + str(self.client))

      self.request = self.getContent(self.csocket)
      if self.request:
        forward = Forward().start(user[0], user[1])
        forward.send(self.request)

        self.response = self.getContent(forward)
        if self.response:
          self.csocket.send(self.response)

      self.disconnect()

    def getContent(self, sock):
      header = self.getHeader(sock)
      length = self.getContentLength(header)
      body   = self.getBody(sock, length)
      data   = b''.join([header, body])

      return data

    def getContentLength(self, header):
      for line in header.split(b'\r\n'):
        if self.CONTENT_LENGTH_FIELD in line:
          return int(line[len(self.CONTENT_LENGTH_FIELD):])
      return 0

    def getHeader(self, sock):
      header = bytes() 
      chunk  = bytes()

      while self.HTTP_HEADER_DELIMITER not in header:
        chunk = sock.recv(self.ONE_BYTE_LENGTH)
        if not chunk:
          break
        else:
          header += chunk

      return header  
        
    def getBody(self, sock, content_length):
      body = bytes()
      data = bytes()

      while True:
        data = sock.recv(content_length)
        if len(data)<=0:
          break
        else:
          body += data

      return body 

    def disconnect(self):
      logging.info("Proxt request at " + str(self.client) + " disconnected...")
      self.csocket.close()
      ProxyServer.threads.remove(self)

if __name__ == '__main__':
  host = socket.gethostbyname(socket.gethostname())
  port = 5000
  proxyServer   = ProxyServer(host, port)
  ingressServer = IngressServer(host, 5001)

  try:
    proxyServer.start()
    ingressServer.start()
  except KeyboardInterrupt:
    print("Keyboard interrupt")

    proxyServer.active = False
    for ins in ingressServer.threads:
      ins.active = False

    sys.exit(1)
