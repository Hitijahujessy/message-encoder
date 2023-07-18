import tkinter as tk
import os
import shutil
from string import ascii_uppercase

from cryptography.fernet import Fernet


def _get_USB_root():
    file_destination = None
    key_destination = None
    _file_trigger = False
    _key_trigger = False
    dirname_addon = 1

    """Scans for drives D: through Z:"""
    for drive in ascii_uppercase[:-24:-1]:
        file_path = f"{drive}:/"
        if os.path.exists(file_path):
            # create a list of files in the drive directory
            if not _file_trigger:
                for file in os.listdir(file_path):
                    if 'encoding' in file:
                        dirname_addon +=1
                file_destination = file_path
                _file_trigger = True
                continue

            # Check to see if there is a file with 'key' in the name that is a '.txt' file
            if not _key_trigger:
                key_destination = file_path
                _key_trigger = True
                continue
    return file_destination, key_destination, dirname_addon


def _encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)


def run_encryption(file_destination='F:/', key_destination='H:/', src_files=None, src_dir=None,
                   dirname=''):
    # set up base src
    def base_file(a):
        return f'file_{a}.txt'

    def code_file(a):
        return f'codefile_{a}.txt'

    def key_file(a, b):
        return f'key_file_{a}{b}.txt'

    charstr = 'abcdefghijklmnopqrstuvwqyxABCDEFGHIJKLMNOPQRSTUVWXYZ'
    char_list = list(charstr)
    dir_name = f'/encoding{str(dirname)}/'
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
    amount = len(src_files)

    # remove all items from the <USBdir> (d:/)
    for item in os.listdir(file_destination):
        # DO NOT REMOVE SYSTEM VOLUME INFORMATION.
        # its special ;(
        if item == 'System Volume Information':
            continue
        os.remove(file_destination + item)

    # continue 3 times (main goal)
    for i in range(amount):
        # open "file_#" and dump all lines from said file into the <dumplist>
        with open(src_files[i] if src_files else base_file(i + 1), 'r') as f:
            dump = [src_files[i] if src_files else base_file(i + 1)]
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

    for num, key in enumerate(key_dict):
        filename = key_file(dirname, char_list[num])
        with open(filename, 'w') as f:
            f.write(key.decode('utf-8'))
        # move "keys.txt" to <USBdir>
        shutil.move(filename, key_destination)


def save_text():
    a = 0
    if all(texts[num].get(1.0, tk.END).strip() == '' for num in range(len(name))):
        return

    while True:
        a += 1
        try:
            dir_name = f'files_{a}/'
            os.makedirs(dir_name)
            break
        except FileExistsError:
            pass

    for num in range(len(name)):
        if not texts[num].get(1.0, tk.END).strip() == '':
            file = open(dir_name + name[num].get() + ".txt", "w")
            file.write(texts[num].get(1.0, tk.END))
            file.close()
        else:
            print('empty')
    file_destination, key_destination, dirname = _get_USB_root()
    run_encryption(src_dir=dir_name, key_destination=key_destination, file_destination=file_destination,
                   dirname=dirname)


if __name__ == '__main__':
    count = 0
    window = tk.Tk()
    window.title("Data Encrypter")

    frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=5)
    frm_form.pack()

    name = []
    texts = []

    text_amount = 3

    for count in range(text_amount):
        label = tk.Entry(master=frm_form, )
        label.grid(row=count, column=0, sticky="e")
        name.append(label)

        label = tk.Label(master=frm_form, text='.txt')
        label.grid(row=count, column=1)

        text = tk.Text(master=frm_form, width=50, height=10)
        text.grid(row=count, column=2)
        texts.append(text)

    frm_buttons = tk.Frame()
    frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

    submit_button = tk.Button(master=frm_buttons, text="Submit", command=save_text)
    submit_button.pack(side=tk.RIGHT, padx=10, ipadx=10)

    window.mainloop()
