#################
# Assembunny Computer: as defined in AdventOfCode 2016 Days 12, 23, 25
#################
from copy import deepcopy
import time
#################
class Assembunny:

    def __init__(self, program, do_optimize=True):
        self.Registers = dict.fromkeys( ['a', 'b', 'c', 'd', 'IP', 'OUT'], 0 )
        self.program = [ s.split() for s in program.splitlines() ] if isinstance(program, str) else deepcopy(program)
        if isinstance(program, str) :
            self.program = [ s.split() for s in program.splitlines() ]
        self.do_optimize = do_optimize
        self.optimize()

    def reset(self) : 
        for r in self.Registers : self.Registers[r] = 0
        self.Registers['OUT'] = ''
    def get(self, reg) : return self.Registers[reg]
    def set(self, reg, value) : self.Registers[reg] = value

    # Define Computer: Registers and Instruction, then an ALU which can run a program
    def value_or_register(self, s) : return s if isinstance(s, int) else self.Registers[s]
    def cpy(self, x, y)   : self.Registers['IP'] += 1; self.Registers[y] = self.value_or_register(x)
    def inc(self, x)      : self.Registers['IP'] += 1; self.Registers[x] += 1
    def dec(self, x)      : self.Registers['IP'] += 1; self.Registers[x] -= 1
    def jnz(self, x, rel) : self.Registers['IP'] += self.value_or_register(rel) if self.value_or_register(x) != 0 else 1

    # Added for 2016 day 23
    ToggleMap = { 'inc' : 'dec', 'dec' : 'inc', 'tgl' : 'inc', 'jnz' : 'cpy', 'cpy' : 'jnz'}
    def tgl(self, x, prog) :
        instr = self.Registers['IP'] + self.value_or_register(x)
        self.Registers['IP'] += 1
        if instr < 0 or instr >= len(prog) : return
        prog[instr][0] = self.ToggleMap[prog[instr][0]]
        #print(f"Assembunny Toggled {instr}")
        #for i, l in enumerate(prog): print(i, l)
        self.optimize() # re-optimize the new program

    # Added for 2016 day 25
    def out(self, x) : self.Registers['IP'] += 1; self.Registers['OUT'] += f'{self.value_or_register(x)}'; return self.value_or_register(x)

    #######################################
    # Optimizer: add y to reg x -> reg x
    def add(self, x, y)      : self.Registers['IP'] += 1; self.Registers[x] += self.value_or_register(y)
    # Optimizer: multiply reg x by y -> reg x
    def mul(self, x, y)      : self.Registers['IP'] += 1; self.Registers[x] *= self.value_or_register(y)
    # Optimizer: do nothing -> not having to adjust jump offset if used to fill gaps after optimizing
    def nop(self)          : self.Registers['IP'] += 1

    # Find optimizations in programs (added for 2016 day 23 - performance...) :
    # - pre-compile numbers
    # - multiply-add : 
    #        inc reg1 / dec reg2 / jnz reg2 -2 / dec reg3 / jnz reg3 -5 
    #     => mul reg2 reg3 / add reg1 reg2 / cpy 0 reg2 / cpy 0 reg3 / nop
    # - add          : 
    #        inc a / dec b / jnz b -2 
    #     => add a b / cpy 0 b / nop
    def optimize(self) :
        # INTs -> pre-compile to numbers if not a register
        for instr in range(len(self.program)) :
            for attr_nr in range(1,len(self.program[instr])) :
                try: self.program[instr][attr_nr] = int(self.program[instr][attr_nr])
                except ValueError: pass
        
        if not self.do_optimize : return

        # Multipliy-add
        for i in range(len(self.program) - 4) :
            inc1, dec2, jnz2, dec3, jnz3 = self.program[i:i+5]
            if inc1[0] == 'inc' and dec2[0] == dec3[0] == 'dec' and jnz2[0] == jnz3[0] == 'jnz' \
                    and dec2[1] == jnz2[1] and dec3[1] == jnz3[1] \
                    and inc1[1] != dec2[1] and dec3[1] != dec2[1]\
                    and jnz2[2] == -2 and jnz3[2] == -5 :
                self.program[i]   = ['mul', dec2[1], dec3[1]]
                self.program[i+1] = ['add', inc1[1], dec2[1]]
                self.program[i+2] = ['cpy', 0, dec2[1]]
                self.program[i+3] = ['cpy', 0, dec3[1]]
                self.program[i+4] = ['nop',]
                #print(f"Optimizer MULT at", i)
        # Add
        for i in range(len(self.program) - 2) :
            inc1, dec2, jnz2 = self.program[i:i+3]
            if inc1[0] == 'inc' and dec2[0] == 'dec' and jnz2[0] == 'jnz' \
                    and dec2[1] == jnz2[1] \
                    and inc1[1] != dec2[1] \
                    and jnz2[2] == -2 :
                self.program[i]   = ('add', inc1[1], dec2[1])
                self.program[i+1] = ('cpy', 0, dec2[1])
                self.program[i+2] = ('nop',)
                #print(f"Optimizer ADD at", i)

    #######################################
    def run(self, break_on_output=lambda:False) :
        start = time.time()
        count = 0
        while self.Registers['IP'] < len(self.program) :
            instruction, *operands = self.program[self.Registers['IP']]
            if instruction == 'tgl' : operands.append(self.program)
            ret = getattr(self, instruction)(*operands)
            count += 1
            # If output was added: run the verify function to check for break condition
            if ret != None and break_on_output(self) : 
                return self.Registers['OUT']
        used = time.time() - start
        print (f"Assembunny hopped {count:,d} times ({count / used / 1E6:.2f} MHops)")

#############
if __name__ == '__main__' :

    # as array
    p_add = [
        ['cpy', 2, 'a'],
        ['cpy', 40,  'b'],
        ['inc', 'a'],
        ['dec', 'b'],
        ['jnz', 'b', -2],
    ]

    # as string
    p_mul = '''cpy 2 a
cpy 5 d
cpy 8 c
inc a
dec c
jnz c -2
dec d
jnz d -5
'''

    for p in (p_add, p_mul) :
        for optimize in (True, False) :
            bunny   = Assembunny(p, do_optimize=optimize)
            bunny.run()
            assert bunny.get('a') == 42

