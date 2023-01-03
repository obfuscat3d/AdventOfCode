import re


sign = lambda x: -1 if x < 0 else 0 if x == 0 else 1
parse_complex = lambda s: int(s.split(',')[0]) + 1j * int(s.split(',')[1])

depth, beach = 0, set()
for line in open('input').read().split('\n'):
    coords = list(map(parse_complex, re.findall("\d+,\d+", line)))
    p0 = coords.pop(0)
    while coords:
        p1 = coords.pop(0)
        while p0 != p1:
            depth = max(depth, p0.imag)
            beach.add(p0)
            p0 += sign((p1 - p0).real) + 1j * sign((p1 - p0).imag)
        beach.add(p0)
        p0, depth = p1, max(depth, p1.imag)


part1, part2, sand = 0, 0, 500
while not 500 in beach:
    if sand.imag == depth + 1:
        beach.add(sand)
        sand, part1, part2 = 500, part1 if part1 else part2, part2 + 1
    elif not sand + 1j in beach:
        sand += 1j
    elif sand - 1 + 1j not in beach:
        sand += (-1 + 1j)
    elif sand + 1 + 1j not in beach:
        sand += 1 + 1j
    else:
        beach.add(sand)
        sand, part2 = 500, part2 + 1

print(part1)
print(part2)
