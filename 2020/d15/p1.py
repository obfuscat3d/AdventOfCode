
# input from AoC
history = [0, 12, 6, 11, 20, 1]

while len(history) < 2020:
    last = history[0]
    if not last in history[1:]:
        history.insert(0, 0)
    else:
        history.insert(0, history[1:].index(last)+1)

print(history[0])
