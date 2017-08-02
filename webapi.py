from twisted.internet import reactor
from lib.serverProtocol import NavtelecomProtocolFactory
from twisted.web import server, resource
from lib import webserver
from lib.registry import Registry

print("Starting Web Server")
factory = NavtelecomProtocolFactory()
site = server.Site(webserver.Simple(factory))
reactor.listenTCP(int(Registry.getInstance().getConfig()['default']['default_server_api_port']), site)
reactor.run()