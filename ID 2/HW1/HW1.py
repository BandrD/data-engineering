import numpy as np
import json

matrix = np.load('matrix_27.npy')

# print(matrix)

size = len(matrix)

matrix_stat = dict()
matrix_stat['sum'] = 0
matrix_stat['avr'] = 0
matrix_stat['sumMD'] = 0
matrix_stat['avrMD'] = 0
matrix_stat['sumSD'] = 0
matrix_stat['avrSD'] = 0
matrix_stat['max'] = matrix[0][0]
matrix_stat['min'] = matrix[0][0]

for i in range(0, size):
    for j in range(0, size):
        matrix_stat['sum'] += (matrix[i][j])
        if i == j:
            matrix_stat['sumMD'] += (matrix[i][j])
        if i + j == size:
            matrix_stat['sumMD'] += matrix[i][j]
        matrix_stat ['max'] = max(matrix_stat['max'], matrix[i][j])
        matrix_stat['min'] = max(matrix_stat['min'], matrix[i][j])

matrix_stat['avr'] = matrix_stat['sum'] / (size*size)
matrix_stat['avrMD'] = matrix_stat['sumMD'] / size
matrix_stat['avrSD'] = matrix_stat['sumSD'] / size

# print(matrix_stat)

for key in matrix_stat.keys():
    matrix_stat[key] = float(matrix_stat[key])

with open("matrix_stat.json", 'w') as result:
    result.write(json.dumps(matrix_stat))

norm_matrix = np.ndarray((size,size), dtype=float)

for i in range(0, size):
    for j in range(0, size):
        norm_matrix[i][j] = matrix[i][j] / matrix_stat['sum']

print(norm_matrix)

np.save('norm_matrix', norm_matrix)
