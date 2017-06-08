import postgresql

class NavtelecomDB:
    db_conf = {
        "host": "localhost",
        "port": "5432",
        "user": "navtelecom",
        "password": "navetlecom",
        "db": "navtelecom"
    }
    def __init__(self):
        self.db = postgresql.open('pq://'+self.db_conf['user']+':'+self.db_conf['password']+
                                  '@'+self.db_conf['host']+':'+self.db_conf['port']+'/'+self.db_conf['db'])
        return

    def __del__(self):
        self.db.close()
        return

    def connectDevice(self,imei: bytearray, id:bytearray):
        updateDevice = self.db.prepare("INSERT INTO devices(imei,ntcb_id,lastSeen) VALUES ($1,$2,DEFAULT) ON CONFLICT(imei) DO UPDATE SET lastSeen=now_ast()")
        devId = int.from_bytes(id, byteorder='little', signed= False)
        devImei = ''
        for b in imei:
            devImei += chr(b)
        updateDevice(int(devImei),int(devId))
        return

    def addRawPacket(self, imei: bytearray, data: bytearray):
        addRaw = self.db.prepare(
            "INSERT INTO raw_packets(id,device_id,data,timestamp,processed) values(DEFAULT,$1,$2,DEFAULT,DEFAULT)")
        devImei = ''
        for b in imei:
            devImei += chr(b)
        addRaw(int(devImei), data)
        return

    def addDecodedPacket(self,imei,data):
        return

    def setFields(self,imei:bytearray, fields: list):
        addFields = self.db.prepare(
            "INSERT INTO device_fieldset(device_id,fieldset) values($1,$2) ON CONFLICT(device_id) DO UPDATE SET fieldset=$3")
        devImei = ''
        for b in imei:
            devImei += chr(b)
        addFields(int(devImei), fields, fields)
        return