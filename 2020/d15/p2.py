
# input from AoC

history = {1: 0, 20: 1, 11: 2, 6: 3, 12: 4}
turn = 5
next = 0

while turn < 30000000-1:  # 2020:
    temp = (turn-history[next]) if next in history else 0
    history[next] = turn
    next = temp

    turn += 1

print(next)
