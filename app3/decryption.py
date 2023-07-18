import os
import random
from string import ascii_uppercase
import cv2
import numpy as np
from cryptography.fernet import Fernet, InvalidToken
from pyzbar.pyzbar import decode


def run(file_name, keep_running=True):
    cap = cv2.VideoCapture(0)
    data = None
    while keep_running:
        ret, frame = cap.read()
        keep_running, data = decoder(frame, file_name)
        cv2.imshow('Image', frame)
        code = cv2.waitKey(10)
        if code == ord('q'):
            break
    cv2.destroyAllWindows()
    return data


def decoder(image, file_name) -> bool:
    data, bartype, pos = QRSCAN(image)

    if data is "":
        # draws a string on the capture frame displaying the contents
        cv2.putText(image, bartype, (0, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return True, None
    elif data[-6] != "=" or len(data) != 49:
        bartype = "Invalid QR code"
        cv2.putText(image, bartype, pos,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return True, None

    # Seperate the key and code from the qr data
    key = data[:-5]
    extra_code = data[-4:]

    string = "Key: " + key + " | Code: " + extra_code + " | Type: " + bartype
    cv2.putText(image, string, pos,
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    print(string)

    try:
        # set the name for the code to decrypt here
        decrypted_text = try_decryption(get_USB_root(
            folter="encoding/") + file_name, str(key))
        if decrypted_text:
            create_decrypted_file(text=decrypted_text)
            # Stop running the capture frame when the file has been decrypted
            return False, decrypted_text
    except FileExistsError as error:
        print(error)
    return True, None


def QRSCAN(img):
    grey_img = cv2.cvtColor(img, 0)
    barcode = decode(grey_img)
    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pos = (x, y)
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        key = obj.data.decode("utf-8")

        if len(key) == 49:
            cv2.polylines(img, [pts], True, (0, 255, 0), 3)
        else:
            cv2.polylines(img, [pts], True, (0, 0, 255), 3)

        barcodeType = obj.type
        return key, str(barcodeType), pos
    return "", "No QR code found", ""


def _decrypt(key, data):
    f = Fernet(key)
    try:
        value = f.decrypt(data)
        return value
    except InvalidToken:
        return None


def try_decryption(encr_file_path: str, key: str) -> list | None:
    return_list = []
    with open(encr_file_path, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            msg = bytes(line, 'utf-8')
            text = _decrypt(key, msg)
            if (text is None):
                return None
            text = text.decode('utf-8')
            text = ''.join(text.splitlines())
            return_list.append(text)
    return return_list


def create_decrypted_file(decr_file_path=os.path.dirname(__file__)+"/decrypts/", text=[""]):
    try:
        file_name = "decrypted_file_" + text[0][:4]
    except IndexError:
        file_name = "decrypted_file_" + str(random.randint(100, 999))
    create_decrypts_folder()
    with open(decr_file_path+file_name+".txt", 'w', encoding="utf-8") as f:
        for line in text:
            f.write(line + "\n")

def create_decrypted_file_with_original_title(decr_file_path=os.path.dirname(__file__) + "/decrypts/", text=[""]):
    filename_sep = text[0].split('/')
    file_name = filename_sep[-1][:-4]
    create_decrypts_folder()
    with open(decr_file_path + file_name + ".txt", 'w', encoding="utf-8") as f:
        for line in text[1:]:
            f.write(line + "\n")

def create_decrypts_folder():
    """Create a dump folder if it doesnt exist yet"""
    if not "decrypts" in os.listdir(os.path.dirname(__file__)):
        os.makedirs(os.path.dirname(__file__) + "/decrypts")


def get_USB_root(check_for_no_filter=False, filter1="key", filter2=".txt", folter="") -> str:
    """Scans for drives D: through Z:"""
    for drive in ascii_uppercase[:-24:-1]:
        file_path = f"{drive}:/" + folter
        if os.path.exists(file_path):
            # create a list of files in the drive directory
            onlyfiles = [f for f in os.listdir(
                file_path) if os.path.isfile(os.path.join(file_path, f))]
            has_keys = False
            # Check to see if there is a file with 'key' in the name that is a '.txt' file
            for file in onlyfiles:
                if filter1 in file and filter2 in file:
                    has_keys = True
                    if check_for_no_filter:  # return the file path if you want the USB drive to contain a key
                        return file_path
                    break
            # If you dont want keys and no keys were found, return the file path
            if not has_keys and not check_for_no_filter:
                return file_path

    print('error, file not found')
    return None


if __name__ == '__main__':
    # pass
    run()
