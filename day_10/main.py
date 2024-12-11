import itertools
import math

with open(r"day_10\data.txt") as file:
    lines = [list([int(i) for i in l.strip()]) for l in file] 

def print_grid(g):
    for l in g:
        print(l)

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def check_valid(coord, grid):
    return 0 <= coord[0] < len(grid) and 0 <= coord[1] < len(grid[0])

import typing as tp
def find_path_count(grid, target):

    steps = {(-1,0), (1,0), (0,-1), (0,1)}

    acc: tp.List[tp.List[tp.Set]] = []
    for i in range(len(grid)):
        acc.append([])
        for j in range(len(grid[0])):
            acc[i].append(0)


    open_nodes = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == target:
                open_nodes.append((i,j))
                acc[i][j] = 1
    
    while open_nodes:
        cur = open_nodes.pop()

        for dir in steps:
            nxt = tuple_add(cur, dir)
            if check_valid(nxt, grid) and grid[cur[0]][cur[1]] - grid[nxt[0]][nxt[1]] == 1:
                acc[nxt[0]][nxt[1]] += 1
                open_nodes.append(nxt)
    
    return acc

vals = find_path_count(lines, 9)
print_grid(lines)
print()
print_grid(vals)

tot = 0
for i in range(len(lines)):
    for j in range(len(lines[0])):
        if lines[i][j] == 0:
            tot += vals[i][j]

print(tot)

# grid = [
#     [0, 1, 2],
#     [0, 2, 0],
# ]

# print(find_path_count(grid, 2))

