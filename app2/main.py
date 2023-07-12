
import os
import sys
from string import ascii_uppercase
import random as rng
import qrcode
import datetime
from qrcode.image.pure import PyPNGImage


class QRSCANNER():
    
    def __init__(self):
        self.find_all_keys_and_convert()
        
    def find_all_keys_and_convert(self):
        keys = self.read_USB()
        if not keys:
            print("no keys found")
        for key in keys:
            with open(self.get_USB_root()+key, encoding = "utf-8") as f:
                data = f.read()
            letters = self.create_extra_code()
            img = self.create_QR(data+letters)
            self.save(img, f"QR_{letters}.png")
        
    def save(self, img: PyPNGImage, name: str):
        path = os.getcwd() + "/app2/dump/"
        img.save(path+name)
        
        # save to usb stick if inserted
        root = self.get_USB_root(False)
        if not root:
            return
        img.save(root + name)

    def get_USB_root(self, check_for_keys=True) -> str:
        """Scans for drives D: through Z:"""
        for drive in ascii_uppercase[:-24:-1]:
            file_path = f"{drive}:/"
            if os.path.exists(file_path):
                onlyfiles = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
                has_keys = False
                for file in onlyfiles:
                    if "key" in file:
                        has_keys = True
                        if check_for_keys:
                            return file_path
                if not has_keys:
                    return file_path
                

        print('error, file not found')
        return None


    def read_USB(self) -> list:
        """Returns the contents of the file as a string"""
        root = self.get_USB_root()
        onlyfiles = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
        txtfiles = []
        for file in onlyfiles:
            if ".txt" in file:
                txtfiles.append(file)
        return txtfiles
    
    def create_QR(self, data) -> PyPNGImage:
        img = qrcode.make(data, image_factory=PyPNGImage)
        return img
    
    def create_extra_code(self) -> str:
        letters = ""
        i = 0
        while i < 4:
            letters += ascii_uppercase[rng.randrange(1, 26)]
            i+=1
        self.save_extra_code(letters)
        return "_" + letters
    
    def save_extra_code(self, letters):
        root = os.getcwd()
        try:
            f = open(root+f"/app2/dump/{letters}.txt", 'x+', encoding="utf-8")
        except FileExistsError:
            f = open(root+f"/app2/dump/{letters}.txt", 'r+', encoding="utf-8")
        f.writelines(letters + " " + datetime.datetime.now(tz=None).strftime("%d/%m/%Y"))
        f.close()

qr = QRSCANNER()
