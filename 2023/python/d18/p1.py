MOVES = {"R": 1, "0": 1, "L": -1, "2": -1, "U": -1j, "3": -1j, "D": 1j, "1": 1j}


def shoelace(dn):
    wpts, cur, trench = [0], 0, 0
    for d, n in dn:
        cur, trench = cur + MOVES[d] * n, trench + n
        wpts.append(cur)

    det = lambda a, b: a.real * b.imag - b.real * a.imag
    A = sum(det(a, b) for a, b in zip(wpts, wpts[1:] + [wpts[0]]))
    return A / 2 + trench / 2 + 1


def integral(dn):
    cur, trench, area = 0, 0, 0
    for d, n in dn:
        cur, trench = cur + MOVES[d] * n, trench + n
        if MOVES[d] in [1, -1]:
            area -= n * (cur.imag) * MOVES[d]

    return area + trench / 2 + 1


plan = [l.split() for l in open("input").readlines()]
print(shoelace([(d, int(n)) for d, n, _ in plan]))
print(shoelace([(c[7], int(c[2:7], 16)) for _, _, c in plan]))
print(integral([(d, int(n)) for d, n, _ in plan]))
print(integral([(c[7], int(c[2:7], 16)) for _, _, c in plan]))
