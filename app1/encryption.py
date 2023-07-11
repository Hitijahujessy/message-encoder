from cryptography.fernet import Fernet
import os
import shutil


def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)


def run_encryption(amount=3):
    # key dict
    key_dict = []

    # set up base src
    USBdir = 'D:/'
    key_file = f'keys.txt'
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
        with open(base_file(i + 1), 'r') as f:
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
                encrypted_line = encrypt(my_key, item)
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


if __name__ == '__main__':
    run_encryption()
