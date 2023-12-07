import re


def parse(text):
    times = [int(n) for n in re.findall(r"\d+", text[0])]
    record_distances = [int(n) for n in re.findall(r"\d+", text[1])]
    return times, record_distances


def go(times, record_distances):
    winnings_combos = 1
    for t, d in zip(times, record_distances):
        winnings_combos *= sum(1 for c in range(1, t) if c * (t - c) > d)
    return winnings_combos


print(go(*parse(open("input").read().split("\n"))))
print(go(*parse(open("input").read().replace(" ", "").split("\n"))))
