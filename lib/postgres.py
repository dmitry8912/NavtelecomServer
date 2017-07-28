import postgresql
import logging
import json
from lib.registry import Registry

class NavtelecomDB:
    _instance = None

    def __init__(self):
        self.db = postgresql.open('pq://' + Registry.getInstance().getConfig()['db']['user'] + ':' + Registry.getInstance().getConfig()['db']['password'] +
                                  '@' + Registry.getInstance().getConfig()['db']['host'] + ':' + Registry.getInstance().getConfig()['db']['port'] + '/' + Registry.getInstance().getConfig()['db']['db'])
        return

    def __del__(self):
        self.db.close()
        return

    @staticmethod
    def getInstance():
        if (NavtelecomDB._instance == None):
            NavtelecomDB._instance = NavtelecomDB()
        return NavtelecomDB._instance

    def connectDevice(self, imei: bytearray, id: bytearray):
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

    def addDecodedPacket(self, imei, data):
        return

    def setFields(self, imei: bytearray, fields: list):
        addFields = self.db.prepare(
            "INSERT INTO device_fieldset(device_id,fieldset) values($1,$2) ON CONFLICT(device_id) DO UPDATE SET fieldset=$3")
        devImei = ''
        for b in imei:
            devImei += chr(b)
        addFields(int(devImei), fields, fields)
        return

    def getField(self, imei: bytearray):
        getFields = self.db.prepare(
            "select fieldset from device_fieldset where device_id = $1")
        return getFields(imei)

    def getNotDecodedPackets(self, limit=0):
        query = "select * from raw_packets where processed = False order by timestamp ASC limit 10"
        if (limit != 0):
            query += " limit " + str(limit)
        packets = self.db.prepare(query)
        return packets()

    def getUnhandledPacketsCount(self):
        query = "select count(*) from raw_packets where processed = False"
        packets = self.db.prepare(query)
        return packets()

    def markPacket(self, packet_id):
        markPacket = self.db.prepare(
            "UPDATE raw_packets SET processed = True where id=$1")
        markPacket(packet_id)
        return

    def getPackets(self):
        query = self.db.prepare("select count(*) from raw_packets where processed = False");
        return query()

    def getLastPacket(self):
        query = self.db.prepare(
            "select TO_CHAR(timestamp, 'DD.MM.YYYY HH24:MI:SS') as lasttime from raw_packets order by timestamp DESC limit 1");
        return query()

    def getVendorsList(self):
        vendorList = self.db.prepare('SELECT array_to_json(array_agg("Vendors")) FROM "Vendors"')
        return json.loads(vendorList()[0][0])

    def addVendor(self, name: str):
        vendorAdd = self.db.prepare("SELECT vendor_add_ret_id($1)")
        return vendorAdd(name)[0][0]

    def updateVendor(self, id: int, name: str):
        vendor = self.db.prepare("SELECT vendor_update($1,$2)")
        return vendor(id, name)[0][0]

    def deleteVendor(self, id: int):
        vendor = self.db.prepare("SELECT vendor_delete($1)")
        return vendor(id)[0][0]

    def getModelsList(self):
        modelsList = self.db.prepare(
            'SELECT array_to_json(array_agg(models_list)) FROM (SELECT "Vendor_Models".id AS model_id, "Vendors".id AS vendor_id, "Vendor_Models".name AS model_name, "Vendors".name AS vendor_name FROM "Vendors", "Vendor_Models" WHERE "Vendors".id = "Vendor_Models".vendor_id) models_list;')
        return json.loads(modelsList()[0][0])

    def addModel(self, name: str, vendor_id: int):
        modelAdd = self.db.prepare("SELECT model_add($1,$2)")
        return modelAdd(name, vendor_id)[0][0]

    def updateModel(self, name: str, id: int, vendor_id: int = -1):
        modelUpdate = self.db.prepare("SELECT model_update($1,$2,$3)")
        return modelUpdate(id, name, vendor_id)[0][0]

    def deleteModel(self, id: int):
        model = self.db.prepare("SELECT model_delete($1)")
        return model(id)[0][0]

    # il_kow: Получить список всех устройств
    def getDevicesList(self):
        devicesList = self.db.prepare('SELECT array_to_json(array_agg(devices_list)) '
                                      'FROM (SELECT  "devices".imei as imei, '
                                      '"devices".ntcb_id as ntcb_id, '
                                      '"devices".lastseen as last_seen, '
                                      '"devices".model_id as model_id, '
                                      '"devices".number as num, '
                                      '"Vendor_Models".name as model_name '
                                      'FROM "Vendor_Models", "devices" '
                                      'WHERE "Vendor_Models".id = "devices".model_id)'
                                      ' devices_list;')
        return json.loads(devicesList()[0][0])

    # il_kow: Добавить устройство
    def addDevice(self, imei: int):
        device_add = self.db.prepare("SELECT device_add($1)")
        return device_add(imei)[0][0]

    # il_kow: Обновить устройство
    def updateDevice(self, imei: int, ntcb_id: int, number: str, model_id: int):
        deviceUpdate = self.db.prepare("SELECT device_update($1, $2, $3, $4)")
        return deviceUpdate(imei, ntcb_id, number, model_id)[0][0]

    # il_kow: Добавить устройство (метод new device)
    def newDevice(self, imei: int, model_id: int):
        device_add = self.db.prepare("SELECT device_new($1, $2)")
        return device_add(imei, model_id)[0][0]

    # il_kow: Удалить устройство
    def deleteDevice(self, imei: int):
        device_delete = self.db.prepare("SELECT device_delete($1)")
        return device_delete(imei)[0][0]

    # il_kow: Получить все модели определенного устройства
    def getModelsListByVendor(self, vendor_id: int):
        modelsList = self.db.prepare('SELECT array_to_json(array_agg(models_list)) '
                                     'FROM ('
                                     'SELECT "Vendor_Models".id AS model_id, '
                                     '"Vendors".id AS vendor_id, '
                                     '"Vendor_Models".name AS model_name, '
                                     '"Vendors".name AS vendor_name '
                                     'FROM "Vendors", "Vendor_Models" '
                                     'WHERE "Vendors".id = "Vendor_Models".vendor_id and "Vendor_Models".vendor_id = $1)'
                                     'models_list;')
        return json.loads(modelsList(vendor_id)[0][0])

    # il_kow Запросы для других классов
    # Получить все устройства - imei - (записывать пакет в БД или нет)
    def getDevicesListRaw(self):
        query = self.db.prepare('SELECT "devices".imei as imei FROM "devices"')
        return query()

    # Проверить через БД существование устройства по imei
    def imeiToCheck(self, imei: int):
        query = self.db.prepare('SELECT * FROM "devices" where "devices".imei = $1')
        response = query(imei)
        if response == []:
            return False
        else:
            return True
