with open('2020/d13/input') as input:
    [_, busses] = input.read().splitlines()
    busses = [x for x in busses.split(',')]

bus_intervals = []
for i in range(len(busses)):
    if busses[i] != 'x':
        bus_intervals.append((i, int(busses[i])))


x = 1
adder = 1
while bus_intervals:
    to_remove = []
    for y in bus_intervals:
        if (x % y[1] == ((y[1] - y[0]) % y[1])):
            adder *= y[1]
            to_remove.append(y)
    print(x, len(bus_intervals), to_remove)
    for l in to_remove:
        bus_intervals.remove(l)
    x += adder
