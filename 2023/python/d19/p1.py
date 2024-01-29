import re, math, operator, collections

Condition = collections.namedtuple("Condition", ("xmas", "op", "n", "result"))
is_empty_gaggle = lambda g: any(x[1] < x[0] for x in g)


def build_single_workflow(line):
    conds = []
    for entry in line.split(","):
        if ":" in entry:
            xmas, op, n, res = re.search(r"(\w)([<>])(\d+):(\w+)", entry).groups()
            conds.append(Condition("xmas".index(xmas), op, int(n), res))
        else:
            conds.append(Condition(None, None, None, entry))
    return conds


def parse(text):
    workflows, parts = {}, []

    for l in text.split("\n\n")[0].split("\n"):
        label, l_text = l.split("{")
        workflows[label] = build_single_workflow(l_text[:-1])

    for l in text.split("\n\n")[1].split("\n"):
        parts.append(tuple(map(int, re.findall("\d+", l))))

    return workflows, parts


def process_single_part_workflow(workflow, part):
    loc = "in"
    for cond in workflow:
        if not cond.op:
            return cond.result
        else:
            op = operator.lt if cond.op == "<" else operator.gt
            if op(part[cond.xmas], cond.n):
                return cond.result


def part1(workflows, parts):
    accepted = []
    for part in parts:
        loc = "in"
        while loc not in "AR":
            loc = process_single_part_workflow(workflows[loc], part)
        accepted.append(part) if loc == "A" else None
    print(sum(sum(a) for a in accepted))


def split_gaggle(gg, xmas, n):
    a = tuple((g[0], g[1]) if xmas != i else (g[0], n - 1) for i, g in enumerate(gg))
    b = tuple((g[0], g[1]) if xmas != i else (n, g[1]) for i, g in enumerate(gg))
    return a, b


def process_gaggle_workflow(workflow, gaggle):
    to_enqueue = []
    for cond in workflow:
        if is_empty_gaggle(gaggle):
            continue
        elif not cond.op:
            to_enqueue.append((cond.result, gaggle))
        else:
            xmas, op, n, result = cond
            if op == "<":
                a, b = split_gaggle(gaggle, xmas, n)
                if not is_empty_gaggle(a):
                    to_enqueue.append((result, a))
                gaggle = b
            else:
                a, b = split_gaggle(gaggle, xmas, n + 1)
                if not is_empty_gaggle(b):
                    to_enqueue.append((result, b))
                gaggle = a
    return to_enqueue


def part2(workflows):
    accepted = 0
    q = [("in", ((1, 4000), (1, 4000), (1, 4000), (1, 4000)))]
    while q:
        wf_label, gaggle = q.pop()
        if wf_label == "A":
            print(gaggle)
            accepted += math.prod(g[1] - g[0] + 1 for g in gaggle)
        elif wf_label != "R":
            q.extend(process_gaggle_workflow(workflows[wf_label], gaggle))
    print(accepted)


workflows, parts = parse(open("input2").read())
part1(workflows, parts)
part2(workflows)
