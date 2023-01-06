import socket
import threading
import logging
import time
import select

class Server(threading.Thread):
  threads = []
  active  = True

  def __init__(self, host, port):
    threading.Thread.__init__(self)

    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server.bind((host, port))
    self.server.listen(5)

  def run(self):
    logging.info("Client server started.")

    while self.active:
      time.sleep(0.001)

      clientSocket, clientAddress = self.server.accept()
      clientSocket.setblocking(0)
      # clientThread = Client(clientSocket)
      # clientThread.start()
      self.threads.append(clientSocket)
      logging.info("Client connected: %s:%s" % (clientSocket.getpeername()))
    
    logging.info("Client server stoped. Threads[%s] are terminating..." % (len(self.threads)))
    for t in self.threads:
      t.terminateAll = True
    
    self.server.close()
	
  @classmethod
  def getClient(cls):
    return cls.threads[0]

# class Client(threading.Thread):
# 	terminateAll = False

# 	def __init__(self, clientSocket):
# 		threading.Thread.__init__(self)
# 		self.clientSocket = clientSocket
# 		# self.clientSocket.setblocking(0)

# 	def run(self):
# 		logging.info("Client connected: %s:%s" % (self.clientSocket.getpeername()))

		# while not self.terminateAll:
		# 	time.sleep(0.001)

		# 	data = self.clientSocket.recv(4096)
		# 	if data != None:
		# 		if len(data) > 0:
		# 			print(data.decode())
		# 		# else:
		# 		# 	self.terminateAll = True
				

		# self.clientSocket.close()
		# logging.info("Client terminated")



# class Client(threading.Thread):
# 	terminateAll = False

# 	def __init__(self, clientSocket):
# 		threading.Thread.__init__(self)
# 		self.clientSocket = clientSocket
# 		self.clientSocket.setblocking(0)

# 	def run(self):
# 		logging.info("Proxy client connected: %s:%s" % (self.clientSocket.getpeername()))
		
# 		targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		targetSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 		targetSocket.connect(("localhost", 8080))
# 		targetSocket.setblocking(0)
		
# 		clientData = bytes()
# 		targetData = bytes()
# 		terminate  = False
		
# 		while not terminate and not self.terminateAll:
# 			inputs  = [self.clientSocket, targetSocket]
# 			outputs = []
			
# 			if len(clientData) > 0:
# 				outputs.append(self.clientSocket)
				
# 			if len(targetData) > 0:
# 				outputs.append(targetSocket)
			
# 			inputsReady, outputsReady, errorsReady = select.select(inputs, outputs, [], 1.0)
# 			for inp in inputsReady:
# 				if inp == self.clientSocket:
# 					try:
# 						data = self.clientSocket.recv(4096)
# 					except Exception as e:
# 						pass
					
# 					if data != None:
# 						if len(data) > 0:
# 							targetData += data
# 						else:
# 							terminate = True
# 				elif inp == targetSocket:
# 					try:
# 						data = targetSocket.recv(4096)
# 					except Exception as e:
# 						pass
						
# 					if data != None:
# 						if len(data) > 0:
# 							clientData += data
# 						else:
# 							terminate = True
						
# 			for out in outputsReady:
# 				if out == self.clientSocket and len(clientData) > 0:
# 					bytesWritten = self.clientSocket.send(clientData)
# 					if bytesWritten > 0:
# 						clientData = clientData[bytesWritten:]
# 				elif out == targetSocket and len(targetData) > 0:
# 					bytesWritten = targetSocket.send(targetData)
# 					if bytesWritten > 0:
# 						targetData = targetData[bytesWritten:]
		
# 		self.clientSocket.close()
# 		targetSocket.close()

# 		logging.info("Proxy client terminated")