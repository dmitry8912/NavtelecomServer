from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from lib import navtelecom

class NavtelecomProtocol(LineReceiver):

    name = ""

    def getName(self):
        if self.name!="":
            return self.name
        return self.transport.getPeer().host

    def connectionMade(self):
        print("New connection from "+self.getName())

    def connectionLost(self, reason):
        print("Lost connection from "+self.getName())
        self.factory.clientProtocols.remove(self)
        self.factory.ntc.disconnect(self)

    def dataReceived(self, line):
        #self.factory.clientProtocols.append(self)
        data = self.factory.ntc.read(line,self)
        if(self in self.factory.clientProtocols):
            if(b'*>FLEX' in line):
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
                #error
                print("Error!")


class NavtelecomProtocolFactory(ServerFactory):

    protocol = NavtelecomProtocol

    def __init__(self):
        self.clientProtocols = []
        self.ntc = navtelecom.Navtelecom()

