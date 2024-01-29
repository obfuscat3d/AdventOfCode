def hf(s, acc=0):
    return acc if not s else hf(s[1:], (acc + ord(s[0])) * 17 % 256)


def part2(data):
    boxes = [{} for _ in range(256)]
    for ts in [d.split("=") for d in data]:
        if len(ts) == 2:
            boxes[hf(ts[0])][ts[0]] = int(ts[1])
        else:
            boxes[hf(ts[0][:-1])].pop(ts[0][:-1], None)
    print(
        sum(
            (1 + i) * (1 + j) * b[k]
            for i, b in enumerate(boxes)
            for j, k in enumerate(b)
        )
    )


data = open("input").read().strip().split(",")
print(sum(hf(s) for s in data))  # part 1
part2(data)
