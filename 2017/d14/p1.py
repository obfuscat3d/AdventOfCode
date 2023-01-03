from itertools import *
from functools import *
from collections import deque


def chunk(l, n):
    cs = len(l) // n
    return [l[cs * i:cs * i + cs] for i in range(n)]


def knot_round(R, pos, skip_size, lengths):
    S = len(R)
    for flip_len in lengths:
        a, b = pos, pos + flip_len - 1
        while a < b:
            R[a % S], R[b % S], a, b = R[b % S], R[a % S], a + 1, b - 1
        pos, skip_size = (pos + skip_size + flip_len) % S, skip_size + 1
    return R, pos, skip_size


def knot_hash(key):
    lengths = list(map(ord, key)) + [17, 31, 73, 47, 23]
    R, pos, skip_size = list(range(256)), 0, 0
    for _ in range(64):
        R, pos, skip_size = knot_round(R, pos, skip_size, lengths)
    chunks = map(lambda x: reduce(lambda a, b: a ^ b, x, 0), chunk(R, 16))
    hex_vals = map(lambda x: "{:02x}".format(x), chunks)
    return ''.join(hex_vals)


INPUT = "stpzcrnm"
unseen = set()
for y in range(128):
    bin_data = "{:0128b}".format(int(knot_hash(f"{INPUT}-{y}"), 16))
    unseen.update({(x, y) for x in range(128) if bin_data[x] == '1'})
print(len(unseen))

regions = 0
while unseen:
    q = deque([unseen.pop()])
    while q:
        x, y = q.popleft()
        for x1, y1 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (x1, y1) in unseen:
                unseen.discard((x1, y1))
                q.append((x1, y1))
    regions += 1
print(regions)
