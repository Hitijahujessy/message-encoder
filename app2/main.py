
import os
import sys
from string import ascii_uppercase
import random as rng

import qrcode
from qrcode.image.pure import PyPNGImage

qr = qrcode.QRCode()

class QRSCANNER():
    
    def __init__(self):
        data = self.read_USB()
        letters = self.create_Extra_Code()
        img = self.create_QR(data+letters)
        with open("/app2")

    def get_USB_root(self) -> str:
        """Scans for drives D: through Z:"""
        for drive in ascii_uppercase[:-24:-1]:
            file_path = f"{drive}:/keys/"
            if os.path.exists(file_path):
                return file_path

        print('error, file not found')
        sys.exit(1)


    def read_USB(self, keyno=1) -> str:
        """Returns the contents of the file as a string"""
        root = self.get_USB_root()
        file_path = root + "key" + str(keyno) + ".txt"
        with open(file_path) as file:
            data = file.read()
        return data
    
    def create_QR(data):
        qr.add_data(data)
        qr.make()
        img = qrcode.make(data, image_factory=PyPNGImage)
        return img
    
    def create_Extra_Code() -> str:
        indexes = [0,1,2,3]
        letters = ""
        for i in indexes:
           letters += ascii_uppercase[rng.randrange(1, 27)]
        return letters

qr = QRSCANNER()
