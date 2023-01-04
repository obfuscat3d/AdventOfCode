from collections import defaultdict

tm = {
    ('A', 0): (1, 1, 'B'),
    ('A', 1): (0, -1, 'B'),
    ('B', 0): (1, -1, 'C'),
    ('B', 1): (0, 1, 'E'),
    ('C', 0): (1, 1, 'E'),
    ('C', 1): (0, -1, 'D'),
    ('D', 0): (1, -1, 'A'),
    ('D', 1): (1, -1, 'A'),
    ('E', 0): (0, 1, 'A'),
    ('E', 1): (0, 1, 'F'),
    ('F', 0): (1, 1, 'E'),
    ('F', 1): (1, 1, 'A'),
}

state, pos, tape = 'A', 0, defaultdict(int)
for _ in range(12683008):
    write, move, new_state = tm[(state, tape[pos])]
    tape[pos], pos, state = write, move, new_state
print(sum(tape.values()))
