import os.path
import time
import random
import tkinter as tk
from tkinter import * 

window = tk.Tk(className="python Cyberpunk 2077 Breach Protocol Solver")
window.geometry("1024x576")
window.configure(background="#16151b")

title = tk.Frame(master=window,height='100',bg="#16151b")
title.pack(fill=tk.X)
title.pack_propagate(False)
title_label = tk.Label(master=title,text="Cyberpunk 2077 Breach Protocol Solver",bg="#16151b",fg="#d1ed5b",font=("Bebas",18))
title_label.pack(side="left",padx=20)

buffer = tk.Frame(master=window,height='150',bg='#16151b')
buffer.pack(fill=tk.X)
buffer.pack_propagate(False)
bufferbox = tk.LabelFrame(master=buffer,height=145,width=500,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
bufferbox.pack(expand=True,anchor='w',padx=20,side='left')
bufferbox.pack_propagate(False)
buffer_title_label = tk.Label(master=bufferbox,text="Specify Buffer Size",bg='#b3cc50',fg='#ffffff',font='Bebas',anchor='w')
buffer_title_label.pack(fill='x')
buffer_entry_text = tk.StringVar()
buffer_entry = Entry(master=bufferbox,textvariable=buffer_entry_text,justify='center')
buffer_entry_text.set(4)
buffer_entry.pack(pady=10)

button_border = tk.Frame(master=buffer,height=53,width=103,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
button_border.pack(expand=True,anchor='w',side='left')
button_border.pack_propagate(False)
solve_button = tk.Button(master=button_border,height=50,width=100,bg='#16151b',text='Solve',fg='#b3cc50',font='Bebas',activebackground='#606e0c',bd=0)
solve_button.pack(expand=True)

matrix = tk.Frame(master=window,bg='#16151b')
matrix.pack(fill='both',expand=True)
matrix.pack_propagate(False)
matrixbox = tk.LabelFrame(master=matrix,height=286,width=500,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
matrixbox.pack(expand=True,anchor='w',padx=20,side='left')
matrixbox.pack_propagate(False)
matrix_title = tk.Label(master=matrixbox,text="Enter Matrix Code",bg='#b3cc50',fg='#ffffff',font='Bebas',anchor='w')
matrix_title.pack(fill='x')
matrix_entry = tk.Text(master=matrixbox,width=454,height=280,bg='#16151b',bd=0,fg='#b3cc50',font='Bebas',insertbackground='#b3cc50')
matrix_entry.insert(END,"7A 55 E9 ...\n55 7A 1C ...\n...")
matrix_entry.pack(padx=10,pady=10)

sequencebox = tk.LabelFrame(master=matrix,height=286,width=500,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
sequencebox.pack(expand=True,anchor='w',padx=20,side='left')
sequencebox.pack_propagate(False)
sequence_title = tk.Label(master=sequencebox,text="Enter Sequences",bg='#b3cc50',fg='#ffffff',font='Bebas',anchor='w')
sequence_title.pack(fill='x')
sequence_entry = tk.Text(master=sequencebox,width=454,height=280,bg='#16151b',bd=0,fg='#b3cc50',font='Bebas',insertbackground='#b3cc50')
sequence_entry.insert(END,"BD 55 7A\n...")
sequence_entry.pack(padx=10,pady=10)

window.mainloop()