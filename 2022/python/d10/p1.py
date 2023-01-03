text = open("input3").read().replace("addx", "noop\naddx").split("\n")

value, p1, p2 = 1, 0, ""

for i, ins in enumerate(text):
    if i+1 in [20, 60, 100, 140, 180, 220]:
        p1 += (i+1)*value
    p2 += "#" if (i % 40) - 1 <= value <= (i % 40) + 1 else "."
    if ins[0] == 'a':
        value += int(ins[4:])
    print(i+1, value)

print(p1)
for x in range(6):
    print(p2[40*x:40*x+40])
