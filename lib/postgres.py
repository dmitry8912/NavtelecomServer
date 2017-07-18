import postgresql
import logging
import json
class NavtelecomDB:
    _instance = None
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

    @staticmethod
    def getInstance():
        if(NavtelecomDB._instance == None):
            NavtelecomDB._instance = NavtelecomDB()
        return NavtelecomDB._instance

    def connectDevice(self,imei: bytearray, id:bytearray):
        updateDevice = self.db.prepare("INSERT INTO devices(imei,ntcb_id,lastSeen) VALUES ($1,$2,DEFAULT) ON CONFLICT(imei) DO UPDATE SET lastSeen=now_ast()")
        devId = int.from_bytes(id, byteorder='little', signed= False)
        devImei = ''
        for b in imei:
            devImei += chr(b)
        updateDevice(int(devImei),int(devId))
        logging.info('Device connected: IMEI='+str(imei)+'; ID='+str(id))
        return

    def addRawPacket(self, imei: bytearray, data: bytearray):
        addRaw = self.db.prepare(
            "INSERT INTO raw_packets(id,device_id,data,timestamp,processed) values(DEFAULT,$1,$2,DEFAULT,DEFAULT)")
        devImei = ''
        for b in imei:
            devImei += chr(b)
        addRaw(int(devImei), data)
        logging.info('Device send packet: IMEI=' + str(imei) + ';')
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

    def getField(self,imei:bytearray):
        getFields = self.db.prepare(
            "select fieldset from device_fieldset where device_id = $1")
        return getFields(imei)

    def getNotDecodedPackets(self,limit = 0):
        query = "select * from raw_packets where processed = False order by timestamp ASC limit 10"
        if(limit != 0):
            query += " limit "+str(limit)
        packets = self.db.prepare(query)
        return packets()

    def getUnhandledPacketsCount(self):
        query = "select count(*) from raw_packets where processed = False"
        packets = self.db.prepare(query)
        return packets()

    def markPacket(self,packet_id):
        markPacket = self.db.prepare(
            "UPDATE raw_packets SET processed = True where id=$1")
        markPacket(packet_id)
        return

    def getPackets(self):
        query = self.db.prepare("select count(*) from raw_packets where processed = False");
        return query()

    def getLastPacket(self):
        query = self.db.prepare("select TO_CHAR(timestamp, 'DD.MM.YYYY HH24:MI:SS') as lasttime from raw_packets order by timestamp DESC limit 1");
        return query()

    def getVendorsList(self):
        vendorList = self.db.prepare('SELECT array_to_json(array_agg("Vendors")) FROM "Vendors"')
        return json.loads(vendorList()[0][0])

    def addVendor(self,name:str):
        vendorAdd = self.db.prepare("SELECT vendor_add_ret_id($1)")
        return vendorAdd(name)[0][0]

    def updateVendor(self,id:int,name:str):
        vendor = self.db.prepare("SELECT vendor_update($1,$2)")
        return vendor(id,name)[0][0]

    def deleteVendor(self,id:int):
        vendor = self.db.prepare("SELECT vendor_delete($1)")
        return vendor(id)[0][0]