with open('2020/d12/input') as input:
    instructions = [(s[0], int(s[1:])) for s in input.read().splitlines()]

x, y, dx, dy = 0, 0, 1, 0
for (i, j) in instructions:
    if i == 'E':
        x += j
    if i == 'W':
        x -= j
    if i == 'N':
        y -= j
    if i == 'S':
        y += j
    if i == 'F':
        x, y = (x + dx * j), (y + dy * j)
    if i == 'L':
        for q in range(j//90):
            dy, dx = -dx, dy
    if i == 'R':
        for q in range(j//90):
            dy, dx = dx, -dy

print(abs(x)+abs(y))
