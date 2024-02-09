
# dummy test
buffer_size = 7
width = 6
height = 6
matrix = [
    ['7A','55','E9','E9','1C','55'],
    ['55','7A','1C','7A','E9','55'],
    ['55','1C','1C','55','E9','BD'],
    ['BD','1C','7A','1C','55','BD'],
    ['BD','55','BD','7A','1C','1C'],
    ['1C','55','55','7A','55','7A'],
]
'''
[
    ['7A','55','E9'],
    ['1C','6D','8F'],
    ['2S','3X','4H']
]
'''

sequences_amount = 3
sequences = [
    ['BD','E9','1C'],
    ['BD','7A','BD'],
    ['BD','1C','BD','55']
]
'''
[
    ['55','6D'],
    ['E9','8F','1C','7A'],
    ['7A','2S','4H']
]
'''

sequences_reward = [
    15,
    20,
    30
]

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

def func():
    max = horizontal(0,0,[],[])
    for output in max:
        print(output)

print('test')
func()