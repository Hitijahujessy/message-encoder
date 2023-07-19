import tkinter as tk
import os
import shutil
from string import ascii_uppercase

from cryptography.fernet import Fernet
global key_destination, file_destination
key_destination, file_destination = None, None

def _get_USB_root():
    _file_trigger = False
    _key_trigger = False

    """Scans for drives D: through Z:"""
    for drive in ascii_uppercase[:-24:-1]:
        file_path = f"{drive}:/"
        if os.path.exists(file_path):
            # designate a file_usb
            if not _file_trigger:
                    # see how many previous tries are already on the usb
                file_destination = file_path
                _file_trigger = True
                continue

            # designate a key_usb
            if not _key_trigger:
                key_destination = file_path
                _key_trigger = True
                continue
    return file_destination, key_destination

def _get_coded_root(limit=['']):
    for drive in ascii_uppercase[:-24:-1]:
        file_path = f"{drive}:/"
        if file_path not in limit:
            if os.path.exists(file_path):
                return file_path

def _encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)

def run_encryption(file_destination='F:/', key_destination='H:/', src_files=None, src_dir=None):
    # set up base src
    def base_file(a): return f'file_{a}.txt'
    def code_file(a): return f'codefile_{a}.txt'
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
    amount = len(src_files)
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
        list.append(code_file(i + 1))


    # Get the codes from the <keydict>, decode it into utf-8 and add it to the "keys.txt" file
    key_files = ["key1.txt", "key2.txt", "key3.txt"]
    index = 0
    for key in key_files:
        with open(key, 'w') as f:
            for index2, key2 in enumerate(key_dict):
                if index2 == index:
                    f.write(key2.decode('utf-8'))
        index += 1
        # move "keys.txt" to <USBdir>
        shutil.move(key, key_destination)

    shutil.move(src_dir, file_destination)

count = 0
window = tk.Tk()
window.title("Data Encrypter")

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=5)
frm_form.pack()

Labels = [
    "text 1",
    "text 2",
    "text 3",
]
list = []

def save_text():
    global key_destination, file_destination
    dir_name = 'start_files/'
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        pass
    
    text_file_1 = open(dir_name+ "text_1.txt", "w")
    text_file_1.write(text_1.get(1.0, tk.END))
    text_file_1.close()

    text_file_2 = open(dir_name+ "text_2.txt", "w")
    text_file_2.write(text_2.get(1.0, tk.END))
    text_file_2.close()

    text_file_3 = open(dir_name+ "text_3.txt", "w")
    text_file_3.write(text_3.get(1.0, tk.END))
    text_file_3.close()

    file_destination, key_destination = _get_USB_root()
    run_encryption(file_destination=file_destination, key_destination=key_destination, src_dir=dir_name)

def save_to_usb():
    global key_destination, file_destination
    code_destination = _get_coded_root([key_destination, file_destination])
    try:
        os.makedirs(code_destination + 'encoding/')
    except FileExistsError:
        pass
    code_destination += 'encoding/'
    for items in list:
        shutil.move(items, code_destination)
    
for count, text in enumerate(Labels):

    label = tk.Label(master=frm_form, text=text)
    label.grid(row=count, column=0, sticky="e")

text_1 = tk.Text(master=frm_form, width=50, height=10)
text_1.grid(row=0, column=1)

text_2 = tk.Text(master=frm_form, width=50, height=10)
text_2.grid(row=1, column=1)

text_3 = tk.Text(master=frm_form, width=50, height=10)
text_3.grid(row=2, column=1)

frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

submit_button = tk.Button(master=frm_buttons, text="Submit", command=save_text)
submit_button.pack(side=tk.RIGHT, padx=10, ipadx=10)
save_to_usb_button = tk.Button(master=frm_buttons, text='save to usb', command=save_to_usb)
save_to_usb_button.pack(side=tk.LEFT, padx =10, ipadx=10)

window.mainloop()
