from itertools import *
from pprint import pprint
from copy import deepcopy


def visible_neighbors(matrix, x, y):
    c = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            i, j, done = x+dx, y+dy, False
            while (not done and
                   i >= 0 and i < len(matrix) and
                   j >= 0 and j < len(matrix[0]) and
                   (i != x or j != y)):
                if matrix[i][j] == '#':
                    c += 1
                    done = True
                elif matrix[i][j] == 'L':
                    done = True
                i, j = i+dx, j+dy

    return c


def neighbors(m, x, y):
    return [(x+i, y+j) for i in [-1, 0, 1] for j in [-1, 0, 1]
            if x+i >= 0 and x+i < len(m) and y+j >= 0 and y+j < len(m[0]) and (i or j)]


def step(matrix):
    changed = False
    next_step = deepcopy(matrix)
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] == 'L':  # Vacio
                if visible_neighbors(matrix, x, y) == 0:
                    next_step[x][y] = '#'
                    changed = True
            elif matrix[x][y] == '#':  # Ocupado
                if visible_neighbors(matrix, x, y) >= 5:
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
