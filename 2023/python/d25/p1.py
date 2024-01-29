import random, re, collections, copy, networkx as nx, matplotlib.pyplot as plt

def parse(fn):
    graph = collections.defaultdict(list)
    for line in open(fn).readlines():
        labels = re.findall(r"\w+", line)
        for l in labels[1:]:
            graph[labels[0]].append(l)
            graph[l].append(labels[0])
    return graph

def visualize(graph):
    edges = [[a,b] for a, bs in graph.items() for b in bs]
    G = nx.Graph()
    G.add_edges_from(edges)
    nx.draw_networkx(G)
    plt.show()

def remove_edges_and_count(graph, edges_to_remove):
    for a, b in edges_to_remove:
        graph[a].remove(b)
        graph[b].remove(a)
    seen, q = set(), [random.choice(list(graph.keys()))]
    while q:
        n = q.pop()
        seen.add(n)
        q.extend(c for c in graph[n] if c not in seen)
    return (len(graph)-len(seen))*len(seen)

def part1_manual(graph):
    # derived visually from visualize() method
    to_remove = [('zhg', 'fmr'), ('krf', 'crg'), ('rgv','jct')]
    print(remove_edges_and_count(graph, to_remove))

def part1_networkx_mincut(graph):
    nodes, cut_value, G = list(graph.keys()), 0, nx.Graph()
    for a,b in [[a,b] for a, bs in graph.items() for b in bs]:
        G.add_edge(a, b, capacity=1)
    while cut_value != 3:
        a, b = random.choices(nodes, k=2)
        cut_value, partition = nx.minimum_cut(G, a, b)
    reachable, non_reachable = partition
    print(len(reachable)*len(non_reachable))

def part1_random(graph):
    nodes = list(graph.keys())
    edge_count = collections.defaultdict(int)
    for _ in range(1000):
        seen = set()
        start, dest = random.choices(nodes, k=2)
        q = [(start, [start])] 
        while q:
            n, path = q.pop(0)
            if n == dest:
                for a,b in zip(path[:-1], path[1:]):
                    edge_count[(min(a,b),max(a,b))] += 1
                break
            seen.add(n)
            q.extend((c, path+[c]) for c in graph[n] if c not in seen)
    to_remove = sorted(edge_count.items(), key=lambda x: x[1], reverse=True)[:3]
    print(remove_edges_and_count(graph, [e[0] for e in to_remove]))

def part1_networkx_girvan_newman(graph):
    G = nx.Graph()
    for a,b in [[a,b] for a, bs in graph.items() for b in bs]:
        G.add_edge(a, b, capacity=1)
    commiunities = next(nx.community.girvan_newman(G))
    print(len(commiunities[0])*len(commiunities[1]))

graph = parse("input")
#visualize(graph)
part1_manual(copy.deepcopy(graph))
part1_networkx_mincut(copy.deepcopy(graph))
part1_random(copy.deepcopy(graph))
part1_networkx_girvan_newman(copy.deepcopy(graph))
