from collections import Counter, deque


with open(r"day_5\data.txt") as file:
    lines = [l.strip() for l in file]

rules = lines[:lines.index("")]
values = lines[lines.index("")+1:]

edges = []
r_d = {}
for rule in rules:
    a = rule.split("|")

    if int(a[0]) in r_d:
        r_d[int(a[0])].add(int(a[1]))
    else:
        r_d[int(a[0])] = {int(a[1])}

    edges.append([int(a[0]), int(a[1])])

def check_row(l, r_d):
    seen = set()
    for c in l:
        if seen.intersection(r_d.get(c, set())):
            print(f"{c} happened after one of {r_d.get(c, set())}")
            return False
        else:
            seen.add(c)
    
    return True

def topological_sort(adj, V):

    # Vector to store indegree of each vertex
    indegree = [0] * V
    for i in range(V):
        for vertex in adj[i]:
            indegree[vertex] += 1
    
    # Queue to store vertices with indegree 0
    q = deque()
    for i in range(V):
        if indegree[i] == 0:
            q.append(i)
    result = []
    while q:
        node = q.popleft()
        result.append(node)
        # Decrease indegree of adjacent vertices as the current node is in topological order
        for adjacent in adj[node]:
            indegree[adjacent] -= 1
            # If indegree becomes 0, push it to the queue
            if indegree[adjacent] == 0:
                q.append(adjacent)

    # Check for cycle
    assert len(result) == V, "Graph contains cycle!"

    return result


def get_sorted(edges):
    h = 0
    for n in edges:
        h = max(h, n[0], n[1])
    
    # Number of nodes
    V = h + 1

    # Graph represented as an adjacency list
    adj = [[] for _ in range(V)]

    for i in edges:
        adj[i[0]].append(i[1])

    vals = topological_sort(adj, V)
    # assert check_row(vals, r_d)
    return vals

def fix(vs, sorted_list):
    vs = [int(v) for v in vs]
    print(vs)

    cs = Counter(vs)

    new_l = []
    for v in sorted_list:
        if cs[v] > 0:
            new_l += [v] * cs[v]
    print(new_l)
    assert len(vs) == len(new_l)
    assert set(vs) == set(new_l)
    # assert check_row(new_l, r_d)

    return new_l

def fix_2(vs, r_d):
    print(vs)

    new_r_d = {k: [v for v in r_d[k] if v in vs] for k in r_d if k in vs}

    edges = []
    for k, values in new_r_d.items():
        for v in values:
            edges.append([k,v])

    print(vs)
    return fix(vs, get_sorted(edges))

tot_0 = 0
tot_1 = 0

for v in values:
    s_v = [int(a) for a in v.split(",")]
    if check_row(s_v, r_d):
        tot_0 += int(s_v[(len(s_v) - 1)//2])
    else:
        print(s_v)
        new_v = fix_2(s_v, r_d)
        print(new_v)
        tot_1 += int(new_v[(len(new_v) - 1)//2])

print(tot_0)
print(tot_1)

# edges = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 1], [5, 2]]
# print(get_sorted(edges))