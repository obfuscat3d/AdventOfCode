from collections import Counter

ORDER_1 = "23456789TJQKA"
ORDER_2 = "J23456789TQKA"


def score(h, jw):
    if jw and h == "JJJJJ":
        return ([5], 0)
    order = ORDER_2 if jw else ORDER_1
    freq = sorted(Counter([c for c in h if c != "J" or not jw]).values())
    freq[-1] += h.count("J") if jw else 0
    return (
        freq[::-1],
        sum(order.index(c) * (13**i) for i, c in enumerate(h[::-1])),
    )


def go(hands, jacks_wild):
    hands = sorted(hands, key=lambda h: score(h[0], jacks_wild))
    print(sum((1 + i) * int(h[1]) for i, h in enumerate(hands)))


hands = [x.split() for x in open("input").read().split("\n")]
go(hands, False)
go(hands, True)
