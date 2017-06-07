from twisted.internet import reactor
from lib.serverProtocol import NavtelecomProtocolFactory

print("Starting Server")
factory = NavtelecomProtocolFactory()
reactor.listenTCP(9000, factory)
reactor.run()