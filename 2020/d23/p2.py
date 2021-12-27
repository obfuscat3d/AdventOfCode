INPUT = [int(i) for i in '586439172']

class LLNode:
    def __init__(self, value, prev=None):
        self.value = value
        self.next = None
        self.prev = prev
        if prev:
            self.prev.next = self
    
    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self

    def insert(self, item):
        item.next = self.next
        item.prev = self
        self.next.prev = item
        self.next = item

def step(head, cups_map):
    removed = [head.next.remove(), head.next.remove(), head.next.remove()]
    removed_values = [x.value for x in removed]
 
    dest_value = head.value - 1
    while dest_value in removed_values or dest_value == 0:
        dest_value -= 1
        if dest_value <= 0:
            dest_value = len(cups_map)
    dest = cups_map[dest_value]

    dest.insert(removed.pop())
    dest.insert(removed.pop())
    dest.insert(removed.pop())

    return head.next if dest != head else head.next.next.next.next

def LLinit(numbers):
    cups_map = {}
    head = cur = LLNode(numbers[0])
    cups_map[head.value] = head
    for x in numbers[1:]:
        cur = LLNode(x, cur)
        cups_map[cur.value] = cur
    head.prev = cur
    cur.next = head
    return head, cups_map

def part2(input):
    input.extend(range(10,1000001))
    head, cups_map = LLinit(input)
    for x in range(10000000):
        head = step(head, cups_map)
    print(cups_map[1].next.value*cups_map[1].next.next.value)

part2(INPUT)
