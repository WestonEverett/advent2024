with open(r"day_2\data.txt") as file:
    lines = [l.strip() for l in file]


def check_line(l):
    return sum([1 for x,y in zip(l[1:], l[:-1]) if not((int(x)-int(y)) >= 1 and (int(x)-int(y)) <= 3)]) == 0 or sum([1 for y,x in zip(l[1:], l[:-1]) if not ((int(x)-int(y)) >= 1 and (int(x)-int(y)) <= 3)]) == 0

def check_line_2(l):

    if check_line(l): return True

    for i in range(len(l)):
        if check_line(l[:i] + l[i+1:]): return True

    return False

total = 0
for l in lines:
    l = l.split(" ")

    if check_line_2(l):
        total+=1

print(total)