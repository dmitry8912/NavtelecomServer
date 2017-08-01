from twisted.internet import reactor
from lib.serverProtocol import NavtelecomProtocolFactory
from twisted.web import server, resource
from lib import webserver
from lib.registry import Registry
import logging
import os

def processWorker():
    print(os.getpid())

print("Starting Server")
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = int(Registry.getInstance().getConfig()['log']['enable_logging']), filename = Registry.getInstance().getConfig()['log']['server_log'])

if __name__ == '__main__':
    factory = NavtelecomProtocolFactory()
    reactor.listenTCP(int(Registry.getInstance().getConfig()['default']['default_server_port']), factory)
    site = server.Site(webserver.Simple(factory))
    reactor.listenTCP(int(Registry.getInstance().getConfig()['default']['default_server_api_port']), site)
    reactor.run()
else:
    print('IM A THREAD NUMBER: ' + str(os.getpid()))
