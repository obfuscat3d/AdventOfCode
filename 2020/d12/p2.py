with open('2020/d12/input') as input:
    instructions = [(s[0], int(s[1:])) for s in input.read().splitlines()]

shipX, shipY, waypointX, waypointY = 0, 0, 10, -1
for (i, j) in instructions:
    print(shipX, shipY, waypointX, waypointY)
    if i == 'E':
        waypointX += j
    if i == 'W':
        waypointX -= j
    if i == 'N':
        waypointY -= j
    if i == 'S':
        waypointY += j
    if i == 'F':
        shipX, shipY = (shipX + waypointX * j), (shipY + waypointY * j)
    if i == 'L':
        for q in range(j//90):
            waypointY, waypointX = -waypointX, waypointY
    if i == 'R':
        for q in range(j//90):
            waypointY, waypointX = waypointX, -waypointY

print(abs(shipX)+abs(shipY))
