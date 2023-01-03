import socket, threading, time, logging, sys

logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s [%(levelname)s] %(message)s",
  handlers = [
    logging.StreamHandler(sys.stdout)
  ]
)

nextPingTime = time.time()

host = "127.0.0.1"
port = 6000

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.connect((host,port))
#server.setblocking(0)


class Request:
  HTTP_HEADER_DELIMITER = b'\r\n\r\n'
  CONTENT_LENGTH_FIELD  = b'Content-Length:'
  ACTION_FIELD          = b'X-Action:'
  ONE_BYTE_LENGTH       = 1

  def __init__(self, socket):
    self.socket = socket
    
  def getContent(self):
    header = self.getHeader()
    if not header:
      return

    header = header.replace(b'localhost:5000', b'localhost:8080')
    length = self.getLength(header)
    body   = self.getBody(length)

    return b''.join([header, body])

  def getAction(self, header):
    for line in header.split(b'\r\n'):
      if self.ACTION_FIELD in line:
        return line[len(self.ACTION_FIELD):]
    return b''

  def getLength(self, header):
    for line in header.split(b'\r\n'):
      if self.CONTENT_LENGTH_FIELD in line:
        return int(line[len(self.CONTENT_LENGTH_FIELD):])
    return 0

  def getHeader(self):
    header = bytes() 
    chunk  = bytes()

    while self.HTTP_HEADER_DELIMITER not in header:
      chunk = self.socket.recv(self.ONE_BYTE_LENGTH)
      if not chunk:
        break
      else:
        header += chunk

    return header  
      
  def getBody(self, content_length):
    body = bytes()
    data = bytes()

    while True:
      data = self.socket.recv(content_length)
      if len(data)<=0:
        break
      else:
        body += data

    return body 



class Forward:
  def __init__(self):
    self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def start(self, host="localhost", port=8080):
    try:
      self.forward.connect((host, port))
      return self.forward
    except Exception as e:
      logging.error(e)
      return False

forward = Forward().start()

def ping():
  pinging  = b'GET / HTTP/1.1\r\n'
  pinging += b'Host: localhost\r\n'
  pinging += b'X-Action: ping\r\n'
  pinging += b'Connection: close\r\n'
  pinging += b'Content-Length: 0\r\n'
  pinging += b'\r\n'

  serverSocket.send(pinging)

def main():   
  nextPingTime = time.time()
  while True:
    time.sleep(0.001)

    request = Request(serverSocket).getContent()
    if request:
      forward.send(request)
      logging.info("request received")
      logging.info(request.decode())
      
      response = Request(forward).getContent()
      if response:
        serverSocket.send(response)
        logging.info("response sended")
        logging.info(response.decode())


    # now = time.time()
    # if (now >= nextPingTime):
    #   nextPingTime = now + 3.0
    #   ping()

      

    # data = server.recv(1024)
    # if data:
    #   print('Received message from the server :', str(data.decode('UTF-8')))

    


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    serverSocket.close()
    print("Keyboard interrupt")