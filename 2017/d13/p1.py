import re


ranges = {}
for l in open("input").read().split('\n'):
    d, r = re.findall("\d+", l)
    ranges[int(d)] = int(r)

print(sum(r * d for r, d in ranges.items() if r % (2 * (d - 1)) == 0))
delay = 0
while any((delay + r) % (2 * (d - 1)) == 0 for r, d in ranges.items()):
    delay += 1
print(delay)
