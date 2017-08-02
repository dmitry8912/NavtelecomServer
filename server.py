from twisted.internet import reactor
from lib.serverProtocol import NavtelecomProtocolFactory
from lib.registry import Registry
import logging

if __name__ =='__main__':
    print("Starting Server")
    logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = int(Registry.getInstance().getConfig()['log']['enable_logging']), filename = Registry.getInstance().getConfig()['log']['server_log'])
    factory = NavtelecomProtocolFactory()
    reactor.listenTCP(int(Registry.getInstance().getConfig()['default']['default_server_port']), factory)
    reactor.run()