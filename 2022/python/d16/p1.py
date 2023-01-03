from collections import namedtuple, defaultdict
from heapq import *


def parse_input(filename):
    valves, tunnels = {}, {}
    for line in open(filename).read().split('\n'):
        valve = line[6:8]
        flow_rate = int(line.split('=')[1].split(';')[0])
        new_tunnels = [x.strip() for x in line.split('valve')[1][1:].split(',')]
        valves[valve], tunnels[valve] = flow_rate, new_tunnels
    return [valves, tunnels]


def calc_distances(valves, tunnels):
    """ Floyd-Warshall FTW """
    dist = {a: {b: 1000 for b in valves} for a in valves}
    for u in valves:
        dist[u][u] = 0
        for v in tunnels[u]:
            dist[u][v] = 1
    for k in valves:
        for i in valves:
            for j in valves:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


# flow = total guaranteed flow from this state
# p1 = position of actor 1
# t1 = time when actor 1 can do something
# p2 = position of actor 2
# t2 = time when actor 2 can do something
# closed = list of valves already closed
State = namedtuple("State", "flow,p1,t1,p2,t2,closed")
State.time = lambda s: min(s.t1, s.t2)


def generate_new_human_states(valves, dist, s):
    if s.time() != s.t1:
        return [s]

    if valves[s.p1] and s.p1 in s.closed:
        return [s._replace(
            flow=s.flow - (29 - s.time()) * valves[s.p1],
            t1=s.t1 + 1,
            closed=s.closed - {s.p1})]

    new_states = [s._replace(p1=dest, t1=s.t1 + dist[s.p1][dest])
                  for dest in s.closed]

    if not new_states:
        return [s._replace(t1=30)]
    else:
        return new_states


def generate_new_elephant_states(valves, dist, states):
    new_states = []
    for s in states:
        if s.time() != s.t2:
            new_states.append(s)
        elif valves[s.p2] and s.p2 in s.closed:
            new_states.append(s._replace(
                flow=s.flow - (29 - s.time()) * valves[s.p2],
                t2=s.t2 + 1,
                closed=s.closed - {s.p2}))
        else:
            new_states.extend(
                [s._replace(p2=dest, t2=s.t2 + dist[s.p2][dest]) for dest in s.closed])

    if not new_states:
        return [s._replace(t2=30) for s in states]
    else:
        return new_states


def part1(valves, dist):
    pq, best, best_for_time = [], 0, defaultdict(int)
    heappush(pq, State(0, 'AA', 0, 'AA', 30, {k for k, v in valves.items() if v}))
    while pq:
        cur = heappop(pq)
        best = min(cur.flow, best)
        best_for_time[cur.time()] = min(best_for_time[cur.time()], cur.flow)
        if cur.time() < 30 and cur.closed:
            if cur.time() < 10 or 1.25 * cur.flow <= best_for_time[cur.time()]:
                for s in generate_new_human_states(valves, dist, cur):
                    heappush(pq, s)

    print(-best)


def part2(valves, dist):
    pq = []
    pq, best, best_for_time = [], 0, defaultdict(int)
    heappush(pq, State(0, 'AA', 4, 'AA', 4, set(k for k, v in valves.items() if v)))
    while pq:
        cur = heappop(pq)
        best = min(cur.flow, best)
        best_for_time[cur.time()] = min(best_for_time[cur.time()], cur.flow)
        if cur.time() < 30 and cur.closed:
            if cur.time() < 12 or 1.25 * cur.flow <= best_for_time[cur.time()]:
                h_states = generate_new_human_states(valves, dist, cur)
                e_states = generate_new_elephant_states(valves, dist, h_states)
                for s in e_states:
                    heappush(pq, s)
    print(-best)


valves, tunnels = parse_input('input')
dist = calc_distances(valves, tunnels)
part1(valves, dist)
part2(valves, dist)
