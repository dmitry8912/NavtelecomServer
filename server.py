from twisted.internet import reactor
from lib.serverProtocol import NavtelecomProtocolFactory
import logging

print("Starting Server")
factory = NavtelecomProtocolFactory()
reactor.listenTCP(9000, factory)
reactor.run()
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NTCC_server.log')