

def neighbors(cube):
    return [(cube[0]+i, cube[1]+j, cube[2]+k, cube[3]+l)
            for i in [-1, 0, 1]
            for j in [-1, 0, 1]
            for k in [-1, 0, 1]
            for l in [-1, 0, 1]]


def parse_input(input):
    matrix = {}
    for x, line in enumerate(input.split('\n')):
        for y, px in enumerate(line):
            matrix[(x, y, 0, 0)] = px == '#'
    return matrix, (0, 0, 0, 0, len(input.split('\n'))-1, len(input.split('\n')[0])-1, 0, 0)


def next_for_cube(matrix, cube):
    n = 0
    for c in neighbors(cube):
        if c in matrix:
            n += matrix[c]
    if cube in matrix and matrix[cube]:
        return n == 3 or n == 4
    else:
        return n == 3


def step(matrix, bounds):
    minX, minY, minZ, minW, maxX, maxY, maxZ, maxW = bounds
    next_matrix = {}
    for x in range(minX-1, maxX+2):
        for y in range(minY-1, maxY+2):
            for z in range(minZ-1, maxZ+2):
                for w in range(minW-1, maxW+2):
                    next_matrix[(x, y, z, w)] = next_for_cube(
                        matrix, (x, y, z, w))
    return next_matrix, (minX-1, minY-1, minZ-1, minW-1, maxX+1, maxY+1, maxZ+1, maxW+1)


def run(matrix, bounds, iterations):
    for x in range(iterations):
        matrix, bounds = step(matrix, bounds)
    return matrix


with open('2020/d17/input') as input:
    matrix, bounds = parse_input(input.read())


final = run(matrix, bounds, 6)
print(len([v for v in final.values() if v]))
