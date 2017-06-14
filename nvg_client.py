from lib import navtelecom
import logging

ntc = navtelecom.Navtelecom()
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'NVGC_client.log')
while(True):
    ntc.decodeFlexFromDB()