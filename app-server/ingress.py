import socket, threading, time, logging, sys

class IngressServer:
  threads = []
  channel = {}

  def __init__(self, host, port):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server.bind((host, port))
    self.server.listen(200) 

  def start(self):
    logging.info("Ingress server started.")

    while True:
      time.sleep(0.0001)
      clientSocket, clientAddress = self.server.accept()

      newthread = self.ClientThread(clientAddress, clientSocket)
      newthread.start()
      self.threads.append(newthread)
    
  class ClientThread(threading.Thread):
    def __init__(self,clientAddress, clientsocket):
      threading.Thread.__init__(self)
      self.csocket = clientsocket
      self.client  = clientAddress
      self.active  = True

    def run(self):
      logging.info("New ingress connection from: " + str(self.client))

      while self.active:
        try:
          data = self.csocket.recv(1024)
          if not data:
            print('No connection, Bye 2')
            break
        except socket.error as e:
          print('No connection, Bye 1')
          break

      self.disconnect()

    def disconnect(self):
      logging.info("Ingress connection at " + str(self.client) + " disconnected...")
      self.csocket.close()
      IngressServer.threads.remove(self)