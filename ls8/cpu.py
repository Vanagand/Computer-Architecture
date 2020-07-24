import sys

# python .\cpu.py examples\print8.ls8
# python .\ls8.py examples\print8.ls8
# python .\ls8.py examples\mult.ls8
# python .\ls8.py examples\stack.ls8
# python .\ls8.py examples\sctest.ls8

"""Operations table."""

# ALU Operations
# ADD  = 0b10100000                                                            DONE
# SUB  = 0b10100001                                                            DONE
# MUL  = 0b10100010                                                            DONE
# DIV  = 0b10100011                                                            DONE
# MOD  = 0b10100100                                                            DONE

# INC  = 0b01100101                                                            DONE
# DEC  = 0b01100110                                                            DONE

# CMP  = 0b10100111                                                            DONE

# AND  = 0b10101000                                                            DONE
# NOT  = 0b01101001                                                            DONE
# OR   = 0b10101010                                                            DONE
# XOR  = 0b10101011                                                            DONE
# SHL  = 0b10101100                                                            DONE
# SHR  = 0b10101101                                                            DONE

# PC Mutators
# CALL = 0b01010000                                                            DONE
# RET  = 0b00010001                                                            DONE

# INT  = 0b01010010                                                            #>>>
# IRET = 0b00010011                                                            #>>>

# JMP  = 0b01010100                                                            #>>>
# JEQ  = 0b01010101                                                            #>>>
# JNE  = 0b01010110                                                            #>>>
# JGT  = 0b01010111                                                            #>>>
# JLT  = 0b01011000                                                            #>>>
# JLE  = 0b01011001                                                            #>>>
# JGE  = 0b01011010                                                            #>>>

# Other
# NOP  = 0b00000000

# HLT  = 0b00000001                                                            DONE

# LDI  = 0b10000010                                                            #>>>

# LD   = 0b10000011                                                            #>>>
# ST   = 0b10000100                                                            #>>>

# PUSH = 0b01000101                                                            DONE
# POP  = 0b01000110                                                            DONE

# PRN  = 0b01000111                                                            DONE
# PRA  = 0b01001000                                                            #>>>

