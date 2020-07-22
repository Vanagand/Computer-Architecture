# python .\cpu.py examples\print8.ls8
# python .\ls8.py examples\print8.ls8
# python .\ls8.py examples\mult.ls8
# python .\ls8.py examples\stack.ls8

"""CPU functionality."""

import sys

# ALU Operations
ADD  = 0b10100000
SUB  = 0b10100001
MUL  = 0b10100010
DIV  = 0b10100011
# MOD  = 0b10100100

# INC  = 0b01100101
# DEC  = 0b01100110

# CMP  = 0b10100111

# AND  = 0b10101000
# NOT  = 0b01101001
# OR   = 0b10101010
# XOR  = 0b10101011
# SHL  = 0b10101100
# SHR  = 0b10101101

# PC Mutators
# CALL = 0b01010000
# RET  = 0b00010001

# INT  = 0b01010010
# IRET = 0b00010011

# JMP  = 0b01010100
# JEQ  = 0b01010101
# JNE  = 0b01010110
# JGT  = 0b01010111
# JLT  = 0b01011000
# JLE  = 0b01011001
# JGE  = 0b01011010

# Other
# NOP  = 0b00000000

HLT  = 0b00000001 

LDI  = 0b10000010

# LD   = 0b10000011
# ST   = 0b10000100

PUSH = 0b01000101
POP  = 0b01000110

PRN  = 0b01000111
# PRA  = 0b01001000


"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.configure_branchtable()
        
        SP = 7
        self.reg[SP] = 0xF4
        
    def configure_branchtable(self):
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[PRN] = self.handle_PRN
    
    # Branchtable operations
    def handle_HLT(self):
        print("Handling HLT operation!")
        self.running = False
    def handle_LDI(self, reg_num, input):
        self.reg[reg_num] = input
        print(f"Handling LDI operation! R{reg_num},{input}\n")
    def handle_PUSH(self, reg_num):
        # decrement stack pointer
        print(f"Handling PUSH operation! R{reg_num}\nPASS\n")
        self.reg[7] -= 1
    def handle_POP(self, reg_num):
        # increment stack pointed
        print(f"Handling POP operation! R{reg_num}\nPASS\n")
        pass
    def handle_PRN(self, reg_num):
        print(f"Handling PRN operation! R{reg_num}\n{self.reg[reg_num]}\n")
        
###
###
###

    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, address, value):
        self.ram[address] = value
    # @property
    # def ram(self):
    #     return self.ram
    # @ram.setter
    # def ram(self, x):
    #     self.ram = x
        
###
###
###

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("Invalid input: .\cpu.py filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#", 1)[0]
                        self.ram[address] = int(line, 2)
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Coudn't find file {sys.argv[1]}")
            sys.exit(1)

###
###
###

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            pass
        elif op == "INC":
            pass
        elif op == "DEC":
            pass
        elif op == "CMP":
            pass
        elif op == "AND":
            pass
        elif op == "NOT":
            pass
        elif op == "OR":
            pass
        elif op == "XOR":
            pass
        elif op == "SHL":
            pass
        elif op == "SHR":
            pass
        else:
            raise Exception("Unsupported ALU operation")

###
###
###

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

###
###
###

    def run(self):
        """Run the CPU."""
        self.load()
        
        while self.running:
            IR = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]
            
            # HLT, LDI, PRN, MUL
            if IR == HLT:
                # print(f"Running operation {IR}")
                self.branchtable[IR]()
            elif IR == LDI:
                # print(f"Running operation {IR}")
                self.branchtable[IR](reg_a, reg_b)
                self.pc += 3
            elif IR == PRN:
                # print(f"Running operation {IR}")
                self.branchtable[IR](reg_a)
                self.pc += 2
            elif IR == MUL:
                # print(f"Running operation {IR}")
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3
            elif IR == PUSH:
                # print(f"Running operation {IR}")
                self.branchtable[IR](reg_a)
                self.pc += 2
            elif IR == POP:
                # print(f"Running operation {IR}")
                self.branchtable[IR](reg_a)
                self.pc += 2         
            else:
                print(f"Unkown instruction {IR}")
                self.handle_HLT()
