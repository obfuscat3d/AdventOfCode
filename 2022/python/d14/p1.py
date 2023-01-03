import re
import collections
import numpy as np

test = open('input').read()
max_y = 0
grid = set()

for l in test.split('\n'):
    m = re.findall("\d+,\d+", l)
    cur = m.pop(0)
    cur = int(cur.split(',')[0]) + 1j * int(cur.split(',')[1])
    while m:
        dest = m.pop(0)
        dest = int(dest.split(',')[0]) + 1j * int(dest.split(',')[1])
        while dest != cur:
            max_y = max(max_y, cur.imag)
            grid.add(cur)
            cur += np.sign((dest - cur).real) + 1j * np.sign((dest - cur).imag)
        grid.add(cur)
        max_y = max(max_y, cur.imag)
        cur = dest

grid2 = grid.copy()

kernels = 0
sand = 500
while sand.imag < 50000:
    if not sand + 1j in grid:
        sand += 1j
    elif sand - 1 + 1j not in grid:
        sand += (-1 + 1j)
    elif sand + 1 + 1j not in grid:
        sand += 1 + 1j
    else:
        grid.add(sand)
        sand = 500
        kernels += 1

print(kernels)

kernels = 0
sand = 500
while not 500 in grid2:
    if sand.imag == max_y + 1:
        grid2.add(sand)
        sand = 500
        kernels += 1
    elif not sand + 1j in grid2:
        sand += 1j
    elif sand - 1 + 1j not in grid2:
        sand += (-1 + 1j)
    elif sand + 1 + 1j not in grid2:
        sand += 1 + 1j
    else:
        grid2.add(sand)
        sand = 500
        kernels += 1

print(kernels)
