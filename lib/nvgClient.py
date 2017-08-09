import socket
import logging


class NvgClient:
    _instance = None
    address = ''
    port = 0

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.s = socket.socket()
        self.s.settimeout(3)
        self.connect()
        return

    def __del__(self):
        try:
            self.s.close()
        finally:
            return

    @staticmethod
    def getInstance(address, port):
        if(NvgClient._instance == None):
            NvgClient._instance = NvgClient(address, port)
        return NvgClient._instance

    def connect(self):
        try:
            self.s.connect((self.address, self.port))
            print("PORTS in NVG CLIENT: {0}".format(self.port))
        except socket.error:
            self.s.close()
            self.s = socket.socket()
            self.s.settimeout(3)
            self.connect()
            logging.error("Socket can`t connect! Reconnected.")
        return

    def send(self, data: bytearray):
        try:
            self.s.send(data)
            logging.info(str(data))
            rdata = self.s.recv(1024)
            if(rdata[0] == 0x55 and rdata[1:5] == data[0:4]):
                logging.info('NVG OK')
                return True
            else:
                logging.info('NVG BAD')
                return False
        except socket.timeout:
            self.s.close()
            self.connect()
        except IndexError:
            logging.info('Server returns nothing. Reconnecting.')
            self.s.close()
            self.s = socket.socket()
            self.s.settimeout(3)
            self.connect()
            return False
