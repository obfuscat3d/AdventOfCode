import re, math


def parse(text):
    times = [int(n) for n in re.findall(r"\d+", text[0])]
    record_distances = [int(n) for n in re.findall(r"\d+", text[1])]
    return times, record_distances


def brute_force(times, record_distances):
    winnings_combos = 1
    for t, d in zip(times, record_distances):
        winnings_combos *= sum(1 for c in range(1, t) if c * (t - c) > d)
    return winnings_combos


def quadratic(times, record_distances):
    winnings_combos = 1
    for t, d in zip(times, record_distances):
        high = (t + math.sqrt(t**2 - 4 * d)) / 2
        low = (t - math.sqrt(t**2 - 4 * d)) / 2
        high = math.floor(high) - (1 if int(high) == high else 0)
        low = math.ceil(low) + (1 if int(low) == low else 0)
        winnings_combos *= high - low + 1
    return winnings_combos


print(brute_force(*parse(open("input2").read().split("\n"))))
print(quadratic(*parse(open("input2").read().split("\n"))))
print(brute_force(*parse(open("input").read().replace(" ", "").split("\n"))))
print(quadratic(*parse(open("input").read().replace(" ", "").split("\n"))))
