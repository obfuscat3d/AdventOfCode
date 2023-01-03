def calc_power_level(x, y, gsn):
    return ((((x + 10) * y + gsn) * (x + 10) // 100) % 10) - 5


def gen_grid(gsn):
    sat = {(0, y): 0 for y in range(0, 301)}
    sat.update({(x, 0): 0 for x in range(0, 301)})
    for x in range(1, 301):
        for y in range(1, 301):
            sat[(x, y)] = (calc_power_level(x, y, gsn) +
                           sat[(x - 1, y)] +
                           sat[(x, y - 1)] -
                           sat[(x - 1, y - 1)])
    return sat


def part1(sat):
    best, best_coord, s = 0, None, 3
    for x in range(1, 300 - s):
        for y in range(1, 300 - s):
            score = sat[(x - 1, y - 1)] + sat[(x + s - 1, y + s - 1)]
            score -= sat[(x - 1, y + s - 1)] + sat[x + s - 1, y - 1]
            if score > best:
                best, best_coord = score, (x, y)
    print(best, best_coord)


def part2(sat):
    best, best_coord = 0, None
    for s in range(1, 300):
        for x in range(1, 300 - s):
            for y in range(1, 300 - s):
                score = sat[(x - 1, y - 1)] + sat[(x + s - 1, y + s - 1)]
                score -= sat[(x - 1, y + s - 1)] + sat[x + s - 1, y - 1]
                if score > best:
                    best, best_coord = score, (x, y, s)
    print(best, best_coord)


sat = gen_grid(3999)
part1(sat)
part2(sat)
