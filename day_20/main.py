import copy
import functools
import itertools
import attrs
import typing as tp

import heapq

with open(r"day_20\map.txt") as file:
    base_grid = [list(l.strip()) for l in file] 

def print_grid(g):
    for l in g:
        print(l)

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

directions = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1)
]

def adj(coord: tp.Tuple[int,int])->tp.List[tp.Tuple[int,int]]:
    moves = []

    for d in directions:
        moves.append(
            tuple_add(coord, d)
        )
    
    return moves

def print_grid(g):
    dist = 5
    for l in g:
        line = ""
        for c in l:
            sc = str(c)
            ju = dist - len(sc)
            line += " " * ju + sc
        print(line)

@attrs.define(frozen=True)
class Position:
    g: float = float("inf")
    h: float = float("inf")
    parent: tp.Optional[tp.Tuple[int, int]] = None
        
    @property
    def f(self):
        return self.g + self.h


def find_start(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return (i,j)
    
    raise ValueError

def find_end(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "E":
                return (i,j)
    
    raise ValueError

def sgn(d: int):
    if d < 0:
        return -1
    
    if d == 0:
        return 0
    
    return 1

@attrs.define
class Maze:
    maze: tp.List[tp.List[str]]
    start: tp.Tuple[int, int]
    end: tp.Tuple[int, int]
    
    _active_maze: tp.List[tp.List[str]] = []

    @classmethod
    def build(cls, maze):
        end = find_end(maze)
        start = find_start(maze)
        return cls(maze, start, end)
    
    def heur(self, coord: tp.Tuple[int, int]):
        delta = tuple_sub(self.end, coord)
        return abs(delta[0]) + abs(delta[1])
        
    def check_valid(self, coord):
        return 0 <= coord[0] < len(self.maze) and 0 <= coord[1] < len(self.maze[0])

    def trace_path(self, positions, end):
        path = [end]
        while (cur := positions[path[0][0]][path[0][1]]).parent is not None:
            path.insert(0, cur.parent)

        return path
    
    def solve(self, skip = tp.Set[tp.Tuple[int,int]]):
        r = len(self.maze)
        c = len(self.maze[0])  

        closed_list = [[False for _ in range(c)] for _ in range(r)]
        nodes = []

        positions = [[Position() for _ in range(c)] for _ in range(r)]

        start_node = Position(0, self.heur(self.start), None)
        positions[self.start[0]][self.start[1]] = start_node

        heapq.heappush(nodes, (start_node.f, self.start))

        while nodes:
            val = heapq.heappop(nodes)
            cur: tp.Tuple[int, int] = val[1]

            cur_node = positions[cur[0]][cur[1]]

            closed_list[cur[0]][cur[1]] = True

            if self.maze[cur[0]][cur[1]] == "E":
                return self.trace_path(positions, self.end)

            for n in adj(cur):
                if not self.check_valid(n) or (self.maze[n[0]][n[1]] == "#" and n not in skip):
                    continue

                new_pos = Position(cur_node.g + 1, self.heur(n), cur)

                if new_pos.f < positions[n[0]][n[1]].f:
                    positions[n[0]][n[1]] = new_pos
                    heapq.heappush(nodes, (new_pos.f, n))

        raise ValueError


    def alt_solve(self, min_jump):
        base_solve = self.solve()

        b_maze = copy.deepcopy(self.maze)
        nodes = [self.end]

        b_maze[self.end[0]][self.end[1]] = 0

        while nodes:
            base = nodes.pop(0)
            b_val = b_maze[base[0]][base[1]]

            for d in directions:
                cur = tuple_add(d, base)

                if not self.check_valid(cur):
                    continue
                
                if b_maze[cur[0]][cur[1]] in [".", "S"]:
                    b_maze[cur[0]][cur[1]] = b_val + 1
                    nodes.append(cur)

        f_maze = copy.deepcopy(self.maze)
        nodes = [self.end]

        f_maze[self.end[0]][self.end[1]] = 0

        while nodes:
            base = nodes.pop(0)
            b_val = f_maze[base[0]][base[1]]

            for d in directions:
                cur = tuple_add(d, base)

                if not self.check_valid(cur):
                    continue
                
                if f_maze[cur[0]][cur[1]] in [".", "E"]:
                    f_maze[cur[0]][cur[1]] = b_val + 1
                    nodes.append(cur)

        cheats = tp.Set[tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]]
        for i in range(1, len(self.maze) - 1):
            for j in range(1, len(self.maze[0]) - 1):
                if self.maze[i][j] != "#":
                    continue

                fs = []
                bs = []
                for n_i_1, n_j_1 in adj((i,j)):
                    for n_i_2, n_j_2 in adj((i,j)):
                        if isinstance(f_maze[n_i_1][n_j_1], int) and isinstance(b_maze[n_i_2][n_j_2], int):
                            sol = f_maze[n_i_1][n_j_1] + b_maze[n_i_2][n_j_2]
                            if (sol + 2) - min_jump <= len(base_solve) - 1:
                                cheats.add(((n_i_1, n_j_1), (n_i_2, n_j_2)))

                    
        
        return len(cheats)
    

maze = Maze.build(base_grid)
print(maze.alt_solve(100))
# base = len(maze.solve())
# count = 0
# for i in range(1, len(maze.maze) - 1):
#     print(i)
#     for j in range(1, len(maze.maze[0]) - 1):
#         if maze.maze[i][j] == "#":
#             n = len(maze.solve({(i,j)}))
#             if n + 100 >= base:
#                 count += 1

# print(count)
