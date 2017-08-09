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

    # il_kow: Удалить устройство
    def deleteDevice(self, imei: int):
        device_delete = self.db.prepare("SELECT device_delete($1)")
        return device_delete(imei)[0][0]

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

    # il_kow Добавить разобранный пакет в таблицу decoded_packets
    def addDecodedPacket(self, imei: bytearray, data: bytearray):
        addRaw = self.db.prepare("INSERT INTO decoded_packets(id, device_id, data, timestamp, processed) values(DEFAULT, $1, $2, DEFAULT, DEFAULT)")
        devImei = ''
        for b in imei:
            devImei += chr(b)
        addRaw(int(devImei), data)
        logging.info('Device send packet: IMEI=' + str(imei) + ';')
        return

    # il_kow Получить все приемники
    def getReceiversList(self):
        receiversList = self.db.prepare('SELECT array_to_json(array_agg(receivers_list)) '
                                        'FROM ('        
                                            'SELECT "receivers".id as id, "receivers".name as name, '
                                            '"receivers".address as address, "receivers".port as port '
                                            'FROM "receivers")'
                                        'receivers_list;')
        return json.loads(receiversList()[0][0])

    # il_kow Добавить приемник
    def addReceiver(self, name:str, address:str, port:str):
        receiverAdd = self.db.prepare("SELECT receiver_add($1, $2, $3)")
        return receiverAdd(name, address, port)[0][0]

    # il_kow Редактировать приемник
    def updateReceiver(self, id:int, name:str, address:str, port:str ):
        receiverUpdate = self.db.prepare('UPDATE "receivers" SET name = $2, address = $3, port = $4 WHERE id = $1;')
        return receiverUpdate(id, name, address, port)

    # il_kow Получить приемники(получатели) - для дальнейшей отправки сигналов по ним
    def getDeviceReceivers(self, imei:int):
        singleDeviceReceivers = self.db.prepare('select "receivers".port, "receivers".address, "devices".imei, '
                                                ' "receivers".name from "devices" '
                                                ' inner join "device_receiver" on '
                                                ' "device_receiver".device_imei = "devices".imei '
                                                ' inner join "receivers" '
                                                ' on "device_receiver".receiver_id = "receivers".id ' 
                                                ' where "devices".imei = $1;')
        return singleDeviceReceivers(imei)

