import math

with open(r"day_9\data.txt") as file:
    lines = [l.strip() for l in file] 

line = [int(i) for i in lines[0]]

def proc(line):
    new_line = []

    for i in range(0,len(line),2):
        new_line += [i//2] * line[i]
        if i + 1 < len(line):
            new_line += [-1] * line[i+1]

    return new_line

def gen(line):
    for val in line[::-1]:
        if val != -1:
            yield val

def combine(line):
    n_l = proc(line)

    i_values = len([i for i in n_l if i != -1])

    r_grab = gen(n_l)

    res = []

    for i in range(i_values):
        if n_l[i] != -1:
            res.append(n_l[i])
        else:
            res.append(next(r_grab))
    
    res += [-1] * (len(n_l)-i_values)

    return res



import attrs

@attrs.define
class Block:
    index: int
    length: int
    start: int

def to_blocks(line):
    pos = 0

    blocks = []

    for i in range(0,len(line),2):
        index = i // 2
        blocks.append(Block(index, line[i], pos))

        pos += line[i]

        if i + 1 < len(line):
            blocks.append(Block(-1, line[i+1], pos))
            pos += line[i+1]

    return blocks

def get_first_block(blocks, largest, index) -> Block:
    for b in blocks[::-1]:
        if b.length <= largest and b.start > index and b.index != -1:
            return b

def from_blocks(blocks):
    d = []
    for b in blocks:
        d += [b.index] * b.length
    
    return d

def move_blocks(line):
    blocks = to_blocks(line)



    d = []
    
    i=0
    while i < len(blocks):

        b = blocks[i]
        
        if b.index != -1:
            d += [b.index] * line[i]
        else:
            if n_b:=get_first_block(blocks, b.length, i + 1):
                d += [n_b.index] * n_b.length
                d += [-1] * (b.length - n_b.length)
                blocks.remove(n_b)
            else:
                d += [-1] * b.length

        i += 1

    return d
import typing as tp
def try_insert(b: Block, bs: tp.List[Block]):
    i = 0
    while i < len(bs):
        cur_b = bs[i]
        if cur_b == b:
            return bs
        if cur_b.index == -1 and cur_b.length >= b.length:
            for j in range(len(bs)):
                if bs[j] == b:
                    bs[j].index = -1
            bs[i] = b

            if cur_b.length > b.length:
                new_b = Block(-1,cur_b.length-b.length,-1)
                bs.insert(i+1, new_b)
            return bs
        i += 1

import copy
def swap(blocks):
    n_b = copy.deepcopy(blocks)
    for i, block in enumerate(blocks[::-1]):
        if block.index != -1:
            try_insert(block, n_b)
    
    return n_b



# n = combine(line)
# tot = 0
# i = 0
# while n[i] != -1:
#     tot += n[i] * i
#     i+=1
# print(tot)

blocks = to_blocks(line)   
n_blocks = from_blocks(swap(blocks))

tot = 0
i = 0
for i, v in enumerate(n_blocks):
    if v != -1:
        tot += v * i
    i+=1
print(tot)