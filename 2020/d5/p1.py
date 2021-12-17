FILE = '2020/d5/input'


def get_seatid(text):
    row = int(text[:-3].replace('B', '1').replace('F', '0'), 2)
    col = int(text[-3:].replace('R', '1').replace('L', '0'), 2)
    return 8*row + col


with open(FILE) as input:
    ids = [get_seatid(line) for line in input.read().splitlines()]

# part 1
print(max(ids))

# part 2
for x in range(84, 866):
    if x not in ids:
        print(x)
