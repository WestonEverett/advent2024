import functools
import itertools
import attrs
import typing as tp

numeric_keypad = [
    ["7","8","9"],
    ["4","5","6"],
    ["1","2","3"],
    [" ", "0", "A"]
]
num_start = (3,2)

dir_keypad = [
    [" ", "^", "A"],
    ["<", "v", ">"]
]
dir_start = (0,2)

def grid_to_map(grid):
    mp = {}
    for i, l in enumerate(grid):
        for j, c in enumerate(l):
            mp[(i,j)] = c
    
    return mp

def inv_map(inp):
    mp = {}

    for k,v in inp.items():
        mp[v] = k

    return mp

num_map = grid_to_map(numeric_keypad)
dir_map = grid_to_map(dir_keypad)
num_lookup = inv_map(num_map)
dir_lookup = inv_map(dir_map)

directions = {
    (1,0): "v",
    (-1,0): "^",
    (0,1): ">",
    (0,-1): "<"
}

appl = {
    "v" : (1,0),
    "^": (-1,0),
    ">": (0,1),
    "<" :(0,-1) 
}

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def find(keypad, target):
    for i in range(len(keypad)):
        for j in range(len(keypad[i])):
            if keypad[i][j]== target:
                return (i,j)
    
    raise ValueError

def get_path(pos, t_pos, banned):
    path = ""

    diff = tuple_sub(t_pos, pos)

    if diff[1] > 0:
        path += directions[(0,1)] * diff[1]

    if diff[0] > 0:
        path += directions[(1,0)] * diff[0]
    if diff[0] < 0:
        path += directions[(-1,0)] * abs(diff[0])
    
    if diff[1] < 0:
        path += directions[(0,-1)] * abs(diff[1])
    
    path += "A"

    return path

@attrs.define 
class Bot:
    keypad: tp.List[tp.List]
    kp_map: tp.Dict
    i_map: tp.Dict
    pos: tp.Tuple[int, int]
    instr: tp.Iterable

    @classmethod
    def build(cls, pos, instr, k_type = None)->"Bot":
        if k_type == "num":
            keypad= numeric_keypad
            kp_map = num_map
            i_map = num_lookup
        else:
            keypad=  dir_keypad
            kp_map = dir_map
            i_map = dir_lookup

        return cls(
            keypad,
            kp_map,
            i_map,
            pos,
            instr
        )

    def readout(self):
        cur = ""
        for ins in self.instr:
            if ins == "A":
                cur += self.kp_map[self.pos]
            else:
                self.pos = tuple_add(self.pos, appl[ins])
        
        return cur


    def get_next(self, target):
        t_pos = self.i_map[target] 
        path = get_path(self.pos, t_pos, self.i_map[" "])
        self.pos = t_pos
        return path
    
    def move(self):
        for inst in self.instr:
            for step in self.get_next(inst):
                yield step


instrs = [
    "123A",
    "877A",
    "882A",
    "810A",
    "287A"
]

total = 0
for ins in instrs:
    b_n = Bot.build(
        num_start,
        ins,
        "num"
    )

    b_1 = Bot.build(
        dir_start,
        b_n.move()
    )

    b_2 = Bot.build(
        dir_start,
        b_1.move()
    )

    res = ''.join(list(b_2.move()))
    s = int(ins[:-1])

    print(f"{len(res)} * {s}")

    total += s * len(res)

print(total)

print("EVERYTHING ABOVE HAS A BUG, SOME MINMOVESETS ARE NOT OPTIMAL")

def get_all_moves(cur:tp.Tuple[int,int], tar:tp.Tuple[int,int], banned:tp.Tuple[int,int]):
    path = ""

    diff = tuple_sub(tar, cur)

    if diff[1] > 0:
        path += directions[(0,1)] * diff[1]

    if diff[0] > 0:
        path += directions[(1,0)] * diff[0]
    if diff[0] < 0:
        path += directions[(-1,0)] * abs(diff[0])
    
    if diff[1] < 0:
        path += directions[(0,-1)] * abs(diff[1])


    valid_sequences = set()
    for p in set(itertools.permutations(path)):
        pos = cur
        valid = True

        for move in p:
            pos = tuple_add(pos, appl[move])

            if pos == banned:
                valid = False

        if valid:
            valid_sequences.add(''.join(p) + "A")
    
    return valid_sequences

@functools.cache
def count_steps(seq, bot, bots, cur = None):
    
    # Get maps
    if bot == 0:
        keypad= numeric_keypad
        kp_map = num_map
        i_map = num_lookup
    else:
        keypad=  dir_keypad
        kp_map = dir_map
        i_map = dir_lookup
    
    # Return if empty
    if not seq:
        return 0
    
    # Get start
    if cur is None:
        cur = i_map["A"]

    # If we are on a bot
    if bot <= bots:
        pos = []

        for path in get_all_moves(cur, i_map[seq[0]], i_map[" "]):
            pos.append(count_steps(path, bot+1, bots))
        
        min_len = min(pos)
    else:
        min_len = 1

    return min_len+count_steps(seq[1:], bot, bots, i_map[seq[0]])

total = 0
for ins in instrs:
    res = count_steps(ins, 0, 2)
    s = int(ins[:-1])

    print(f"{res} * {s}")

    total += s * res

print(f"1: {total}")

total = 0
for ins in instrs:
    res = count_steps(ins, 0, 25)
    s = int(ins[:-1])

    print(f"{res} * {s}")

    total += s * res

print(f"2: {total}")