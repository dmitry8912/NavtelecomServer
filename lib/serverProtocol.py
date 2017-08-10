from twisted.internet.protocol import ServerFactory
import json

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.protocols.policies import TimeoutMixin

from lib import navtelecom
from lib.database import postgres


class NavtelecomProtocol(LineReceiver, TimeoutMixin):

    name = ""

    def getName(self):
        if self.name!="":
            return self.name
        return self.transport.getPeer().host

    def connectionMade(self):
        self.setTimeout(30)

    def connectionLost(self, reason):
        if(self in self.factory.clientProtocols):
            self.factory.clientProtocols.remove(self)
        self.factory.ntc.disconnect(self)

    # Получает данные (line) Если прочитывает - разбирает пакет
    def dataReceived(self, line):
        self.resetTimeout()
        #self.factory.clientProtocols.append(self)
        data = self.factory.ntc.read(line,self)
        if(self in self.factory.clientProtocols):
            if (int.from_bytes(line, byteorder='little') == 0x7f): # Поддержание связи
                #just ping message
                return
            if(b'*>FLEX' in line): # Запрос на установление соединения в формате Flex
                self.factory.ntc.coordinateFlexVersion(data,self)
            else:
                if(b'~' in line[0:1]):
                    self.factory.ntc.flexExec(line,self)
                else:
                    #command answer
                    return
        else:
            if(data):
                self.factory.clientProtocols.append(self)
                self.factory.ntc.makeHandshake(self)
            else:
                return

    def timeoutConnection(self):
        self.transport.abortConnection()


class NavtelecomProtocolFactory(ServerFactory):

    protocol = NavtelecomProtocol

    def __init__(self):
        self.clientProtocols = []
        self.ntc = navtelecom.Navtelecom()

    def getCurrentStateInfo(self):
        import os
        import psutil
        db = postgres.NavtelecomDB.getInstance()
        state = {
            'clients': len(self.ntc.clients),
            'pid': os.getpid(),
            'mem': psutil.Process(os.getpid()).memory_info()[0] / float(2 ** 20),
            'packets': db.getPackets()[0][0],
            'last': db.getLastPacket()[0][0]
        }
        return (json.dumps(state)).encode()

