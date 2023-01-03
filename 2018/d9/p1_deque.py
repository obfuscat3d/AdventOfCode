from collections import deque


def turn(player_ct, scores, marbles, marble):
    if marble % 23 != 0:
        marbles.rotate(-1)
        marbles.append(marble)
    else:
        marbles.rotate(7)
        scores[marble % player_ct] += marble + marbles.pop()
        marbles.rotate(-1)


def part1(player_ct, marble_ct):
    marble, scores = 1, [0] * player_ct
    marbles = deque([0])
    while marble < marble_ct:
        turn(player_ct, scores, marbles, marble)
        marble += 1
    print(max(scores.values()))


def part2(player_ct, marble_ct):
    part1(player_ct, marble_ct * 100)


part1(455, 71223)
part2(455, 71223)
