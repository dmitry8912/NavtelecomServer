from lib import navtelecom
import logging
import socket

ntc = navtelecom.Navtelecom()
s = socket.socket();
s.connect(('91.202.252.202', 2999))
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NVGC_client.log')
while(True):
    ntc.decodeFlexFromDB(s)