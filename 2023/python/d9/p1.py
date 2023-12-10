import re


def whos_next(l):
    if len(set(l)) == 1:
        return l[0]
    else:
        return l[-1] + whos_next([l[i + 1] - l[i] for i in range(len(l) - 1)])


data = [list(map(int, re.findall(r"-?\w+", l))) for l in open("input3").readlines()]
print(sum(whos_next(l) for l in data))
print(sum(whos_next(l[::-1]) for l in data))
