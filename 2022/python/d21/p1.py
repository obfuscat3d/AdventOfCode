from operator import add, sub, mul, floordiv

S2O = {'-': sub, '+': add, '/': floordiv, '*': mul}
INVERSE_OP = {add: sub, sub: add, floordiv: mul, mul: floordiv}


class Node:
    def __init__(self, nodes, l, r, op, val):
        self.nodes, self.l, self.r, self.op, self._val = nodes, l, r, op, val

    def val(self):
        if self._val:
            return self._val
        if isinstance(self.l, str):
            self.l, self.r = self.nodes[self.l], self.nodes[self.r]
        if self.r and self.r.val() != None and self.l.val() != None:
            self._val = self.op(self.l.val(), self.r.val())
            return self._val
        return None


def node_from_str(nodes, s, part2):
    f = s.split(' ')
    if f[0] == 'humn:' and part2:
        nodes[f[0][:4]] = Node(nodes, None, None, None, None)
    elif len(f) == 2:
        nodes[f[0][:4]] = Node(nodes, None, None, None, int(f[1]))
    else:
        nodes[f[0][:4]] = Node(nodes, f[1], f[3], S2O[f[2]], None)


def parse(part2=False):
    nodes = {}
    [node_from_str(nodes, s, part2)
     for s in open('input').read().split('\n')]
    return nodes


def solve_for_variable(nodes, x, y):
    while x.r:  # until the variable is isolated
        if x.r.val() == None:
            if x.op in [add, mul]:
                x, y = x.r, Node(nodes, y, x.l, INVERSE_OP[x.op], None)
            else:
                x, y = x.r, Node(nodes, x.l, y, x.op, None)
        else:
            x, y = x.l, Node(nodes, y, x.r, INVERSE_OP[x.op], None)
    return y.val()


def part1():
    print(parse()['root'].val())


def part2():
    nodes = parse(part2=True)
    r = nodes['root']
    r.val()  # need to compute the tree
    print(solve_for_variable(nodes,
                             r.l if r.r.val() else r.r,
                             r.r if r.r.val() else r.l))


part1()
part2()
