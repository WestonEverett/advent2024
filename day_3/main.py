import regex

with open(r"day_3\data.txt") as file:
    lines = [l.strip() for l in file]

full_str = ''.join(lines)

mul_pat = r"(?P<type>mul)\((?P<arg_1>\d{1,3})\,(?P<arg_2>\d{1,3})\)"
do_pat = r"(?P<type>do)\(\)"
dont_pat = r"(?P<type>don\'t)\(\)"

reg = regex.compile(f"(?:{mul_pat}|{do_pat}|{dont_pat})")

tot = 0
active = True
for m in reg.finditer(string=full_str): 
    if m["type"] == "do":  
        active = True
    
    if m["type"] == "don't":
        active = False

    if m["type"] == "mul" and active:
        tot += int(m["arg_1"]) * int(m["arg_2"])

print(tot)
