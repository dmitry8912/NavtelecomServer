from lib import navtelecom
from lib import postgres
from tendo import singleton
import logging
import time

me = singleton.SingleInstance()
ntc = navtelecom.Navtelecom()
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'/var/sr-nav/navtelecom/NVGC_client.log')
while(True):
    t = (postgres.NavtelecomDB.getInstance()).getUnhandledPacketsCount()
    logging.info('located '+str(t[0][0])+' enties')
    if(t[0][0] > 0):
        logging.info('decoding')
        ntc.decodeFlexFromDB()
    else:
        time.sleep(5)
        t = (postgres.NavtelecomDB.getInstance()).getUnhandledPacketsCount()
        if(t[0][0] < 0):
            logging.info('SCRIPT END')
            break
