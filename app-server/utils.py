import logging

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

    action = self.getAction(header)
    if b'ping' in action:
      logging.info("Ping: %s:%s" % (self.socket.getpeername()))

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