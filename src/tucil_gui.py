import os.path
import time
import random
import tkinter as tk
from tkinter import * 

def func():
    buffer_size = int(buffer_entry.get())
    matrix = matrix_entry.get('1.0','end-1c').split("\n")
    matrix = [line.split() for line in matrix]
    height = len(matrix)
    width = len(matrix[0])
    sequences = sequence_entry.get('1.0','end-1c').split("\n")
    sequences = [line.split() for line in sequences]
    sequences_amount = len(sequences)
    sequences_reward = [1 for i in range(sequences_amount)]

    matrix_2 = [[1 for i in range(width)] for j in range(height)]

    def checkReward(buffer):
        reward = 0
        for i in range(sequences_amount):
            # print(buffer)
            # print(sequences[i])
            has_reward = False
            j = 0
            while not has_reward and j < (len(buffer)-len(sequences[i])+1):
                is_reward = True
                k = 0
                while is_reward and k < len(sequences[i]): 
                    if (buffer[j+k] != sequences[i][k]):
                        is_reward = False
                    k += 1
                if is_reward:
                    reward += sequences_reward[i]
                    has_reward = True
                j += 1

        return reward

    def horizontal(buffer_size,row,ctr,buffer,coor_buffer):
        # print(buffer,coor_buffer)
        max_reward = checkReward(buffer)
        max_buffer = buffer
        max_coor = coor_buffer
        if (ctr < buffer_size):

            for i in range (width):
                if (matrix_2[row][i] != 0):
                    matrix_2[row][i] = 0
                    buffer.append(matrix[row][i])
                    coor_buffer.append(str(i+1)+','+str(row+1))
                    new_buffer = buffer.copy()
                    new_coor_buffer = coor_buffer.copy()
                    new_reward = vertical(buffer_size,i,ctr+1,new_buffer,new_coor_buffer)
                    buffer.pop()
                    coor_buffer.pop()
                    matrix_2[row][i] = 1

                    if new_reward[0] > max_reward:
                        max_reward = new_reward[0]
                        max_buffer = new_reward[1]
                        max_coor = new_reward[2]
        
        return (max_reward,max_buffer,max_coor)

    def vertical(buffer_size,column,ctr,buffer,coor_buffer):
        # print(buffer,coor_buffer)
        max_reward = checkReward(buffer)
        max_buffer = buffer
        max_coor = coor_buffer
        if (ctr < buffer_size):

            for i in range(height):
                if (matrix_2[i][column] != 0):
                    matrix_2[i][column] = 0
                    buffer.append(matrix[i][column])
                    coor_buffer.append(str(column+1)+','+str(i+1))
                    new_buffer = buffer.copy()
                    new_coor_buffer = coor_buffer.copy()
                    new_reward = horizontal(buffer_size,i,ctr+1,new_buffer,new_coor_buffer)
                    buffer.pop()
                    coor_buffer.pop()
                    matrix_2[i][column] = 1

                    if new_reward[0] > max_reward:
                        max_reward = new_reward[0]
                        max_buffer = new_reward[1]
                        max_coor = new_reward[2]

        return (max_reward,max_buffer,max_coor)

    print(buffer_size)
    print(matrix)
    print(sequences)

    start = round(time.time()*1000)
    max = horizontal(buffer_size,0,0,[],[])
    print(max[0])
    for tokens in max[1]:
        print(tokens,end=" ")
    print()
    for coors in max[2]:
        print(coors)
    end = round(time.time()*1000)
    print(f"\n{end-start} ms\n")
    
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
solve_button = tk.Button(master=button_border,command=func,height=50,width=100,bg='#16151b',text='Solve',fg='#b3cc50',font='Bebas',activebackground='#606e0c',bd=0)
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