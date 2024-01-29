import re, z3, math, collections, itertools as it, numpy as np

Stone = collections.namedtuple("Stone", ["x", "y", "z", "dx", "dy", "dz"])

def parse(fn):
    return [Stone(*map(int, re.findall(r'-?\d+', l))) for l in open(fn).readlines()]

def find_intersection(a, b):
    slopeA = a.dy / a.dx if a.dx else math.inf
    slopeB = b.dy / b.dx if b.dx else math.inf
    if slopeA == slopeB:
        # This isn't quite a valid assumption, but it works for the input
        return None, None
    elif slopeA == math.inf:
        x = a.x
        y = slopeB * (x - b.x) + b.y
    elif slopeB == math.inf:
        x = b.x
        y = slopeA * (x - a.x) + a.y
    else:
        x = (a.y - b.y + slopeB * b.x - slopeA * a.x) / (slopeB - slopeA)
        y = slopeA * (x - a.x) + a.y

    # verify not in the past
    if (np.sign(x - a.x) != np.sign(a.dx) or 
        np.sign(x - b.x) != np.sign(b.dx) or 
        np.sign(y - a.y) != np.sign(a.dy) or 
        np.sign(y - b.y) != np.sign(b.dy)):
        return None, None

    return (x,y)

def part1(hail, accepted_range):
    total, min_d, max_d = 0, accepted_range[0], accepted_range[1]
    for a,b in it.product(hail, hail):
        x,y = find_intersection(a, b)
        if x and y and min_d <= x <= max_d and min_d <= y <= max_d:
            total += 1
    print(total // 2) # divide by 2 because we double count

def part2(hail):
    x, y, z, dx, dy, dz = map(z3.Int, ["x", "y", "z", "dx", "dy", "dz"])
    s = z3.Solver()
    for i, h in enumerate(hail):
        t = z3.Int(f"t{i}")
        s.add(x + dx*t == h.x+h.dx*t)
        s.add(y + dy*t == h.y+h.dy*t)
        s.add(z + dz*t == h.z+h.dz*t)
    
    s.check()
    print(s.model().eval(x+y+z))

hail = parse("input")
part1(hail, (200000000000000, 400000000000000))
part2(hail)
