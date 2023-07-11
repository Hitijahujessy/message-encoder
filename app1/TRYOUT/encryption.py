from cryptography.fernet import Fernet
import os
import sys
import shutil


def _encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)


def _decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)


def run_encryption(
        amount=3,
        USBdir='D:/',
        key_file='keys.txt',
        file_lib=None
):
    # key dict
    key_dict = []
    if file_lib:
        amount = len(file_lib)
    # set up base src
    base_file = lambda a: f'file_{a}.txt'
    code_file = lambda a: f'codefile_{a}.txt'

    # remove all items from the <USBdir> (d:/)
    for item in os.listdir(USBdir):
        # DO NOT REMOVE SYSTEM VOLUME INFORMATION.
        # its special ;(
        if item == 'System Volume Information':
            continue
        os.remove(USBdir + item)

    # continue 3 times (main goal)
    for i in range(amount):
        # open "file_#" and dump all lines from said file into the <dumplist>
        with open(file_lib[i] if file_lib else base_file(i + 1), 'r') as f:
            dump = []
            for line in f.readlines():
                dump.append(line)
            # Generate the most beautiful key ever seen and add it to the <key_dict>
            my_key = Fernet.generate_key()
            key_dict.append(my_key)
            # create <dict> for the encoded lines to go into
            dict = []
            for item in dump:
                item = bytes(item, 'utf-8')
                # This is where the magic happens
                encrypted_line = _encrypt(my_key, item)
                dict.append(encrypted_line)
        # create "codefile_#" and put all encoded lines from <dict> into said file
        with open(code_file(i + 1), 'w') as f:
            for text in dict:
                f.write(text.decode('utf-8') + '\n')
        # move "codefile_#" into the <USBdir>
        shutil.move(code_file(i + 1), USBdir)

    # Get the codes from the <keydict>, decode it into utf-8 and add it to the "keys.txt" file
    with open(key_file, 'w') as f:
        for key in key_dict:
            f.write(key.decode('utf-8') + '\n')
    # move "keys.txt" to <USBdir>
    shutil.move(key_file, USBdir)


def run_decryption(
        decrypt_location='d:/',
        key_file_name='keys.txt'
):
    keysrc = decrypt_location + key_file_name
    decrypt_dict = []
    for file in os.listdir(decrypt_location):
        if file == 'System Volume Information':
            continue
        if file == key_file_name:
            continue
        decrypt_dict.append(decrypt_location + file)
    keys = []
    try:
        with open(keysrc, 'r') as f:
            for line in f.readlines():
                keys.append(bytes(''.join(line.splitlines()), 'utf-8'))
    except FileNotFoundError:
        print('No decryption_key file', file=sys.stderr)

    for num, file in enumerate(decrypt_dict):
        with open(file, 'r') as f:
            for line in f.readlines():
                msg = bytes(line, 'utf-8')
                text = _decrypt(keys[num], msg)
                text = text.decode('utf-8')
                text = ''.join(text.splitlines())
                print(text)


if __name__ == '__main__':
    run_encryption()

    file_lib = ['hae.txt', 'howudoin.txt', 'ohmy.txt', 'dontwanna.txt']
    run_encryption(file_lib=file_lib)

    run_decryption()
