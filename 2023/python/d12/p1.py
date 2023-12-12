from functools import lru_cache


def parse(filename):
    data = []
    for l in open(filename).readlines():
        a, b = l.split(" ")
        data.append((a, tuple(map(int, b.split(",")))))
    return data


@lru_cache(maxsize=None)
def arr_cnt(m, s, n):
    # m = measurement ("#?.#"), s = survey (1,2,3), n = is next spot lava
    tr = lambda t: (t[0] - 1,) + t[1:]  # lru_cache demands tuples
    if not s:
        return 0 if "#" in m else 1
    elif not m:
        return 0 if sum(s) else 1
    elif s[0] == 0:
        return arr_cnt(m[1:], s[1:], False) if m[0] in ["?", "."] else 0
    elif n:
        return arr_cnt(m[1:], tr(s), True) if m[0] in ["?", "#"] else 0
    elif m[0] == "#":
        return arr_cnt(m[1:], tr(s), True)
    elif m[0] == ".":
        return arr_cnt(m[1:], s, False)
    else:
        return arr_cnt(m[1:], s, False) + arr_cnt(m[1:], tr(s), True)


data = parse("input")
print(sum(arr_cnt(m, s, False) for m, s in data))
data2 = [(((m + "?") * 5)[:-1], s * 5) for m, s in data]
print(sum(arr_cnt(m, s, False) for m, s in data2))
