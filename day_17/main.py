import attrs
import typing as tp

@attrs.define
class Comp:
    instr: tp.List[int]
    reg_a: int
    reg_b: int
    reg_c: int
    output: tp.Optional[tp.List[int]] = None
    i: int = 0

    def combo(self, com):
        if 0 <= com <= 3:
            return com
        
        if com == 4:
            return self.reg_a
        
        if com == 5:
            return self.reg_b
        
        if com == 6:
            return self.reg_c
        
        raise ValueError

    def adv(self, com):
        num = self.reg_a
        denom = 2 ** self.combo(com)

        self.reg_a = int(num // denom)

    def bxl(self, com):
        self.reg_b = self.reg_b ^ com
    
    def bst(self, com):
        self.reg_b = self.combo(com) % 8

    def jnz(self, com):
        if self.reg_a == 0:
            pass
        else:
            self.i = com - 2

    def bxc(self, com):
        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, com):
        num = self.combo(com) % 8
        self.output.append(num)
        if self.output[len(self.output) - 1] != self.instr[min(len(self.output), len(self.instr)) - 1]:
            return "exit"

    def bdv(self, com):
        num = self.reg_a
        denom = 2 ** self.combo(com)

        self.reg_b = int(num // denom)   

    def cdv(self, com):
        num = self.reg_a
        denom = 2 ** self.combo(com)

        self.reg_c = int(num // denom)

    op_map = [
        adv,
        bxl,
        bst,
        jnz,
        bxc,
        out,
        bdv,
        cdv
    ]

    def exe(self, A, v = False):
        self.output = []
        self.i = 0
        self.reg_a = A
        self.reg_b = 0
        self.reg_c = 0

        while self.i < len(self.instr)-1:
            op = self.instr[self.i]
            com = self.instr[self.i+1]

            if v:
                print(self)
                print(f"{self.op_map[op].__name__}, {com}")

            res = self.op_map[op](self, com)
            # if res == "exit":
            #     return False
            
            self.i += 2

        return self.output # == self.instr
        

tst = Comp(
    [0,3,5,4,3,0],
    0,
    0,
    0
)

# print(tst.exe(117440))

def find_brute(c: Comp):
    i = 0
    while True:
        if c.exe(i):
            return i
        # print(i)
        i += 1




p1 = Comp(
    [2,4,1,1,7,5,1,5,4,5,0,3,5,5,3,0],
    0,
    0,
    0
)

# bst, 4: b = a % 8
# bxl, 1: b = b ^ 1
# cdv, 5: c = a << b
# bxl, 5: b = b ^ 5
# bxc, 5: b = b ^ c
# adv, 3: a = a << 3
# out, 5: out += b % 8
# jnz, 0: if a == 0 restart

# b = last three digits of a +- 1 (deterministic)

# i = 519000000
# while not p1.exe(i):
#     if i % 1000000 == 0:
#         print(i)
#     i += 1

print(f"max 16 dig {2 ** (3*16) - 1}")
print(f"min 16 dig {2 ** (3*15)}")
print(p1.exe(140737488355328))
print(p1.exe(35184372088832))

vals = {0}
for l in range(len(p1.instr)):
    base_vals = set(map(lambda x: x * 8, vals))
    print(f"level {l}")
    vals = set()
    for i in range(8):
        for v in base_vals:
            val = v + i
            if p1.instr[-(l+1)] == p1.exe(val)[-(l+1)]:
                vals.add(val)

print(min(vals))

print(p1.exe(164540892147389))
a = 0