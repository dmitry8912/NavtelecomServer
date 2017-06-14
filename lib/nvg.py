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
        length = length.to_bytes(2, 'little')
        dtype = type.to_bytes(1, 'little')

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

    def addTime(self,time: bytearray):
        time = int(time)
        time = time.to_bytes(4,byteorder='little',signed=False)
        self.addData(0x01,time)
        return

    def addState(self,sosState: bool, engineState: bool, standState: bool):
        state = 0b00000000
        if(sosState):
            state += 0b00000001

        if(engineState):
            state += 0b00000010

        if(standState):
            state += 0b00000100

        self.addData(2,state.to_bytes(2,byteorder='little'))
        return

    def addCoordinates(self,lat:int,lon:int,alt:int,speed:int,course:int,satCount:int):
        data = bytearray()
        data += int(lat).to_bytes(8, byteorder='little')
        data += int(lon).to_bytes(8, byteorder='little')
        data += int(alt).to_bytes(8, byteorder='little')
        data += int(round(speed[0])).to_bytes(8, byteorder='little')
        data += int(course).to_bytes(8, byteorder='little')
        data += int(satCount).to_bytes(8, byteorder='little')
        self.addData(3,data)
        return

    def addGSM(self,signalLevel: int):
        gsm = signalLevel.to_bytes(2,'little',True)
        self.addData(4,gsm)
        return

    def addOutsideVoltage(self, level):
        gsm = level.to_bytes(2, 'little')
        self.addData(5, gsm)
        return

    def addBatteryVoltage(self, level):
        gsm = level.to_bytes(2, 'little')
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

    def addADCState(self,state):
        return

    def addDriverCode(self, code):
        return

    def addFuelLevel(self, level):
        return
