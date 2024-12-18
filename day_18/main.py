import attrs
import typing as tp

with open(r"day_18\tst.txt") as file:
    tst_i, tst_j = 7,7
    tst_grid = [[int(i) for i in l.split(",")] for l in file] 

with open(r"day_18\data.txt") as file:
    m_i, m_j = 71,71
    m_grid = [[int(i) for i in l.split(",")] for l in file] 

def print_grid(g):
    for l in g:
        print(l)

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def check_valid(coord, grid):
    return 0 <= coord[0] < len(grid) and 0 <= coord[1] < len(grid[0])

directions = {
    (0,-1),
    (1,0),
    (0,1),
    (-1,0) 
}

@attrs.define
class Sim:
    length: int
    order: tp.List[tp.List[int]]
    _grid: tp.List[tp.List[int]] = []
    i: int = 0

    start:tp.Tuple[int, int] = (0,0)

    def gen(self):
        self._grid = []

        for i in range(self.length):
            self._grid.append([])
            for j in range(self.length):
                self._grid[i].append(-1)

    def apply_order(self, x):
        for _ in range(x):
            if self.i < len(self.order):
                c = self.order[self.i]
                self.i += 1

                self._grid[c[1]][c[0]] = -2

    def dijk(self, target, app):
        self.gen()
        self.apply_order(app)


        nodes = [(0,0)]
        visited = set()

        self._grid[0][0] = 0

        while nodes:
            base = nodes.pop()
            b_val = self._grid[base[0]][base[1]]

            for d in directions:
                cur = tuple_add(d, base)
                if cur in visited:
                    continue
                elif not check_valid(cur, self._grid):
                    continue
                else:
                    visited.add(cur)
                
                if cur == target:
                    return b_val + 1

                c_val = self._grid[cur[0]][cur[1]]

                if c_val != -2:
                    if c_val == -1:
                        self._grid[cur[0]][cur[1]] = b_val + 1
                    else:
                        self._grid[cur[0]][cur[1]] = min(c_val, b_val + 1)
                    nodes.insert(0,cur)

        return -1
    

s = Sim(7,tst_grid)
s.gen()
s.apply_order(21)
print(tst_grid[20])
print_grid(s._grid)
# print(s.dijk((6,6), 21))

# i = 0
# while True:
#     i += 1
#     sm = Sim(7,tst_grid)
#     if sm.dijk((6,6), i) == -1:
#         raise ValueError(i)

sm = Sim(m_j,m_grid)
sm.gen()
sm.apply_order

print(m_grid[2960])

