from types import SimpleNamespace


def Node(prev, next, data):
    return SimpleNamespace(prev=prev, next=next, data=data)


def insert(cur, data):
    new = Node(cur, cur.next, data)
    cur.next.prev = new
    cur.next = new
    return new


def remove(node):
    node.prev.next = node.next
    node.next.prev = node.prev
    return node.next


def turn(player_ct, scores, cur, next_val):
    if next_val % 23 != 0:
        cur = cur.next
        return insert(cur, next_val)
    else:
        for _ in range(7):
            cur = cur.prev
        scores[next_val % player_ct] += cur.data + next_val
        return remove(cur)


def part1(player_ct, marble_ct):
    next_val, scores = 1, [0] * player_ct
    cur = Node(None, None, 0)
    cur.next = cur.prev = cur
    while next_val < marble_ct:
        cur = turn(player_ct, scores, cur, next_val)
        next_val += 1
    print(max(scores))


def part2(player_ct, marble_ct):
    part1(player_ct, marble_ct * 100)


part1(455, 71223)
part2(455, 71223)
