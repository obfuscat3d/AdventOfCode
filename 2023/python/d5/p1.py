def parse(text):
    sections = text.split("\n\n")
    seeds, maps = [int(n) for n in sections[0].split()[1:]], []
    for section in sections[1:]:
        maps.append([])
        for l in section.split("\n")[1:]:
            maps[-1].append(tuple(int(i) for i in l.split()))
    return seeds, maps


# ii = "initial interval", a (start, end) tuple where end is inclusive
# maps = list of mappings still to be processed
def best(ii, maps):
    # if we've done the final mapping, just return the lowest value
    if not maps:
        return ii[0]

    # d = destination
    # s = start
    # r = range
    for d, s, r in maps[0]:
        # range is entirely inside a mapping
        if s <= ii[0] < s + r and s <= ii[1] < s + r:
            r1 = (d + ii[0] - s, d + ii[1] - s)
            return best(r1, maps[1:])

        # range starts inside a mapping but ends outside
        elif s <= ii[0] < s + r and s + r < ii[1]:
            r1 = (d + ii[0] - s, d + r)
            r2 = (s + r, ii[1])
            return min(best(r1, maps[1:]), best(r2, maps))

        # range starts below a mapping but ends inside mapping
        elif ii[0] < s and s <= ii[1] < s + r:
            r1 = (ii[0], s - 1)
            r2 = (d, d + ii[1] - s)
            return min(best(r1, maps), best(r2, maps[1:]))

        # range begins below and ends above a mapping
        elif ii[0] < s and ii[1] > s + r:
            r1 = (ii[0], s - 1)
            r2 = (d, d + r)
            r3 = (s + r, ii[1])
            return min(best(r1, maps), best(r2, maps[1:]), best(r3, maps))

    # No maps matched this range. Preserve values and move on.
    return best(ii, maps[1:])


rs, maps = parse(open("input").read())

# part 1, just create a (start, end) tuple for each seed
iis1 = [(i, i) for i in rs]
print(min((best(ii, maps) for ii in iis1)))

# part 2, note the -1 for the second number since we use inclusive ranges
iis2 = [(rs[2 * i], rs[2 * i] + rs[2 * i + 1] - 1) for i in range(len(rs) // 2)]
print(min((best(ii, maps) for ii in iis2)))
