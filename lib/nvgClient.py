import socket
import logging

class NvgClient:
    _instance = None
    def __init__(self):
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
    def getInstance():
        if(NvgClient._instance == None):
            NvgClient._instance = NvgClient()
        return NvgClient._instance

    def connect(self):
        try:
            self.s.connect(('91.202.252.202',2999))
        except socket.error:
            self.s.close()
            self.s = socket.socket()
            self.s.settimeout(3)
            self.connect()
            logging.error("Socket can`t connect!")
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
