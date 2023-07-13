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


def run_encryption(file_destination='G:/', key_destination='E:/',key_file='keys.txt', src_files=None, src_dir=None):
    # set up base src
    base_file = lambda a: f'file_{a}.txt'
    code_file = lambda a: f'codefile_{a}.txt'
    dir_name = '/encoding/'
    try:
        os.makedirs(file_destination + dir_name)
    except FileExistsError:
        pass
    file_destination += dir_name
    if src_files is None:
        src_files = []
    key_dict = []
    if src_dir:
        for file in os.listdir(src_dir):
            if '.txt' in file:
                src_files.append(src_dir + file)
                break
    amount = len(src_files)

    # remove all items from the <USBdir> (d:/)

    for item in os.listdir(file_destination):
        # DO NOT REMOVE SYSTEM VOLUME INFORMATION.
        # its special ;(
        if item == 'System Volume Information':
            continue
        os.remove(file_destination+ item)

    # continue 3 times (main goal)
    for i in range(amount):
        # open "file_#" and dump all lines from said file into the <dumplist>
        with open(src_files[i] if src_files else base_file(i + 1), 'r') as f:
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
        shutil.move(code_file(i + 1), file_destination)

    # Get the codes from the <keydict>, decode it into utf-8 and add it to the "keys.txt" file
    key_files = ["key1.txt", "key2.txt", "key3.txt"]
    index = 0
    for key in key_files:
        with open(key, 'w') as f:
            for index2, key2 in enumerate(key_dict):
                if index2 == index:
                    f.write(key2.decode('utf-8'))
        index+=1
        # move "keys.txt" to <USBdir>
        shutil.move(key, key_destination)


def run_decryption(decrypt_location='d:/encoding/', key_location=None, key_file_name='keys.txt', keys=None):
    if keys is None:
        keys = []
    key_src = key_location + key_file_name
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
    run_encryption(src_dir=os.path.dirname(__file__)+'/trying_dir/', key_destination="E:/")
    run_decryption()
