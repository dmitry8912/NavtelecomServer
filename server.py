from twisted.internet import reactor
from lib.serverProtocol import NavtelecomProtocolFactory
from twisted.web import server, resource
from lib import webserver
import logging

print("Starting Server")
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NTCC_server.log')
factory = NavtelecomProtocolFactory()
reactor.listenTCP(9000, factory)
site = server.Site(webserver.Simple(factory))
reactor.listenTCP(9090, site)
reactor.run()
