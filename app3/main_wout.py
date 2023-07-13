import tkinter as tk

class Main():
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Data Decrypter")

        
        
        self._create_GUI()
    
    def _create_GUI(self):
        
        # Create the outer frame
        self.outer_frame = tk.Frame(master=self.window, relief=tk.SUNKEN, borderwidth=5, width=500, height=400, padx=20, pady=20)
        self.outer_frame.grid()
        
        # Create two boxes where the text will go
        frame_size = 150
        self.frame_left = tk.Frame(master=self.outer_frame, relief=tk.SUNKEN, borderwidth=2, width=frame_size, height=frame_size)
        self.frame_right = tk.Frame(master=self.outer_frame, relief=tk.SUNKEN, borderwidth=2, width=frame_size, height=frame_size)
        self.frame_left.grid(column=1, row=1)
        self.frame_right.grid(column=3, row=1)
        
        # Create the button for QR
        self.qr_button = tk.Button(self.outer_frame, text="Scan QR", width=10, command=self._scan_qr)
        self.qr_button.grid(column=2, row=1, padx=10)
        self.decrypt_button = tk.Button(self.outer_frame, text="Decrypt", width=10, command=self._decrypt)
        
        # Create the labels inside the textboxes
        self.label_left = tk.Label(self.frame_left, width=50, height=20)
        self.label_left.pack()
        self.label_right = tk.Label(self.frame_right, width=50, height=20)
        self.label_right.pack()
    
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