with open('2020/d13/input') as input:
    [depart, busses] = input.read().splitlines()
    depart = int(depart)
    busses = [int(x) for x in busses.split(',') if x != 'x']

times = [(bus_id, bus_id - depart % bus_id) for bus_id in busses]
times.sort(key=lambda x: x[1])
print(times[0][0]*times[0][1])
