import tkinter as tk
import os
import shutil
from string import ascii_uppercase

from cryptography.fernet import Fernet


def _get_USB_root():
    _file_trigger = False
    _key_trigger = False
    dirname_addon = 1

    """Scans for drives D: through Z:"""
    for drive in ascii_uppercase[:-24:-1]:
        file_path = f"{drive}:/"
        if os.path.exists(file_path):
            # designate a file_usb
            if not _file_trigger:
                for file in os.listdir(file_path):
                    # see how many previous tries are already on the usb
                    if 'encoding' in file:
                        dirname_addon +=1
                file_destination = file_path
                _file_trigger = True
                continue

            # designate a key_usb
            if not _key_trigger:
                key_destination = file_path
                _key_trigger = True
                continue
    return file_destination, key_destination, dirname_addon

def _get_coded_root(limit=['']):
    for drive in ascii_uppercase[:-24:-1]:
        file_path = f"{drive}:/"
        if file_path not in limit:
            if os.path.exists(file_path):
                return code_destination

        

def _encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)


def run_encryption(src_files=None, src_dir=None):
    global file_destination, key_destination,  dirname
    # set up base src
    def base_file(a):
        return f'file_{a}.txt'

    def code_file(a):
        return f'codefile_{a}.txt'

    def key_file(a, b):
        return f'key_file_{a}{b}.txt'

    # setup link between aplhabet and numbers, for naming purposes
    charstr = 'abcdefghijklmnopqrstuvwqyxABCDEFGHIJKLMNOPQRSTUVWXYZ'
    char_list = list(charstr)
    if src_files is None:
        src_files = []
    key_dict = []
    if src_dir:
        for file in os.listdir(src_dir):
            if '.txt' in file:
                src_files.append(src_dir + file)
    amount = len(src_files)

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
        file_names.append(code_file(i + 1))
    # Get the codes from the <keydict>, decode it into utf-8 and add it to the "keys.txt" file

    for num, key in enumerate(key_dict):
        filename = key_file(dirname, char_list[num])
        with open(filename, 'w') as f:
            f.write(key.decode('utf-8'))
        # move "keys.txt" to <USBdir>
        shutil.move(filename, key_destination)
    shutil.move(src_dir, file_destination)

def save_text():
    global file_destination, key_destination, code_destination, dirname
    # If all text fields are empty, return
    if all(texts[num].get(1.0, tk.END).strip() == '' for num in range(len(name))):
        return

    # constantly try to make a new dir, until u dont get one that doesnt exist yet
    a = 0
    while True:
        a += 1
        try:
            dir_name = f'files_{a}/'
            os.makedirs(dir_name)
            break
        except FileExistsError:
            pass

    for num in range(len(name)):
        # as long as file isnt empty, create new file with as title name[num].input
        if not texts[num].get(1.0, tk.END).strip() == '':
            file = open(dir_name + name[num].get() + ".txt", "w")
            file.write(texts[num].get(1.0, tk.END))
            file.close()

    # retrieve USB roots, destinations and how many previous tries have been done
    if not file_destination and not key_destination:
        file_destination, key_destination, dirname = _get_USB_root
        if not file_destination or not key_destination:
            print('please insert atleast 2 usbs')
            return
    # run encrypt
    run_encryption(src_dir=dir_name)

def save_to_usb():
    global file_destination, key_destination, code_destination, dirname
    limit = [file_destination, key_destination]
    code_destination = _get_coded_root(limit)
    dir_name = 'encoding_0/'
    a = 0
    while True:
        a += 1
        try:
            dir_name = f'encoding_{a}/'
            dirname = a
            os.makedirs(code_destination+dir_name)
            break
        except FileExistsError:
            pass
    code_destination += dir_name
    for name in file_names:
        shutil.move(name, code_destination)


if __name__ == '__main__':
    global file_destination, key_destination, code_destination, dirname
    file_destination, key_destination, code_destination, dirname = None, None, None, None
    count = 0
    window = tk.Tk()
    window.title("Data Encrypter")

    frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=5)
    frm_form.pack()

    name = []
    texts = []
    file_names = []

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
    save_to_usb_button = tk.Button(master=frm_buttons, text='save to usb', command=save_to_usb)
    save_to_usb_button.pack(side=tk.LEFT, padx =10, ipadx=10)

    window.mainloop()
