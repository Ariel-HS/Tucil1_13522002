import os.path
import time
import random
import tkinter as tk
from tkinter import * 
from tkinter.filedialog import askopenfile

window = tk.Tk(className="python Cyberpunk 2077 Breach Protocol Solver")
window.geometry("1024x576")
window.configure(background="#16151b")
window.resizable(False,False)

def func():
    buffer_size = int(buffer_entry.get().rstrip())
    matrix = matrix_entry.get('1.0','end-1c').rstrip().split("\n")
    matrix = [line.split() for line in matrix]
    height = len(matrix)
    width = len(matrix[0])
    sequences = sequence_entry.get('1.0','end-1c').rstrip().split("\n")
    sequences = [line.split() for line in sequences]
    sequences_amount = len(sequences)
    sequences_reward = reward_entry.get('1.0','end-1c').rstrip().split("\n")
    sequences_reward = [int(amount) for amount in sequences_reward]

    # cek sequence unik (kalau tidak unik, reward = 0)
    for i in range(sequences_amount-1):
        for j in range(i+1,sequences_amount):
            if len(sequences[i]) == len(sequences[j]):
                is_same = True
                k = 0
                while is_same and k < len(sequences[i]):
                    if sequences[i][k] != sequences[j][k]:
                        is_same = False
                    k += 1
                if is_same:
                    sequences_reward[j] = 0

    matrix_2 = [[1 for i in range(width)] for j in range(height)]

    def checkReward(buffer):
        reward = 0
        for i in range(sequences_amount):
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

    start = round(time.time()*1000)
    max = horizontal(buffer_size,0,0,[],[])
    end = round(time.time()*1000)
    duration = end-start

    popup = Toplevel(master=window)
    popup.geometry("450x400")
    popup.title("Solution")
    popup.resizable(False,False)

    text_frame = tk.Frame(master=popup,height='100',bg="#16151b")
    text_frame.pack(fill='x',side='top')
    text_frame.pack_propagate(False)
    solution = tk.Text(master=text_frame,bd=0,bg="#16151b",fg='#b3cc50')
    solution.pack(fill='x',padx=10,pady=10)
    solution.insert(END, f"Reward: {max[0]}\nSequence: ")
    for tokens in max[1]:
        solution.insert(END, f"{tokens} ")
    solution.insert(END, "\nSteps: ")
    for coors in max[2]:
        solution.insert(END, f"{coors} ")
    solution.config(state='disabled')

    matrix_frame = tk.Frame(master=popup,height='250',bg="#16151b")
    matrix_frame.pack(fill='x',side='top')
    matrix_frame.pack_propagate(False)
    matrix_text = tk.Text(master=matrix_frame,bd=0,font=("Bebas",18),bg="#16151b",fg='#b3cc50')
    matrix_text.pack(fill='both',padx=10,pady=10,side='top',expand=True)
    matrix_text.tag_config('highlight',background='#606e0c')
    for i in range(height):
        for j in range(width):
            if (str(j+1)+','+str(i+1)) not in max[2]:
                matrix_text.insert(END, f"{matrix[i][j]} ")
            else:
                matrix_text.insert(END, matrix[i][j],'highlight')
                matrix_text.insert(END, ' ')
        matrix_text.insert(END,'\n')
    matrix_text.config(state='disabled')
    time_frame = tk.Frame(master=popup,height='50',bg="#16151b")
    time_frame.pack(fill='x',side='top')
    time_frame.pack_propagate(False)
    time_text = tk.Text(master=time_frame,bd=0,bg="#16151b",fg='#b3cc50')
    time_text.pack(fill='x',padx=10,pady=10,side='top')
    time_text.insert(END, f"time: {duration} ms")
    time_text.config(state='disabled')

def upload():
    file = askopenfile(mode='r')

    buffer_entry.delete(0,END)
    matrix_entry.delete('1.0',END)
    sequence_entry.delete('1.0',END)
    reward_entry.delete('1.0',END)

    buffer_entry.insert(END,file.readline().rstrip())
    dimension = file.readline().rstrip().split()
    for i in range(int(dimension[1])):
        matrix_entry.insert(END,file.readline())
    sequences_amount = int(file.readline().rstrip())
    for i in range(sequences_amount):
        sequence_entry.insert(END,file.readline())
        reward_entry.insert(END,file.readline())

    file.close()

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
solve_button.pack_propagate(False)

matrix = tk.Frame(master=window,bg='#16151b')
matrix.pack(fill='both',expand=True)
matrix.pack_propagate(False)
matrixbox = tk.LabelFrame(master=matrix,height=286,width=500,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
matrixbox.pack(expand=True,anchor='w',padx=(20,10),side='left')
matrixbox.pack_propagate(False)
matrix_title = tk.Label(master=matrixbox,text="Enter Matrix Code",bg='#b3cc50',fg='#ffffff',font='Bebas',anchor='w')
matrix_title.pack(fill='x')
matrix_entry = tk.Text(master=matrixbox,width=454,height=280,bg='#16151b',bd=0,fg='#b3cc50',font='Bebas',insertbackground='#b3cc50')
matrix_entry.insert(END,"7A 55 E9 ...\n55 7A 1C ...\n...")
matrix_entry.pack(padx=10,pady=10)

sequencebox = tk.LabelFrame(master=matrix,height=286,width=225,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
sequencebox.pack(expand=True,anchor='w',padx=10,side='left')
sequencebox.pack_propagate(False)
sequence_title = tk.Label(master=sequencebox,text="Enter Sequences",bg='#b3cc50',fg='#ffffff',font='Bebas',anchor='w')
sequence_title.pack(fill='x')
sequence_entry = tk.Text(master=sequencebox,width=454,height=280,bg='#16151b',bd=0,fg='#b3cc50',font='Bebas',insertbackground='#b3cc50')
sequence_entry.insert(END,"BD 55 7A\n...")
sequence_entry.pack(padx=10,pady=10)

rewardbox = tk.LabelFrame(master=matrix,height=286,width=225,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
rewardbox.pack(expand=True,anchor='w',padx=(10,20),side='left')
rewardbox.pack_propagate(False)
reward_title = tk.Label(master=rewardbox,text="Enter Reward",bg='#b3cc50',fg='#ffffff',font='Bebas',anchor='w')
reward_title.pack(fill='x')
reward_title.pack_propagate(False)
reward_entry = tk.Text(master=rewardbox,width=454,height=280,bg='#16151b',bd=0,fg='#b3cc50',font='Bebas',insertbackground='#b3cc50')
reward_entry.insert(END,"15\n...")
reward_entry.pack(padx=10,pady=10)
reward_entry.pack_propagate(False)

upload_button = tk.Button(master=title,text="Upload File",command=upload)
upload_button.pack(side="left",padx=20)

window.mainloop()