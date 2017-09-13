import struct
import logging

class NVG:
    def __init__(self):
        self.data = {}
        return

    def __del__(self):
        del self.data
        return

    def addData(self,type:int,data:bytearray):
        self.data[type] = bytearray()
        length = len(data)
        length = length.to_bytes(2, byteorder='little',signed=False)
        dtype = type.to_bytes(1, byteorder='little',signed=False)

        for b in dtype:
            self.data[type].append(b)

        for b in length:
            self.data[type].append(b)

        for b in data:
            self.data[type].append(b)
        return

    def getPacket(self):
        length = 6
        for d in self.data.items():
            length+=len(d[1])

        length = length.to_bytes(4,'little')

        protocol_ver = [b'\x00',b'\x01']

        data = bytearray()

        data += length

        for p in protocol_ver:
            data += p

        for d in self.data.items():
            data += d[1]

        return data

    def addIdentifier(self,imei: bytearray):
        self.addData(0, imei)
        return

    def addTime(self,time: int):
        time = time.to_bytes(4,byteorder='little',signed=False)
        self.addData(0x01,time)
        return

    def addState(self,sosState: bool, engineState: bool, standState: bool):
        state = 0b00000000
        if(sosState):
            state += 0b10000000

        if(engineState):
            state += 0b01000000

        if(standState):
            state += 0b00100000

        self.addData(2,state.to_bytes(2,byteorder='little'))
        return

    def addCoordinates(self,lat:int,lon:int,alt:int,speed:int,course:int,satCount:int):
        data = bytearray()
        data += struct.pack('<d',(lon/600000))
        data += struct.pack('<d',(lat/600000))
        data += struct.pack('<d',(alt))
        data += int(round(speed[0])).to_bytes(2, byteorder='little')
        data += int(course).to_bytes(2, byteorder='little')
        data += int(satCount).to_bytes(1, byteorder='little')
        self.addData(3,data)
        return

    def addGSM(self,signalLevel: int):
        gsm = signalLevel.to_bytes(2,byteorder='little',signed=True)
        self.addData(4,gsm)
        return

    def addOutsideVoltage(self, level: int):
        #logging.debug('Outside Voltage Raw = '+str(level))
        level = int(round(level / 100))
        #logging.debug('Outside Voltage Comp = ' + str(level))
        gsm = level.to_bytes(2, 'little')
        #logging.debug('Outside Voltage Bytes = ' + str(gsm))
        self.addData(5, gsm)
        return

    def addBatteryVoltage(self, level: int):
        #logging.debug('Battery Voltage Raw = ' + str(level))
        # if(level > 4200):
        #     level = 100
        # else:
        #     level = round(((level/4200)*100)%100)
        #logging.debug('Battery Voltage Comp = ' + str(level))
        gsm = level.to_bytes(2, byteorder='little',signed = False)
        #logging.debug('Battery Voltage Bytes = ' + str(level))
        self.addData(6, gsm)
        return

    def addDigitalInputsState(self, inputs:list):
        i = 1
        data = 0b0
        for i in inputs:
            if(i):
                data+= 0x01 << i
        self.addData(7,data)
        return

    def addDigitalOutputsState(self, outputs:list):
        i = 1
        data = 0b0
        for i in outputs:
            if(i):
                data+= 0x01 << i
        self.addData(8,data)
        return

    def addDigitalInputsStateFromFlex(self, states:bytearray):
        #logging.debug('DI states = ' + str(states))
        if(len(states) != 2):
            states = int.from_bytes(states,byteorder='little')
            states = states.to_bytes(2,byteorder='little',signed=False)
        #logging.debug('DI states as bytes = ' + str(states))
        self.addData(7, states)
        return

    def addDigitalOutputsStateFromFlex(self, states:bytearray):
        #logging.debug('DO states = ' + str(states))
        if(len(states) != 2):
            states = int.from_bytes(states,byteorder='little')
            states = states.to_bytes(2,byteorder='little',signed=False)
        #logging.debug('DO states as bytes = ' + str(states))
        self.addData(8,states)
        return

    def addADCState(self,states: list):
        #logging.debug('ADC states = ' + str(states))
        data = bytearray()
        num = 1
        for b in states:
            data += int(num).to_bytes(1, byteorder='little', signed=False)
            data += struct.pack('<d', float(b/100))
            #logging.debug('ADC state #'+str(num)+' = ' + str(float(b/100)))
            num += 1
        #logging.debug('ADC states as bytes = ' + str(data))
        self.addData(9,data)
        return

    def addDriverCode(self, code:str):
        self.addData(10,code)
        return

    def addFuelLevel(self, level: list):
        logging.debug('Fuel Levels = ' + str(level))
        data = bytearray()
        num = 1
        for el in level:
            data += int(num).to_bytes(1,byteorder='little',signed=False)
            data += struct.pack('<d',float(el))
            logging.debug('Fuel state #' + str(num) + ' = ' + str(float(el)))
            num += 1
        logging.debug('Fuel states as bytes = ' + str(data))
        self.addData(11,data)
        return
