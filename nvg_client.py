from lib import navtelecom
from lib import postgres
from tendo import singleton
import logging

me = singleton.SingleInstance()
ntc = navtelecom.Navtelecom()
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NVGC_client.log')
while(True):
    t = (postgres.NavtelecomDB.getInstance()).getUnhandledPacketsCount()
    if(t[0][0] > 0):
        ntc.decodeFlexFromDB()
    else:
        break