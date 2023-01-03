import re

text = open("input").read().split('\n')

s1 = [[] for _ in range(9)]
while not text[0].startswith(' 1'):
    for i in range(9):
        if text[0][1 + 4 * i] != ' ':
            s1[i].append(text[0][1 + 4 * i])
    text.pop(0)

text = text[2:]
s2 = [s.copy() for s in s1]

for c, f, t in [map(int, re.findall('\d+', l)) for l in text]:
    s1[t - 1], s1[f - 1] = s1[f - 1][:c][::-1] + s1[t - 1], s1[f - 1][c:]
    s2[t - 1], s2[f - 1] = s2[f - 1][:c] + s2[t - 1], s2[f - 1][c:]

print("".join(s[0] for s in s1))
print("".join(s[0] for s in s2))
