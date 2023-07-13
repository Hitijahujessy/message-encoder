
import os
import sys
from string import ascii_uppercase
import random as rng
import qrcode
import datetime
from qrcode.image.pure import PyPNGImage


class QRSCANNER():
    
    def __init__(self):
        self.create_dump_folder()
        self.find_all_keys_and_convert()
        
    def find_all_keys_and_convert(self):
        """"""
        # get a list of paths to the keys
        key_paths = self.read_USB()
        if not key_paths:
            print("no keys found")
        for key in key_paths:
            with open(self.get_USB_root(True)+key, encoding = "utf-8") as f:
                data = f.read()
            letters = self.create_extra_code()
            img = self.create_QR(data+letters)
            self.save(img, f"QR_{letters}.png")
            
    def create_dump_folder(self):
        """Create a dump folder if it doesnt exist yet"""
        if not "dump" in os.listdir(os.path.dirname(__file__)):
            os.makedirs(os.path.dirname(__file__) + "/dump")
        
    def save(self, img: PyPNGImage, name: str):
        """Save the QR image to the dump folder and try to upload to an USB stick with no keys on it"""
        path = os.path.dirname(__file__) + "/dump/"
        img.save(path+name)
        # save to usb stick if inserted
        root = self.get_USB_root()
        if not root:
            return
        img.save(root + name)

    def get_USB_root(self, check_if_keys=False) -> str:
        """Scans for drives D: through Z:"""
        for drive in ascii_uppercase[:-24:-1]:
            file_path = f"{drive}:/"
            if os.path.exists(file_path):
                # create a list of files in the drive directory
                onlyfiles = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
                has_keys = False
                # Check to see if there is a file with 'key' in the name that is a '.txt' file
                for file in onlyfiles:
                    if "key" in file and ".txt" in file:
                        has_keys = True
                        if check_if_keys: # return the file path if you want the USB drive to contain a key
                            return file_path
                        break
                # If you dont want keys and no keys were found, return the file path
                if not has_keys and not check_if_keys:
                    return file_path
                
        print('error, file not found')
        return None


    def read_USB(self, string_filter="key", extension_filter=".txt") -> list:
        """Returns a list of strings that are paths to a key file. \n
        ex: 'key.txt'"""
        root = self.get_USB_root(check_if_keys=True)
        # seperate files from directories
        onlyfiles = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
        # create a list containing files that have both filters in its name
        txtfiles = []
        for file in onlyfiles:
            if extension_filter & string_filter in file:
                txtfiles.append(file)
        return txtfiles
    
    def create_QR(self, data) -> PyPNGImage:
        """Turns a text string into a QR code"""
        img = qrcode.make(data, image_factory=PyPNGImage)
        return img
    
    def create_extra_code(self) -> str:
        """Create a random string of 4 capital letters and underscore and save it to the dump folder. \n
            ex. Return : "_GASK"
        """
        letters = ""
        i = 0
        while i < 4:
            letters += ascii_uppercase[rng.randrange(1, 26)]
            i+=1
        self.save_extra_code(letters)
        return "_" + letters
    
    def save_extra_code(self, letters):
        root = os.path.dirname(__file__)
        # Create a txt file and write the key and code to it
        try:
            f = open(root+f"/dump/{letters}.txt", 'x+', encoding="utf-8")
        except (FileExistsError):
            f = open(root+f"/dump/{letters}.txt", 'r+', encoding="utf-8")
        f.writelines(letters + " " + datetime.datetime.now(tz=None).strftime("%d/%m/%Y"))
        f.close()

qr = QRSCANNER()
