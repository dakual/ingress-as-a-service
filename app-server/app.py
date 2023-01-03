#!/usr/bin/env python
import socket, logging, sys
from ingress import IngressServer
from proxy import ProxyServer

logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s [%(levelname)s] %(message)s",
  handlers = [
    logging.StreamHandler(sys.stdout)
  ]
)

host          = socket.gethostbyname(socket.gethostname())
ingressServer = IngressServer(host, 6000)
proxyServer   = ProxyServer(host, 5000, IngressServer)


if __name__ == '__main__':
  try:
    proxyServer.start()
    ingressServer.start()
  except KeyboardInterrupt:
    print("Keyboard interrupt")

    proxyServer.active = False
    for ins in ingressServer.clients:
      ins.active = False

    sys.exit(1)
