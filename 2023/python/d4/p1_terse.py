import re


cm = lambda s: len(re.findall(r"\d+", s.split(":")[1])) - len(
    set(re.findall(r"\d+", s.split(":")[1]))
)
cards = open("input").read().split("\n")
card_counts, score = [1] * len(cards), 0
for i, m in enumerate([cm(c) for c in cards]):
    score += int(2 ** (m - 1))
    for j in range(i + 1, m + i + 1):
        card_counts[j] += card_counts[i]
print(score, sum(card_counts))