"""CPU functionality."""

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.PC = 0b00000000
        self.FL = 0b00000000
        self.running = True
        self.configure_branchtable()

        self.IM = 5 # interrupt mask
        self.reg[self.IM] = 0b00000000                                         #>>> TODO
        self.IS = 6 # interrupt status
        self.reg[self.IS] = 0b00000000                                         #>>> TODO
        self.SP = 7 # stack pointer
        self.reg[self.SP] = 0xF4
        
    def configure_branchtable(self):
        self.branchtable = {}
        self.branchtable[0b01010000] = self.handle_CALL
        self.branchtable[0b00010001] = self.handle_RET
        # self.branchtable[0b01010010] = self.handle_INT                       #>>> TODO
        # self.branchtable[0b00010011] = self.handle_IRET                      #>>> TODO
        self.branchtable[0b01010100] = self.handle_JMP
        self.branchtable[0b01010101] = self.handle_JEQ
        self.branchtable[0b01010110] = self.handle_JNE
        self.branchtable[0b01010111] = self.handle_JGT
        self.branchtable[0b01011000] = self.handle_JLT
        self.branchtable[0b01011001] = self.handle_JLE
        self.branchtable[0b01011010] = self.handle_JGE
        self.branchtable[0b00000000] = self.handle_NOP
        self.branchtable[0b00000001] = self.handle_HLT
        self.branchtable[0b10000010] = self.handle_LDI
        # self.branchtable[0b10000011] = self.handle_LD                        #>>> TODO
        # self.branchtable[0b10000100] = self.handle_ST                        #>>> TODO
        self.branchtable[0b01000101] = self.handle_PUSH
        self.branchtable[0b01000110] = self.handle_POP
        self.branchtable[0b01000111] = self.handle_PRN
        # self.branchtable[0b01001000] = self.handle_PRA                       #>>> TODO
    
    # Branchtable operations
    def handle_CALL(self, reg_num):
        """Calls a subroutine at the address stored in reg_a."""
        print(f"Handling CALL operation!")
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.PC+2
        self.PC = self.reg[reg_num]
    def handle_RET(self):
        """Return from subroutine."""
        print(f"Handling RET operation!\n")
        self.PC = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1 
    def handle_INT(self):                                                      #>>> TODO
        pass 
    def handle_IRET(self):                                                     #>>> TODO
        pass
    def handle_JMP(self, reg_num): # 0b01010100 <NOTE>
        """Jump to the address stored in the given register."""                # 00000LGE (Less-than, Greater-than, Equal)
        print(f"Moving. JMP!\n")
        self.PC = self.reg[reg_num]
    def handle_JEQ(self, reg_num): # 0b01010101 <NOTE>
        """If E flag is True, jump to the address stored in the given register."""
        print(f"Moving. JEQ!\n") 
        if (self.FL & 0b00000001) > 0:
            self.PC = self.reg[reg_num]
        else:
            self.PC += 2
    def handle_JNE(self, reg_num): # 0b01010110 <NOTE>
        """If E flag is False, jump to the address stored in the given register."""
        print(f"Moving. JNE!\n") 
        if (self.FL & 0b00000001) == 0:
            self.PC = self.reg[reg_num]
        else:
            self.PC += 2
    def handle_JGT(self, reg_num): # 0b01010111
        """If G flag is False, jump to the address stored in the given register."""
        print(f"Moving. JGT!\n") 
        if (self.FL & 0b00000010) == 0:
            self.PC = self.reg[reg_num]
        else:
            self.PC += 2
    def handle_JLT(self, reg_num): # 0b01011000
        """If L flag is True, jump to the address stored in the given register."""
        print(f"Moving. JLT!\n") 
        if (self.FL & 0b00000100) > 0:
            self.PC = self.reg[reg_num]
        else:
            self.PC += 2
    def handle_JLE(self, reg_num): # 0b01011001
        """If L OR E flags are True, jump to then adddress in the given register."""
        print(f"Moving. JLE!\n") 
        if (self.FL & 0b00000101) > 0:
            self.PC = self.reg[reg_num]
        else:
            self.PC += 2
    def handle_JGE(self, reg_num): # 0b01011010
        """If G OR E flags are True, jump to the address stored in the given register."""
        print(f"Moving. JGE!\n") 
        if (self.FL & 0b00000011) > 0:
            self.PC = self.reg[reg_num]
        else:
            self.PC += 2
    def handle_NOP(self):
        pass 
    def handle_HLT(self):
        print("Handling HLT operation!")
        self.running = False
    def handle_LDI(self, reg_num, input):
        self.reg[reg_num] = input
        print(f"Handling LDI operation! R{reg_num},{input}\n")
    def handle_LS(self):                                                       #>>> TODO
        pass
    def handle_ST(self):                                                       #>>> TODO
        pass
    def handle_PUSH(self, reg_num):
        # decrement stack pointer
        print(f"Handling PUSH operation! R{reg_num}\n")
        self.ram_write(self.reg[self.SP], self.reg[reg_num])
        self.SP -= 1
    def handle_POP(self, reg_num):
        # increment stack pointed
        print(f"Handling POP operation! R{reg_num}\n")
        self.reg[reg_num] = self.ram_read(self.reg[self.SP+1])
        self.SP += 1
    def handle_PRN(self, reg_num):
        print(f"Handling PRN operation! R{reg_num}      >>> {self.reg[reg_num]}\n")
    def handle_PRA(self):                                                      #>>> TODO
        pass
        
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
        if op == 0b10100000:
            """Add the value from reg_a and reg_b, and store the result into reg_a"""
            print(f"ADD R0,({self.reg[0]}+{self.reg[1]})\n")
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 0b10100001:
            """Substract the value from reg_a and reg_b, and store the result into reg_a"""
            print(f"SUB R0,({self.reg[0]}-{self.reg[1]})\n")
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 0b10100010:
            """Multiplies the value from reg_a and reg_b, and store the result into reg_a"""
            print(f"MUL R0,({self.reg[0]}*{self.reg[1]})\n")
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 0b10100011:
            """Divides the value from reg_a and reg_b, and store the result into reg_a"""
            print(f"DIV R0,({self.reg[0]}/{self.reg[1]})\n")
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 0b10100100:
            """Divides the value from reg_a and reg_b, and store the remainder into reg_a"""
            print(f"MOD R0,({self.reg[0]}%{self.reg[1]})\n")
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 0b01100101:
            """Increments the given register by 1"""
            print(f"INC R0,({self.reg[0]}+1)\n")
            self.reg[reg_a] += 1
        elif op == 0b01100110:
            """Decreases the given register by 1"""
            print(f"DEC R0,({self.reg[0]}-1)\n")
            self.reg[reg_a] -= 1
        elif op == 0b10100111: # 0b00000LGE <NOTE>
            """Compares the values of reg_a and reg_b."""
            self.FL = 0b00000000
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL += 0b00000001
                print(f"Handling CMP! R0,{self.reg[0]} == R1,{self.reg[1]}\n0b{self.FL:b}\n")
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL += 0b00000010
                print(f"Handling CMP! R0,{self.reg[0]} < R1,{self.reg[1]}\n0b{self.FL:b}\n")
            if self.reg[reg_a] > self.reg[reg_b]:
                self.FL += 0b00000100
                print(f"Handling CMP! R0,{self.reg[0]} > R1,{self.reg[1]}\n0b{self.FL:b}\n")
        elif op == 0b10101000:
            """Bitwise-AND from reg_a and reg_b, and store the result into reg_a"""
            print(f"AND\n")
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 0b01101001:
            """Bitwise-NOT from reg_a and reg_b, and store the result into reg_a"""
            print(f"NOT\n")
            self.reg[reg_a] = ~ self.reg[reg_a]
        elif op == 0b10101010:
            """Bitwise-OR from reg_a and reg_b, and store the result into reg_a"""
            print(f"OR\n")
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 0b10101011:
            """Bitwise-XOR from reg_a and reg_b, and store the result into reg_a"""
            print(f"XOR\n")
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == 0b10101100:
            """Shift the value in reg_a left by the number of bits specified in reg_b, filling the low bits with 0."""
            print(f"SHL\n")
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 0b10101101:
            """Shift the value in reg_a right by the number of bits specified in reg_b, filling the high bits with 0."""
            print(f"SHR\n")
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        else:
            raise Exception("Unknown ALU operation.")

