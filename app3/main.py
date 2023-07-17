import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import decryption

import os


class Main():

    dir = decryption.get_USB_root(folter="/encoding/")  # String to hold directory path, should lead to encoded-fileS USB

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Data Decryptor")
        self.decrypted_text = ""

        self._create_GUI()
        self.get_dir()
        
        

    def _create_GUI(self):

        # Create the outer frame
        self.outer_frame = tk.Frame(
            master=self.window, relief=tk.SUNKEN, borderwidth=5, width=500, height=400, padx=20, pady=20)
        self.outer_frame.grid()

        # Create file chooser and box that displays text of the decoded file
        frame_size = 150
        self.trv = ttk.Treeview(master=self.outer_frame, selectmode='browse')
        # self.frame_left = tk.Frame(master=self.outer_frame, relief=tk.SUNKEN, borderwidth=2, width=frame_size, height=frame_size)
        self.frame_right = tk.Frame(
            master=self.outer_frame, relief=tk.SUNKEN, borderwidth=2, width=frame_size, height=frame_size)
        # self.frame_left.grid(column=1, row=1)
        self.frame_right.grid(column=3, row=1)

        # Create the button for QR
        self.qr_button = tk.Button(self.outer_frame, text="Scan QR", width=10, command=lambda: [
                                   select_file(), print("filename:", self.file_name), get_decrypted_text()])
        self.qr_button.grid(column=2, row=1, padx=10)
        self.decrypt_button = tk.Button(
            self.outer_frame, text="Decrypt", width=10, command=self._decrypt)

        # Create the labels inside the textboxes
        # self.label_left = tk.Label(self.frame_left, width=50, height=20)
        # self.label_left.pack()
        self.label_right = tk.Label(self.frame_right, width=50, height=20, text=self.decrypted_text, wraplength=300, justify='left')
        self.label_right.pack()

        # TreeView

        # Shows selected directory, might be of use when debugging/testing
        self.l1 = tk.Label(self.outer_frame,text=dir, font=16)
        self.l1.grid(row=0,column=0,padx=0)

        # trv = ttk.Treeview(self.outer_frame,selectmode='browse',height=9)
        self.trv.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.trv["columns"] = ("1")
        self.trv['show'] = 'tree headings'
        self.trv.column("#0", width=20, anchor='c')
        self.trv.column("1", width=300, anchor='w')
        self.trv.heading("#0", text="#")
        self.trv.heading("1", text="Name", anchor='w')
        
        def select_file():
            self.selected_file = self.trv.focus()
            self.file_details = self.trv.item(self.selected_file)
            self.file_name = self.file_details.get("values")[0]
            # print(self.file_name)
            
        def get_decrypted_text():
            self.decrypted_text = decryption.run()
            self.label_right.config(text=self.decrypted_text)

    def get_dir(self):

        path = self.dir  # select directory
        self.l1.config(text=path) # update the text of Label with directory path
        dirnames = next(os.walk(path))[1]  # list of directories
        files = next(os.walk(path))[2] # list of files
        for item in self.trv.get_children():
            self.trv.delete(item)
        i = 1
        f2i = 1  # sub directory id
        for d in dirnames:
            self.trv.insert("", 'end', iid=i, values=d)
            path2 = path + '/' + d  # Path for sub directory
            # print(path2)
            files2 = next(os.walk(path2))[2]  # file list of Sub directory
            for f2 in files2:  # list of files
                # print(f2)
                self.trv.insert(i, 'end', iid='sub'+str(f2i), values="-" + f2)
                f2i = f2i + 1
            i = i + 1
        for f in files:  # list of files
            self.trv.insert("", 'end', iid=i, values=f)
            i = i + 1



    def run(self):
        self.window.mainloop()

    def _scan_qr(self):
        print("qr")
        self._switch_qr_decrypt()

    def _decrypt(self):
        print("decrypt")
        self._switch_qr_decrypt()

    def _switch_qr_decrypt(self):
        if (self.qr_button.winfo_ismapped()):
            self.qr_button.grid_remove()
            self.decrypt_button.grid(column=2, row=1, padx=10)
        elif (self.decrypt_button.winfo_ismapped()):
            self.decrypt_button.grid_remove()
            self.qr_button.grid(column=2, row=1, padx=10)


main = Main()
main.run()
