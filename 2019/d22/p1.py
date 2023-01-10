deck = list(range(10007))
for ins in open("input").read().split('\n'):
    if "stack" in ins:
        deck = deck[::-1]
    elif "increment" in ins:
        n = int(ins.split()[-1])
        new_deck = [None] * len(deck)
        for i, j in enumerate(range(0, n * len(deck), n)):
            new_deck[j % len(deck)] = deck[i]
        deck = new_deck
    elif "cut" in ins:
        n = int(ins.split()[-1]) % len(deck)
        deck = deck[n:] + deck[:n]

print(deck.index(2019))
