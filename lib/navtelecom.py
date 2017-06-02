import serial
import string
import binascii
import array


class Navtelecom:
    deviceSerial = None

    def __init__(self, serialinstance: serial):
        self.deviceSerial = serialinstance
        if(not self.deviceSerial.is_open):
            self.deviceSerial.open()
        return

    def __del__(self):
        self.deviceSerial.close()

    def xor_sum(self, array: bytearray):
        sum = 0x00
        for number in array:
            sum ^= number
        return sum

    def send(self, header: string, request: string, recieverid: int, senderid: int):
        data = bytearray()
        for char in header:
            data.append(ord(char))

        sender = self.int_to_byte_arrray(senderid, 4)
        for sbyte in sender:
            data.append(sbyte)

        reciever = self.int_to_byte_arrray(recieverid, 4)
        for rbyte in reciever:
            data.append(rbyte)

        datalen = self.int_to_byte_arrray(len(request),2);
        for lbyte in datalen:
            data.append(lbyte)

        request_bytes = request.encode('ascii')
        data_checksum = self.xor_sum(request_bytes)
        data.append(data_checksum)
        data.append(self.xor_sum(data))
        for data_byte in request_bytes:
            data.append(data_byte)

        if(self.deviceSerial.is_open):
            self.deviceSerial.write(data)

    def int_to_byte_arrray(self, num: int, length: int):
        return num.to_bytes(length, byteorder='little')

    def read(self):
        response = self.deviceSerial.readline()
        xor_checksum_header = self.xor_sum(response[:15])
        if(xor_checksum_header != response[15]):
            return False

        data_checksum = self.xor_sum(response[16:])
        if(data_checksum != response[14]):
            return False

        return response[16:len(response)]
