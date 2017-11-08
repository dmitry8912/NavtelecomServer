from lib import navtelecom
from lib import postgres
import multiprocessing
import logging
import os

def dec(packet):
    ntc = navtelecom.Navtelecom()
    ntc.decPacket(packet)

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'nvg_logs/NVGC_client-main.log')
if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    pool = multiprocessing.Pool(100)
    while(True):
        ntc = navtelecom.Navtelecom()
        packets = ntc.decodeFlexFromDB()
        pool.map(dec,packets)
else:
    print(os.getpid())