###
###
###

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
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
            IR = self.ram[self.PC]
            reg_a = self.ram[self.PC + 1]
            reg_b = self.ram[self.PC + 2]

            if IR == 0b00000001: # HLT
                self.branchtable[IR]()
            elif IR == 0b10000010: # LDI
                self.branchtable[IR](reg_a, reg_b)
                self.PC += 3
            elif IR == 0b01000111: # PRN
                self.branchtable[IR](reg_a)
                self.PC += 2
            elif IR == 0b10100000: # ADD
                self.alu(0b10100000, reg_a, reg_b)
                self.PC += 3
            elif IR == 0b10100001: # SUB
                self.alu(0b10100001, reg_a, reg_b)
                self.PC += 3
            elif IR == 0b10100010: # MUL
                self.alu(0b10100010, reg_a, reg_b)
                self.PC += 3
            elif IR == 0b10100011: # DIV
                self.alu(0b10100011, reg_a, reg_b)
                self.PC += 3
            elif IR == 0b10100111: # CMP <NOTE>
                self.alu(0b10100111, reg_a, reg_b)
                self.PC += 3
            elif IR == 0b01000101: # PUSH
                self.branchtable[IR](reg_a)
                self.PC += 2
            elif IR == 0b01000110: # POP
                self.branchtable[IR](reg_a)
                self.PC += 2
            elif IR == 0b01010000: # CALL
                self.branchtable[IR](reg_a)
            elif IR == 0b00010001: # RET
                self.branchtable[IR]()
            elif IR == 0b01010100: # JMP
                self.branchtable[IR](reg_a) # <NOTE>
            elif IR == 0b01010101: # JEQ
                self.branchtable[IR](reg_a) # <NOTE>
            elif IR == 0b01010110: # JNE
                self.branchtable[IR](reg_a) # <NOTE>
            elif IR == 0b01010111: # JGT
                self.branchtable[IR](reg_a)
            elif IR == 0b01011000: # JLT
                self.branchtable[IR](reg_a)
            elif IR == 0b01011001: # JLE
                self.branchtable[IR](reg_a)
            elif IR == 0b01011010: # JGE
                self.branchtable[IR](reg_a)
            elif IR == 0b00000000: # NOP
                self.branchtable[IR]()
            else:
                print(f"Unkown instruction {IR}")
                self.handle_HLT()
