from itertools import *
from pprint import pprint
from copy import deepcopy


def neighbors(m, x, y):
    return [(x+i, y+j) for i in [-1, 0, 1] for j in [-1, 0, 1]
            if x+i >= 0 and x+i < len(m) and y+j >= 0 and y+j < len(m[0]) and (i or j)]


def step(matrix):
    changed = False
    next_step = deepcopy(matrix)
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] == 'L':  # Vacio
                if not [1 for (i, j) in neighbors(matrix, x, y) if matrix[i][j] == '#']:
                    next_step[x][y] = '#'
                    changed = True
            elif matrix[x][y] == '#':  # Ocupado
                if len([1 for (i, j) in neighbors(matrix, x, y) if matrix[i][j] == '#']) >= 4:
                    next_step[x][y] = 'L'
                    changed = True
    return (next_step, changed)


with open('2020/d11/input') as input:
    matrix = [[i for i in j] for j in input.read().splitlines()]

changed = True
while changed:
    matrix, changed = step(matrix)
print(len([1 for x in range(len(matrix))
      for y in range(len(matrix[0])) if matrix[x][y] == '#']))
