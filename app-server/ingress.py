import socket, threading, time, logging, sys, select
from utils import Request


class IngressServer:
  clients = []
  active  = True

  def __init__(self, host, port):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # self.server.setblocking(0)
    self.server.bind((host, port))
    self.server.listen(5) 

  def start(self):
    logging.info("Ingress server started.")
    self.clients.append(self.server)
    
    while self.active:
      time.sleep(0.001)
      readable, writable, exceptional = select.select(self.clients, [], [])
      for s in readable:
        if s == self.server:
          connection, client_address = s.accept()
          # connection.setblocking(0)
          logging.info("Client connected: %s:%s" % (connection.getpeername()))
          # self.clients.append(connection)
          self.clients.insert(1, connection)
        else:
          try:
            data = Request(s).getContent() # s.recv(1024)
            if len(data) > 0:
              logging.info("Data received: %s:%s" % (s.getpeername()))
              # logging.info(data.decode('ascii').rstrip())
            else:
              raise Exception("Client connection null")
          except Exception as e:
            self.disconnect(s)

  def disconnect(self, s):
    logging.info("Client disconnected: %s:%s" % (s.getpeername()))
    
    if s in self.clients:
      self.clients.remove(s)
      s.close()

  @classmethod
  def getClients(cls):
    return cls.clients[1]


