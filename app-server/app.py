#!/usr/bin/env python
import logging
import sys
import proxy
import client

logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s [%(levelname)s] %(message)s",
  handlers = [
    logging.StreamHandler(sys.stdout)
  ]
)


if __name__ == '__main__':
  host         = "127.0.0.1" # socket.gethostbyname(socket.gethostname())
  proxyServer  = proxy.Server(host, 5000)
  clientServer = client.Server(host, 6000)
  
  
  try:
    proxyServer.start()
    clientServer.start()
  except KeyboardInterrupt:
    print("Keyboard interrupt")

    proxyServer.active   = False
    # ingressServer.active = False
    # for ins in ingressServer.clients:
    #   ins.active = False

    sys.exit(1)
