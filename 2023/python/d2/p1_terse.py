import re, math, collections

s1, s2, CA = 0, 0, {"r": 12, "g": 13, "b": 14}
for l in open("input").read().split("\n"):
    v, mc = True, collections.defaultdict(int)
    for c, a in CA.items():
        v &= not any(int(m.split()[0]) > a for m in re.findall(f"\\d+ {c}", l))
        mc[c] = max(mc[c], *(int(m.split()[0]) for m in re.findall(f"\\d+ {c}", l)))
    s1, s2 = s1 + (int(l.split(" ")[1][:-1]) if v else 0), s2 + math.prod(mc.values())
print(s1, s2)
