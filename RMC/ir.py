import brl as broadlink
import configparser
import sys
import time, binascii
import netaddr
import string
from os import path
from Crypto.Cipher import AES


class RM3Mini():
    def __init__(self, ip, mac, port):
        self.IPAddress = ip
        self.MACAddress = netaddr.EUI(mac)
        self.Port = port
        self.Timeout = 10
        self.device = broadlink.rm((self.IPAddress, self.Port), self.MACAddress, self.Timeout)
        self.device.auth()

    def reauthorize(self):
        self.device = broadlink.rm((self.IPAddress, self.Port), self.MACAddress, self.Timeout)
        self.device.auth()

    def sendIR(self, command):
        DecodedCommand = command.decode('hex')
        self.device.send_data(DecodedCommand)

    def recordIR(self):
        EncodedCommand = '000000000000000000000000'
        while(EncodedCommand=='000000000000000000000000'):
            print('READING IR SIGNAL...')
            self.device.enter_learning()
            time.sleep(self.Timeout)
            LearnedCommand = self.device.check_data()
            if LearnedCommand is None:
                return None
            EncodedCommand = LearnedCommand.encode('hex')
            print(EncodedCommand)
            self.reauthorize()
        return EncodedCommand


# if __name__ == '__main__':
#     RM3Device = RM3Mini(RealIPAddress, RealMACAddress, RealPort)
#     try:
#         while True:
#             command = raw_input('SELECT MODE... -c:LIGHT -r:REGISTER & DO >>> ')
#             if(command=='-c'):
#                 RM3Device.sendIR(LIGHT)
#             elif(command=='-r'):
#                 tmpCommand = RM3Device.recordIR()
#                 if(tmpCommand is not None):
#                     RM3Device.sendIR(tmpCommand)
#     except KeyboardInterrupt:
#         sys.exit()
