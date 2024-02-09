import os.path
import time
import random

input_type = input("Apakah ingin memasukkan input melalui file atau secara acak?(file/acak) ")
while input_type != 'file' and input_type != 'acak':
    print("Invalid input")
    input_type = input("Apakah ingin memasukkan input melalui file atau secara acak?(file/acak) ")

if input_type == 'file':
    file_name = input("Enter absolute path: ")
    while not os.path.isfile(file_name):
        print("File not found")
        file_name = input("Enter absolute path: ")

    file = open(file_name,'r')

    buffer_size = int(file.readline().rstrip())
    dimension = file.readline().rstrip().split()
    width = int(dimension[0])
    height = int(dimension[1])
    matrix = [file.readline().rstrip().split() for i in range(height)]
    sequences_amount = int(file.readline().rstrip())
    sequences = []
    sequences_reward = []
    for i in range(sequences_amount):
        sequences.append(file.readline().rstrip().split())
        sequences_reward.append(int(file.readline().rstrip()))

    file.close()

else:
    pass

matrix_2 = [[1 for i in range(width)] for i in range(height)]

def checkReward(buffer):
    reward = 0
    for i in range(sequences_amount):
        # print(buffer)
        # print(sequences[i])
        for j in range(len(buffer)-len(sequences[i])+1):
            is_reward = True
            k = 0
            while is_reward and k < len(sequences[i]): 
                if (buffer[j+k] != sequences[i][k]):
                    is_reward = False
                k += 1
            if is_reward:
                reward += sequences_reward[i]

    return reward

def horizontal(row,ctr,buffer,coor_buffer):
    global buffer_size
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
                new_reward = vertical(i,ctr+1,new_buffer,new_coor_buffer)
                buffer.pop()
                coor_buffer.pop()
                matrix_2[row][i] = 1

                if new_reward[0] > max_reward:
                    max_reward = new_reward[0]
                    max_buffer = new_reward[1]
                    max_coor = new_reward[2]
    
    return (max_reward,max_buffer,max_coor)

def vertical(column,ctr,buffer,coor_buffer):
    global buffer_size
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
                new_reward = horizontal(i,ctr+1,new_buffer,new_coor_buffer)
                buffer.pop()
                coor_buffer.pop()
                matrix_2[i][column] = 1

                if new_reward[0] > max_reward:
                    max_reward = new_reward[0]
                    max_buffer = new_reward[1]
                    max_coor = new_reward[2]

    return (max_reward,max_buffer,max_coor)

start = round(time.time()*1000)
max = horizontal(0,0,[],[])
print(max[0])
for tokens in max[1]:
    print(tokens,end=" ")
print()
for coors in max[2]:
    print(coors)
end = round(time.time()*1000)
print(f"\n{end-start} ms\n")

is_simpan = input("Apakah ingin menyimpan solusi?(y/n) ")

while (is_simpan != 'y' and is_simpan != 'n'):
    print("Invalid input")
    is_simpan = input("Apakah ingin menyimpan solusi?(y/n) ")

if is_simpan == 'y':
    file_output_name = input("Enter absolute path: ")

    file_output = open(file_output_name,'w')
    file_output.write(str(max[0])+'\n')
    for tokens in max[1]:
        file_output.write(tokens+" ")
    file_output.write('\n')
    for coors in max[2]:
        file_output.write(coors+'\n')

    file_output.close()