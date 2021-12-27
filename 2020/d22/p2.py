import re


def round(p1, p2):
    print('round', p1, p2)
    a, b = p1.pop(0), p2.pop(0)
    if a <= len(p1) and b <= len(p2):
        q1, q2 = game(p1[:a], p2[:b])
        if q1:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)
    else:
        if a < b:
            p2.append(b)
            p2.append(a)
        else:
            p1.append(a)
            p1.append(b)

    return p1, p2


def game(p1, p2):
    print('game', p1, p2)
    p1_hands = set()
    p2_hands = set()
    while p1 and p2:
        if str(p1) in p1_hands and str(p2) in p2_hands:
            return p1, []
        p1_hands.add(str(p1)) 
        p2_hands.add(str(p2))
        p1, p2 = round(p1, p2)
    return p1, p2


def score(hand):
    return sum([x*(len(hand)-i) for i,x in enumerate(hand)])


with open('2020/d22/input') as input:
    numbers = [int(i) for i in filter(re.compile("^\d+$").match, input.read().splitlines())]

p1, p2 = numbers[:len(numbers)//2], numbers[len(numbers)//2:]
p1, p2 = game(p1, p2)
#print(p1,p2)

print(score(p1) if p1 else score(p2))

