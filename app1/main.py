import tkinter as tk

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

def save_text():
   text_file_1 = open("text_1.txt", "w")
   text_file_1.write(text_1.get(1.0, tk.END))
   text_file_1.close()

   text_file_2 = open("text_2.txt", "w")
   text_file_2.write(text_2.get(1.0, tk.END))
   text_file_2.close()

   text_file_3 = open("text_3.txt", "w")
   text_file_3.write(text_3.get(1.0, tk.END))
   text_file_3.close()

for count, text in enumerate(Labels):

    label = tk.Label(master=frm_form, text=text)
    label.grid(row=count, column=0, sticky="e")

text_1 = tk.Text(master=frm_form, width= 50, height=10)
text_1.grid(row=0, column=1)

text_2 = tk.Text(master=frm_form, width= 50, height=10)
text_2.grid(row=1, column=1)

text_3 = tk.Text(master=frm_form, width= 50, height=10)
text_3.grid(row=2, column=1)

frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

submit_button = tk.Button(master=frm_buttons, text="Submit", command=save_text)
submit_button.pack(side=tk.RIGHT, padx=10, ipadx=10)

window.mainloop()