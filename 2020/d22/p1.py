from collections import deque
import re

def round(p1, p2):
    a, b = p1.popleft(), p2.popleft()
    if a < b:
        p2.append(b)
        p2.append(a)
    else:
        p1.append(a)
        p1.append(b)
    return p1, p2
    
def game(p1, p2):
    while p1 and p2:
        p1, p2 = round(p1, p2)
    return p1 if len(p1) else p2

def score(hand):
    return sum([x*(len(hand)-i) for i,x in enumerate(hand)])

with open('2020/d22/input') as input:
    numbers = [int(i) for i in filter(re.compile("^\d+$").match, input.read().splitlines())]

p1, p2 = deque(numbers[:len(numbers)//2]), deque(numbers[len(numbers)//2:])
print(score(game(p1,p2)))