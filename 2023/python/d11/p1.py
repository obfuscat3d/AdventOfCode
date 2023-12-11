import itertools as it


def parse(filename):
    lines = open(filename).readlines()
    stars = {(x, y) for y, l in enumerate(lines) for x, c in enumerate(l) if c == "#"}
    stars_x, stars_y = {x for x, _ in stars}, {y for _, y in stars}
    return stars, stars_x, stars_y


def md(p1, p2, s_x, s_y, expansion_factor):
    cr = lambda a, b: range(a, b) if a < b else range(b, a)
    return (
        abs(p1[0] - p2[0])
        + abs(p1[1] - p2[1])
        + sum([expansion_factor - 1 for x in cr(p1[0], p2[0]) if x not in s_x])
        + sum([expansion_factor - 1 for y in cr(p1[1], p2[1]) if y not in s_y])
    )


def distance_sum(stars, s_x, s_y, factor):
    return sum(md(a, b, s_x, s_y, factor) for a, b in it.combinations(stars, 2))


stars, stars_x, stars_y = parse("input")
print(distance_sum(stars, stars_x, stars_y, 2))
print(distance_sum(stars, stars_x, stars_y, 1_000_000))
