import re


def count_matches(s):
    # Split the string at ':' then use a regex to find all numbers in the second
    # half. Count the dupes.
    nums = re.findall(r"\d+", s.split(":")[1])
    return len(nums) - len(set(nums))


def p1(cards):
    # int(2**(matches-1)) generates the correct "score" for each card
    # in problem 1 given the number of matches
    return sum(int(2 ** (count_matches(c) - 1)) for c in cards)


def p2(cards):
    # Iterate sequentially over the cards keeping track of how many of each we have
    # at a given time.
    card_counts = [1] * len(cards)  # Default to one of each card
    for i, m in enumerate([count_matches(c) for c in cards]):
        for j in range(i + 1, m + i + 1):
            # When incrementing card counts, make sure to do so by the number of
            # times we have the current card
            card_counts[j] += card_counts[i]
    return sum(card_counts)


cards = open("input").read().split("\n")
print(p1(cards))
print(p2(cards))
