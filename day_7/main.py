with open(r"day_7\data.txt") as file:
    lines = [l.strip() for l in file] 

data = []
for l in lines:
    c = l.split(":")
    a = int(c[0])
    b = [int(b_0) for b_0 in c[1].strip().split(" ")]
    data.append((a,b))

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def con(a, b):
    return int(str(a)+str(b))

def check_possible(tar, vals):
    if len(vals) == 1:
        if vals[0] == tar:
            return True 
        return False
    
    if vals[0] > tar:
        return False
    
    flag = False
    for func in [add, mul, con]:
        new_vals = [func(vals[0], vals[1])] + vals[2:]
        if check_possible(tar, new_vals):
            flag = True
        
    return flag

tot = 0
for a, b in data:
    if check_possible(a, b):
        tot += a
print(tot)