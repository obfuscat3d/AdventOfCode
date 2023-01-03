import re


def argmax(l):
    return -max((x, -i) for i, x in enumerate(l))[1]


data = list(map(int, re.findall("\d+", open("input").read())))

seen = set()
while tuple(data) not in seen:
    seen.add(tuple(data))
    i = argmax(data)
    val, data[i], i = data[i], 0, (i + 1) % len(data)
    while val:
        data[i], i, val = data[i] + 1, (i + 1) % len(data), val - 1
print(len(seen))

# Run it again with the current data to get the cycle length
seen = set()
while tuple(data) not in seen:
    seen.add(tuple(data))
    i = argmax(data)
    val, data[i], i = data[i], 0, (i + 1) % len(data)
    while val:
        data[i], i, val = data[i] + 1, (i + 1) % len(data), val - 1

print(len(seen))
