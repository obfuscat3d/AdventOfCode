import re

DIR_VALS = {1: 0, 1j: 1, -1: 2, -1j: 3}
SIZE = 4


def parse():
    grid_text, path = open("input").read().split('\n\n')

    grid = {}
    for y, line in enumerate(grid_text.split('\n')):
        for x, char in enumerate(line):
            if char != ' ':
                grid[x + 1j * y] = char

    return [grid, path]


def teleport_1(pos, dp):
    pos -= dp
    while pos in grid:
        pos -= dp
    return pos + dp, dp


def teleport_2(pos, dp):
    if pos.imag == -1 and 0 <= pos.real <= 2 * SIZE:
        return [1j * (SIZE * 2 + pos.real), 1]
    elif pos.real == -1 and 3 * SIZE <= pos.imag < 4 * SIZE:
        return [pos.imag - 2 * SIZE, 1j]
    elif pos.real == SIZE - 1 and 0 <= pos.imag < SIZE:
        return [1j * (3 * SIZE - pos.imag - 1), 1]
    elif pos.real == - 1 and 2 * SIZE <= pos.imag < 3 * SIZE:
        return [SIZE + 1j * (3 * SIZE - pos.imag - 1), 1]
    elif 2 * SIZE <= pos.real < 3 * SIZE and pos.imag == -1:
        return [pos.real - 2 * SIZE + 1j * (4 * SIZE - 1), -1j]
    elif pos.imag == SIZE * 4:
        return [2 * SIZE + pos.real, 1j]
    elif pos.real >= 3 * SIZE:
        return [2 * SIZE - 1 + 1j * (3 * SIZE - 1 - pos.imag), -1]
    elif pos.real == 100 and 2 * SIZE <= pos.imag < 3 * SIZE:
        return [3 * SIZE - 1 + 1j * (3 * SIZE - pos.imag - 1), -1]
    elif 2 * SIZE <= pos.real < 3 * SIZE and pos.imag == SIZE and dp == 1j:
        return [(2 * SIZE - 1) + 1j * (pos.real - SIZE), -1]
    elif pos.real == 100 and SIZE <= pos.imag < 2 * SIZE and dp == 1:
        return [SIZE + pos.imag + 1j * (SIZE - 1), -1j]
    elif SIZE <= pos.real < 2 * SIZE and pos.imag == 3 * SIZE and dp == 1j:
        return [SIZE - 1 + 1j * (2 * SIZE + pos.real), -1]
    elif pos.real == SIZE and 3 * SIZE <= pos.imag < 4 * SIZE and dp == 1:
        return [pos.imag - 2 * SIZE + 1j * (3 * SIZE - 1), -1j]
    elif pos.real == SIZE - 1 and SIZE <= pos.imag <= 2 * SIZE and dp == -1:
        return [pos.imag - SIZE + 1j * 2 * SIZE, 1j]
    elif 0 <= pos.real < SIZE and pos.imag == 2 * SIZE - 1 and dp == -1j:
        return [SIZE + 1j * (SIZE + pos.real), 1]
    assert False


def move(teleport_fn, grid, pos, dp, n):
    for _ in range(n):
        if grid.get(pos + dp, ' ') == '.':
            pos += dp
        elif grid.get(pos + dp, ' ') == '#':
            return pos, dp
        else:
            temp_pos, temp_dp = teleport_fn(pos + dp, dp)
            if grid[temp_pos] == '#':
                return pos, dp
            else:
                pos, dp = temp_pos, temp_dp
    return pos, dp


def run(teleport_fn, grid, pos, dp, path):
    state = (pos, dp, path)
    while state[2]:
        if state[2][0] in ['R', 'L']:
            dp = dp * (-1j) if state[2][0] == 'L' else dp * (1j)
            state = (state[0], dp, state[2][1:])
        else:
            cur = re.findall("\d+", state[2])[0]
            pos, dp = move(teleport_fn, grid, state[0], state[1], int(cur))
            state = (pos, dp, state[2][len(cur):])
    return [state[0], state[1]]


grid, path = parse()
final_pos, dp = run(teleport_1, grid, SIZE, 1, path)
print(1000 * (1 + final_pos.imag) + 4 * (1 + final_pos.real) + DIR_VALS[dp])
final_pos, dp = run(teleport_2, grid, SIZE, 1, path)
print(1000 * (1 + final_pos.imag) + 4 * (1 + final_pos.real) + DIR_VALS[dp])
