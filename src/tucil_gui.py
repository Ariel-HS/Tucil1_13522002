import os.path
import time
import random
import tkinter as tk
from tkinter import * 
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile

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
                    elif (new_reward[0] == max_reward) and (len(new_reward[1])<len(max_buffer)):
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
                    elif (new_reward[0] == max_reward) and (len(new_reward[1])<len(max_buffer)):
                        max_buffer = new_reward[1]
                        max_coor = new_reward[2]
                        
        return (max_reward,max_buffer,max_coor)

    start = round(time.time()*1000)
    max = horizontal(buffer_size,0,0,[],[])
    end = round(time.time()*1000)
    duration = end-start

    popup = Toplevel(master=window,bg="#16151b")
    popup.geometry("450x440")
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
    time_frame = tk.Frame(master=popup,height='50',width=450,bg="#16151b")
    time_frame.pack(side='top')
    time_frame.pack_propagate(False)
    time_text = tk.Text(master=time_frame,bd=0,bg="#16151b",fg='#b3cc50')
    time_text.pack(padx=10,pady=10,side='left')
    time_text.insert(END, f"time: {duration} ms")
    time_text.config(state='disabled')

    def save():
        file = asksaveasfile(mode='w',defaultextension=".txt")
        if not file is None:
            file.write(str(max[0])+'\n')
            for tokens in max[1]:
                file.write(tokens+" ")
            file.write('\n')
            for coors in max[2]:
                file.write(coors+'\n')
        file.close()

    save_button = tk.Button(master=popup,text="Save as File",command=save)
    save_button.pack(padx=10,side='top',anchor='w')

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

def openRandomize():

    def randomize():
        token_amount = int(token_num_entry.get().rstrip())
        tokens = token_entry.get().rstrip().split()
        tokens = [tokens[i] for i in range(token_amount)]
        buffer_size = int(buffer_size_entry.get().rstrip())
        dimension = matrix_size_entry.get().rstrip().split()
        width = int(dimension[0])
        height = int(dimension[1])
        sequences_amount = int(sequence_num_entry.get().rstrip())
        max_sequence_length = int(sequence_max_entry.get().rstrip())
        matrix = [[random.choice(tokens) for i in range(width)] for j in range(height)]
        sequences = [[random.choice(tokens) for i in range(random.randint(1,max_sequence_length))] for j in range(sequences_amount)]
        sequences_reward = [random.randint(1,50) for i in range(sequences_amount)]

        buffer_entry.delete(0,END)
        matrix_entry.delete('1.0',END)
        sequence_entry.delete('1.0',END)
        reward_entry.delete('1.0',END)

        buffer_entry.insert(END,buffer_size)

        for line in matrix:
            for element in line:
                matrix_entry.insert(END,f"{element} ")
            matrix_entry.insert(END,"\n")

        for line in sequences:
            for element in line:
                sequence_entry.insert(END,f"{element} ")
            sequence_entry.insert(END,"\n")
        
        for element in sequences_reward:
            reward_entry.insert(END,f"{element}\n")

        popup.destroy()

    popup = Toplevel(master=window,bg="#16151b")
    popup.geometry("400x400")
    popup.title("Randomize")
    popup.resizable(False,False)

    token_num = tk.Label(master=popup,text='Jumlah Token Unik: ')
    token_num.pack(padx=5,pady=(5,0))
    token_num_entry = tk.Entry(master=popup)
    token_num_entry.pack(padx=5,pady=(2,5))
    token = tk.Label(master=popup,text='Tokens: ')
    token.pack(padx=5,pady=(5,0))
    token_entry = tk.Entry(master=popup)
    token_entry.insert(END,"BD 1C 7A 55 E9")
    token_entry.pack(padx=5,pady=(2,5))
    buffer_size_label = tk.Label(master=popup,text='Ukuran Buffer: ')
    buffer_size_label.pack(padx=5,pady=(5,0))
    buffer_size_entry = tk.Entry(master=popup)
    buffer_size_entry.pack(padx=5,pady=(2,5))
    matrix_size = tk.Label(master=popup,text='Ukuran Matriks (width x height): ')
    matrix_size.pack(padx=5,pady=(5,0))
    matrix_size_entry = tk.Entry(master=popup)
    matrix_size_entry.insert(END,"6 6")
    matrix_size_entry.pack(padx=5,pady=(2,5))
    sequence_num = tk.Label(master=popup,text='Jumlah Sekuens: ')
    sequence_num.pack(padx=5,pady=(5,0))
    sequence_num_entry = tk.Entry(master=popup)
    sequence_num_entry.pack(padx=5,pady=(2,5))
    sequence_max = tk.Label(master=popup,text='Ukuran Maksimal Sekuens: ')
    sequence_max.pack(padx=5,pady=(5,0))
    sequence_max_entry = tk.Entry(master=popup)
    sequence_max_entry.pack(padx=5,pady=(2,5))

    randomize_button_border = tk.Frame(master=popup,height=33,width=73,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
    randomize_button_border.pack(pady=20)
    randomize_button_border.pack_propagate(False)
    randomize_button = tk.Button(master=randomize_button_border,command=randomize,bg='#16151b',text='Randomize',fg='#b3cc50',font='Bebas',activebackground='#606e0c',bd=0)
    randomize_button.pack(expand=True)
    randomize_button.pack_propagate(False)

title = tk.Frame(master=window,height='100',bg="#16151b")
title.pack(fill=tk.X)
title.pack_propagate(False)
title_label = tk.Label(master=title,text="Cyberpunk 2077 Breach Protocol Solver",bg="#16151b",fg="#d1ed5b",font=("Bebas",18))
title_label.pack(side="left",padx=20)

frame = tk.Frame(master=window,height='150',bg='#16151b')
frame.pack(fill=tk.X)
frame.pack_propagate(False)
buffer = tk.Frame(master=frame,height='150',width='540',bg='#16151b')
buffer.pack(side='left')
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

button_frame = tk.Frame(master=frame,height='150',width='484',bg='#16151b')
button_frame.pack()
button_frame.pack_propagate(False)
button_border = tk.Frame(master=button_frame,height=53,width=103,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
button_border.pack(side='left',padx=69.5)
button_border.pack_propagate(False)
solve_button = tk.Button(master=button_border,command=func,height=50,width=100,bg='#16151b',text='Solve',fg='#b3cc50',font='Bebas',activebackground='#606e0c',bd=0)
solve_button.pack(expand=True)
solve_button.pack_propagate(False)
button_border_2 = tk.Frame(master=button_frame,height=53,width=103,bg='#16151b',highlightbackground='#b3cc50',highlightcolor='#b3cc50',highlightthickness=3,bd=0)
button_border_2.pack(side='left',padx=69.5)
button_border_2.pack_propagate(False)
randomize_button = tk.Button(master=button_border_2,command=openRandomize,height=50,width=100,bg='#16151b',text='Randomize',fg='#b3cc50',font='Bebas',activebackground='#606e0c',bd=0)
randomize_button.pack(expand=True)
randomize_button.pack_propagate(False)

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

upload_button = tk.Button(master=title,text="Import from File",command=upload)
upload_button.pack(side="left",padx=20)

window.mainloop()