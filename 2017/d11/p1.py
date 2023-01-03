DIRS = {'n': -1j, 's': 1j, 'ne': -1j + 1, 'nw': -1, 'sw': 1j - 1, 'se': +1}

path = open("input").read().split(',')
p, max_d = 0, 0
for d in path:
    p += DIRS[d]
    max_d = max(max_d, max(p.real, p.imag))
print(max(p.real, p.imag))
print(max_d)
