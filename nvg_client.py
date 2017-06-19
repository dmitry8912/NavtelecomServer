from lib import navtelecom
from lib import nvgProtocol
from twisted.internet import reactor, protocol
import logging
import socket

ntc = navtelecom.Navtelecom()
f = nvgProtocol.NvgProtocolFactory()
reactor.connectTCP("91.202.252.202", 2999, f)
reactor.run()
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NVGC_client.log')
while(True):
    ntc.decodeFlexFromDB(f)