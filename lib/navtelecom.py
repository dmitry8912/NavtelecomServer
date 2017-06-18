import string
import struct
import logging
import socket
from lib import datadict
from lib import crc8custom
from lib import postgres
from lib import nvg

class Navtelecom:
    myId = 1
    def __init__(self):
        self.connected = {}
        self.clients = {}
        return

    def __del__(self):
        return

    def xor_sum(self, array: bytearray):
        sum = 0x00
        for number in array:
            sum ^= number
        return sum

    def send(self, header: bytearray, request: string, recieverid: bytearray, senderid: int):
        data = bytearray()
        for char in header:
            data.append(char)

        # reciever = self.int_to_byte_arrray(recieverid, 4)
        for rbyte in recieverid:
            data.append(rbyte)

        sender = self.int_to_byte_arrray(senderid, 4)
        for sbyte in sender:
            data.append(sbyte)

        datalen = self.int_to_byte_arrray(len(request),2);
        for lbyte in datalen:
            data.append(lbyte)

        request_bytes = request.encode('ascii')
        data_checksum = self.xor_sum(request_bytes)
        data.append(data_checksum)
        data.append(self.xor_sum(data))
        for data_byte in request_bytes:
            data.append(data_byte)
        return data

    def sendBytes(self, header: bytearray, request: bytearray, recieverid: bytearray, senderid: int):
        data = bytearray()
        for char in header:
            data.append(char)

        # reciever = self.int_to_byte_arrray(recieverid, 4)
        for rbyte in recieverid:
            data.append(rbyte)

        sender = self.int_to_byte_arrray(senderid, 4)
        for sbyte in sender:
            data.append(sbyte)

        datalen = self.int_to_byte_arrray(len(request),2);
        for lbyte in datalen:
            data.append(lbyte)

        data_checksum = self.xor_sum(request)
        data.append(data_checksum)
        data.append(self.xor_sum(data))
        for data_byte in request:
            data.append(data_byte)
        return data

    def int_to_byte_arrray(self, num: int, length: int):
        return num.to_bytes(length, byteorder='little')

    def read(self, response: bytearray, connection):
        if(len(response) < 16):
            return False
        xor_checksum_header = self.xor_sum(response[:15])
        if(xor_checksum_header != response[15]):
            return False

        data_checksum = self.xor_sum(response[16:])
        if(data_checksum != response[14]):
            return False

        if(self.getClient(connection) == None):
            self.clients.update({ response[20:]: connection })
            self.connected.update({ response[20:]: { 'id':response[8:12], 'preambule': response[0:4], 'fields': [] }})
            db = postgres.NavtelecomDB.getInstance()
            db.connectDevice(response[20:],response[8:12])

        return response[16:len(response)]

    def makeHandshake(self,ntp):
        client = self.getClient(ntp)
        data = self.send(client['preambule'],'*<S',client['id'],self.myId)
        ntp.transport.write(data)
        return

    def flexExec(self,data,connection):
        if(not self.checkCRC(data)):
            print('CRC Corrupt')
            return
        else:
            db = postgres.NavtelecomDB.getInstance()
            db.addRawPacket(self.getImei(connection),data)
            connection.transport.write(self.formAnswer(data))
        client = self.getClient(connection)
        #decode current state
        if(data[:2] == b'~C'):
            telemetry = data[2:len(data) - 1]
            decoded = self.decodeTelemetry(telemetry, client)

        #decode alarm package and\or additional package
        if (data[:2] == b'~T' or data[:2] == b'~X'):
            if(data[:2] == b'~T'):
                telemetry = data[6:len(data) - 1]
                decoded = self.decodeTelemetry(telemetry, client)
            if(data[:2] == b'~X'):
                telemetry = data[6:len(data) - 1]
                decoded = self.decodeAdditionalTelemetry(telemetry)
        else:
            #decode array and array of additional packages
            size = int(len(data[3:-1]) / data[2])
            count = int(data[2])
            start = 3
            while (count > 0):
                if(data[:2] == b'~A'):
                    decoded = self.decodeTelemetry(data[start:start+size],client)
                else:
                    if(data[:2] == b'~E'):
                        decoded = self.decodeAdditionalTelemetry(data[start:start + size])
                start += size
                count -= 1

    def checkCRC(self, data: bytearray):
        crc = crc8custom.crc8()
        if(data[len(data)-1] == crc.crc(data[:-1])):
            return True
        else:
            return False

    def coordinateFlexVersion(self,data,connection):
        #flex v check
        if(data[6] == 0xB0 and data[7] == 0x14 and data[8] == 0x14):
            bitfield = data[10:]
            fields = []
            fieldnum = 1
            for bit in bitfield:
                j = 0x80
                while(j > 0):
                    if(bit & j > 0):
                        fields.append(fieldnum)
                    j = j >> 1
                    fieldnum += 1
            imei = self.getImei(connection)
            self.connected[imei]['fields'] = fields
            db = postgres.NavtelecomDB.getInstance()
            db.setFields(imei,fields)
        #FLEX 2.0 struct 2.0
        response = bytearray(b'*<FLEX')
        response.append(0xB0)
        response.append(0x14)
        response.append(0x14)
        client = self.getClient(connection)
        data = self.sendBytes(client['preambule'], response, client['id'], self.myId)
        connection.transport.write(data)
        return

    def getClient(self,connection):
        try:
            imei = list(self.clients.keys())[list(self.clients.values()).index(connection)]
            client = self.connected[imei]
        except ValueError:
            return None
        return client

    def getImei(self,connection):
        try:
            imei = list(self.clients.keys())[list(self.clients.values()).index(connection)]
        except ValueError:
            return None
        return imei

    def disconnect(self,connection):
        try:
            imei = list(self.connected.keys())[list(self.clients.values()).index(connection)]
            del self.connected[imei]
            del self.clients[imei]
        except ValueError:
            return
        return

    def formAnswer(self,data):
        response = bytearray()
        crc = crc8custom.crc8()
        for b in data[:2]:
            response.append(b)
        if(data[:2] == b'~C'):
            response.append(crc.crc(response))
            return response
        lastIndex = 3
        if(data[:2] == b'~X' or data[:2] == b'~T'):
            lastIndex = 6
        for b in data[2:lastIndex]:
            response.append(b)

        response.append(crc.crc(response))
        return response

    def decodeTelemetry(self,telemetry: bytearray, client: dict):
        result = {}
        offset = 0
        for f in client['fields']:
            if ('composite' in datadict.flexdictionary[f - 1] and datadict.flexdictionary[f - 1]['composite']):
                result[f] = { 'name': datadict.flexdictionary[f - 1]['name'], 'value': 'complex',
                              'bytes': telemetry[offset:offset + datadict.flexdictionary[f - 1]['size']], 'fieldnum': f }
            else:
                if (datadict.flexdictionary[f - 1]['type'] == 'I'):
                    value = int.from_bytes(telemetry[offset:offset + datadict.flexdictionary[f - 1]['size']],
                                           byteorder='little', signed=datadict.flexdictionary[f - 1]['signed'])

                if (datadict.flexdictionary[f - 1]['type'] == 'F'):
                    value = struct.unpack('f', telemetry[offset:offset + datadict.flexdictionary[f - 1]['size']])

                result[f] = {'name': datadict.flexdictionary[f - 1]['name'], 'value': value,
                             'bytes': telemetry[offset:offset + datadict.flexdictionary[f - 1]['size']], 'fieldnum': f }

            offset += datadict.flexdictionary[f - 1]['size']
        return result

    def decodeAdditionalTelemetry(self, telemetry: bytearray):
        result = []
        offset = 0
        for f in datadict.additionalpackagedict:
            if ('composite' in f and f['composite']):
                result.append({'name': f['name'], 'value': 'complex', 'bytes': telemetry[offset:offset + f['size']]})
            else:
                if (f['type'] == 'I'):
                    value = int.from_bytes(telemetry[offset:offset + f['size']], byteorder='little', signed=f['signed'])
                if (f['type'] == 'F'):
                    value = struct.unpack('f', telemetry[offset:offset + f['size']])
                result.append({'name': f['name'], 'value': value,
                             'bytes': telemetry[offset:offset + f['size']]})
            offset += f['size']
        return result

    def decodeFlexFromDB(self, sock: socket):
        self.sock = sock
        db = postgres.NavtelecomDB.getInstance()
        packets = db.getNotDecodedPackets()
        for packet in packets:
            packet_id = packet[0]
            imei = str(packet[1]).encode()
            client = {'fields':db.getField(packet[1])[0][0]}
            data = packet[2]
            if (data[:2] == b'~C'):
                telemetry = data[2:len(data) - 1]
                decoded = self.decodeTelemetry(telemetry, client)

                # decode alarm package and\or additional package
            if (data[:2] == b'~T' or data[:2] == b'~X'):
                if (data[:2] == b'~T'):
                    telemetry = data[6:len(data) - 1]
                    decoded = self.decodeTelemetry(telemetry, client)
                    print(decoded)
                    self.sendToNVG(self.toNVG(imei,decoded,client['fields']),packet_id)
                if (data[:2] == b'~X'):
                    telemetry = data[6:len(data) - 1]
                    decoded = self.decodeAdditionalTelemetry(telemetry)
            else:
                # decode array and array of additional packages
                size = int(len(data[3:-1]) / data[2])
                count = int(data[2])
                start = 3
                while (count > 0):
                    if (data[:2] == b'~A'):
                        decoded = self.decodeTelemetry(data[start:start + size], client)
                        print(decoded)
                        self.sendToNVG(self.toNVG(imei, decoded, client['fields']),packet_id)
                    else:
                        if (data[:2] == b'~E'):
                            decoded = self.decodeAdditionalTelemetry(data[start:start + size])
                    start += size
                    count -= 1

    def toNVG(self,imei: bytearray, data: list, fields: list):
        packet = nvg.NVG()
        packet.addIdentifier(imei)
        for f in fields:
            if(f == 3):
                packet.addTime(data[f]['value'])
        packet.addCoordinates(data[10]['value'],data[11]['value'],1,data[13]['value'],data[14]['value'],int.from_bytes(data[8]['bytes'],byteorder='little') ^ 0b11000000)
        return packet.getPacket()

    def additionalToNVG(self,imei,data: list):
        packet = nvg.NVG()
        packet.addIdentifier(imei)
        for f, v in data:
            if(f == 3):
                packet.addTime(data[f]['value'])
            if(f == 2):
                return
        packet.addCoordinates(data[5]['value'],data[6]['value'],data[7]['value'],data[8]['value'],data[8] ^ 0b11000000)
        return packet.getPacket()

    def sendToNVG(self,data:bytearray, packet_id):
        logging.info('packet_id='+str(packet_id))
        print('packet_id=' + str(packet_id))
        import socket
        self.sock.send(data)
        rdata = self.sock.recv(1024)
        if(rdata[0] == 0x55 and rdata[1:5] == data[0:4]):
            logging.info("NVG SEND OK")
            print("NVG SEND OK")
            db = postgres.NavtelecomDB.getInstance()
            db.markPacket(packet_id)
        else:
            logging.info('NVG ERROR')
            print("NVG ERROR")
            logging.debug(rdata[0])
            logging.debug(rdata[1:5])
            logging.debug(data[0:4])