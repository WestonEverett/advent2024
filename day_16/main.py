import attrs
import typing as tp

import heapq

with open(r"day_16\tst.txt") as file:
    base_grid = [list(l.strip()) for l in file] 

def print_grid(g):
    for l in g:
        print(l)

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

@attrs.define(frozen=True)
class Position:
    coord: tp.Tuple[int, int]
    direction: tp.Tuple[int, int]
    cost: int

    def potential(self) -> tp.List["Position"]:
        moves = []

        moves.append(
            Position(tuple_add(self.coord, self.direction), self.direction, self.cost+1)
        )

        if self.direction[0] == 0:
            moves.append(
                Position(self.coord, (1,0), self.cost+1000)
            )
            moves.append(
                Position(self.coord, (-1,0), self.cost+1000)
            )
        
        if self.direction[1] == 0:
            moves.append(
                Position(self.coord, (0,1), self.cost+1000)
            )
            moves.append(
                Position(self.coord, (0,-1), self.cost+1000)
            )
        
        return moves


def find_start(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return Position((i,j), (0,1), 0)
    
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
    start: Position
    end: tp.Tuple[int, int]

    cost: int = None

    @classmethod
    def build(cls, maze):
        start = find_start(maze)
        end = find_end(maze)
        return cls(maze, start, end)
    
    def heur(self, pos: Position):
        score = pos.cost

        delta = tuple_sub(self.end, pos.coord)

        score += abs(delta[0]) + abs(delta[1])

        if delta[0] != 0:
            score += abs(sgn(delta[0]) - sgn(pos.direction[0])) * 1000
        
        if delta[1] != 0:
            score += abs(sgn(delta[1]) - sgn(pos.direction[1])) * 1000
        
        return score
    
    def spread(self, explored, cur):
        a = set()

        
    
    def solve(self):
        ent = 0

        nodes = [(0, ent, self.start)]

        explored = dict()

        while nodes:
            val = heapq.heappop(nodes)
            cur: Position = val[2]

            if self.cost is not None:
                if cur.cost > self.cost:
                    continue

            # explored.add((cur.coord, cur.direction))

            if self.maze[cur.coord[0]][cur.coord[1]] == "E":
               self.cost = cur.cost
               print("MADE IT")

            for n in cur.potential():
                if self.maze[n.coord[0]][n.coord[1]] != "#":
                    if (exp := explored.get((n.coord, n.direction), None)) is not None:
                        if exp[0] == n.cost:
                            new_sources = exp[1] + [cur]
                            explored[(n.coord, n.direction)] = (exp[0], new_sources)
                        elif exp[0] > n.cost:
                            explored[(n.coord, n.direction)] = (n.cost, [cur])
                            print(exp)
                            print(n)
                    else:
                        ent += 1
                        explored[(n.coord, n.direction)] = (n.cost, [cur])
                        heapq.heappush(nodes, (self.heur(n), ent, n))
        
        for k in explored:
            print(k, explored[k])
        return self.cost
    
    def get_paths(self, score, loc: tp.Optional[Position] = None) -> tp.Tuple[tp.Dict[tp.Tuple[int,int], int]]:
        valid_visited = dict()
        valid_visited[loc.coord] = 0

        path_count = 0

        if loc is None:
            loc=self.start()

        if score < loc.cost:
            return {}, 0
        
        if score == loc.cost:
            if self.maze[loc.coord[0]][loc.coord[1]] == "E":
                return valid_visited, 1
            else:
                return {}, 0

        for n in loc.potential():
            if self.maze[n.coord[0]][n.coord[1]] != "#":
                res = self.get_paths(score, n)
                if res[1] != 0:
                    path_count += res[1]
                    valid_visited[loc.coord] += res[1]
                    valid_visited = valid_visited | res[0]
        







    

# def backtrack_solve(maze):
#     while 

maze = Maze.build(base_grid)
print(maze.solve())
