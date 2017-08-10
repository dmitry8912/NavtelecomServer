from twisted.internet import reactor
from twisted.web import server

from lib.configuration import webserver
from lib.configuration.registry import Registry
from lib.serverProtocol import NavtelecomProtocolFactory

print("Starting Web Server")
factory = NavtelecomProtocolFactory()
site = server.Site(webserver.Simple(factory))
reactor.listenTCP(int(Registry.getInstance().getConfig()['default']['default_server_api_port']), site)
reactor.run()