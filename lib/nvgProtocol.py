from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from lib import navtelecom
from lib import postgres
import json
import logging

class NvgProtocol(Protocol):

    packet_id = None
    packetData = None
    def connectionMade(self):
        logging.info("Connected to server")

    def connectionLost(self, reason):
        logging.info("Lost connection")

    def dataReceived(self, line):
        if (line[0] == 0x55 and line[1:5] == self.data[0:4]):
            logging.info("NVG SEND OK")
            db = postgres.NavtelecomDB.getInstance()
            db.markPacket(self.packet_id)
        else:
            logging.info('NVG ERROR')
            logging.debug(line[0])
            logging.debug(line[1:5])
            logging.debug(line[0:4])
        return

class NvgProtocolFactory(ReconnectingClientFactory):

    protocol = NvgProtocol
    def __init__(self):
        self.ntc = navtelecom.Navtelecom()

    def buildProtocol(self,addr):
        logging.info('Connected.')

    def clientConnectionLost(self, connector, reason):
        logging.info('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.info('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def sendPacket(self,data, id):
        self.protocol.packet_id = id
        self.protocol.packetData = data
        self.protocol.transport.write(data)
        logging.info('data sended')
        return

