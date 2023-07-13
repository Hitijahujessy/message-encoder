from cryptography.fernet import Fernet
import os
import sys
import shutil
import qrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Decode QR
def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data: " + str(barcodeData) + " | Type: " + str(barcodeType)
        
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)
        try:
            run_decryption(keys=barcodeData)
        except FileNotFoundError as e:
            print(e)


def scan_qr():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        decoder(frame)
        cv2.imshow('Image', frame)
        code = cv2.waitKey(10)
        if code == ord('q'):
            break

def _decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)

def run_decryption(decrypt_location='d:/encoding/', key_file_name='keys.txt', keys=None):
    if keys is None:
        keys = []
    key_src = decrypt_location + key_file_name
    decrypted_name = lambda a: f'decrypted_file_{a}'
    dir = 'files/'
    decrypt_dict = []
    for file in os.listdir(decrypt_location):
        if file == 'System Volume Information':
            continue
        if file == key_file_name:
            continue
        decrypt_dict.append(decrypt_location + file)
    try:
        with open(key_src, 'r') as f:
            for line in f.readlines():
                keys.append(bytes(''.join(line.splitlines()), 'utf-8'))
    except FileNotFoundError:
        print('No decryption_key file', file=sys.stderr)

    try:
        os.makedirs(dir)
    except FileExistsError:
        pass

    for num, file in enumerate(decrypt_dict):
        dict = []
        with open(file, 'r') as f:
            for line in f.readlines():
                msg = bytes(line, 'utf-8')
                text = _decrypt(keys[num], msg)
                text = text.decode('utf-8')
                text = ''.join(text.splitlines())
                dict.append(text)
        with open(dir + decrypted_name(num + 1), 'w') as f:
            for line in dict:
                f.write(line + '\n')


if __name__ == '__main__':
    #scan_qr()
    #run_decryption()

    # Scan QR
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        decoder(frame)
        cv2.imshow('Image', frame)
        code = cv2.waitKey(10)
        if code == ord('q'):
            break
