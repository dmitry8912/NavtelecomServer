import serial
from lib import navtelecom

# smart = serial.Serial('COM3', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
# smart.timeout = 10
#
# dev = navtelecom.Navtelecom(smart)
# data = dev.send('@NTC', '*?A', 1, 0)
#
# response = dev.read()
# if(response):
#     print(response)
#
# smart.close()
