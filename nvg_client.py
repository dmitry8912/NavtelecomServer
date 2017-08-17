from lib import navtelecom
from lib import postgres
from tendo import singleton
import multiprocessing
import logging
import os

def dec(packet):
    ntc = navtelecom.Navtelecom()
    ntc.decPacket(packet)

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NVGC_clien'+str(os.getpid())+u'.log')
if __name__ == '__main__':
    pool = multiprocessing.Pool(3)
    while(True):
        ntc = navtelecom.Navtelecom()
        packets = ntc.decodeFlexFromDB()
        pool.map(dec,packets)
else:
    print(os.getpid())