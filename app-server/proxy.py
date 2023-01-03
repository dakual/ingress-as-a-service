import socket, threading, time, logging, sys
from ingress import IngressServer
from utils import Request


class ProxyServer(threading.Thread):
  threads = []
  active  = True

  def __init__(self, host, port, ingress):
    threading.Thread.__init__(self)

    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server.bind((host, port))
    self.server.listen(200)
    self.ingress = ingress

  def run(self):
    logging.info("Proxy server started.")

    while self.active:
      time.sleep(0.001)
      clientSocket, clientAddress = self.server.accept()

      newthread = self.ProxyThread(clientAddress, clientSocket)
      newthread.start()
      self.threads.append(newthread)
    
  class ProxyThread(threading.Thread):

    def __init__(self,clientAddress, clientsocket):
      threading.Thread.__init__(self)
      self.csocket = clientsocket
      self.client  = clientAddress

    def run(self):
      logging.info("New proxy request connection from: " + str(self.client))

      self.request = Request(self.csocket).getContent()
      if self.request:
        forward = IngressServer.getClients()
        forward.send(self.request)

        self.response = Request(forward).getContent()
        if self.response:
          self.csocket.send(self.response)

      self.disconnect()

    def disconnect(self):
      logging.info("Proxt request at " + str(self.client) + " disconnected...")
      self.csocket.close()
      ProxyServer.threads.remove(self)