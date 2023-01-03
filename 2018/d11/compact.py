import itertools

sat = {(0, y): 0 for y in range(0, 301)}
sat.update({(x, 0): 0 for x in range(0, 301)})
for x, y in itertools.product(range(1, 301), range(1, 301)):
    sat[(x, y)] = (((((x + 10) * y + 3999) * (x + 10) // 100) % 10) - 5 +
                   sat[(x - 1, y)] +
                   sat[(x, y - 1)] -
                   sat[(x - 1, y - 1)])

best_3, best_3_coord, best, best_coord = 0, None, 0, None
for s in range(1, 300):
    for x, y in itertools.product(range(1, 300 - s), range(1, 300 - s)):
        score = sat[(x - 1, y - 1)] + sat[(x + s - 1, y + s - 1)]
        score -= sat[(x - 1, y + s - 1)] + sat[x + s - 1, y - 1]
        if score > best:
            best, best_coord = score, (x, y, s)
        if score > best_3 and s == 3:
            best_3, best_3_coord = score, (x, y)
print(best_3, best_3_coord)
print(best, best_coord)
