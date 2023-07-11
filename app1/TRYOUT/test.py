from cryptography.fernet import Fernet
import sys
import os

def my_decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)

USBdir = 'd:/'
keysrc = None
decrypt_dict = []
for file in os.listdir(USBdir):
    if file == 'System Volume Information':
        continue
    if 'keys' in file:
        keysrc = USBdir + file
        continue
    decrypt_dict.append(USBdir+file)

if not keysrc:
    print('No decryptkey file', file=sys.stderr)
    sys.exit()
keys = []
with open(keysrc, 'r') as f:
    for line in f.readlines():
        keys.append(bytes(''.join(line.splitlines()), 'utf-8'))


for num, file in enumerate(decrypt_dict):
    with open(file, 'r') as f:
        for line in f.readlines():
            msg = bytes(line, 'utf-8')
            text = my_decrypt(keys[num], msg)
            text = text.decode('utf-8')
            text = ''.join(text.splitlines())
            print(text)
