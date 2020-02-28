"""CPU functionality."""

import sys

# Hardcoding variables for branch table
LDI = 0b10000010 # LDI R0, 8
PRN = 0b01000111 # PRN R0
HLT = 0b00000001 # HLT
ADD = 0b10100000
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7  # Stack Pointer (SP) Register 7


class CPU: 
    """Main CPU Class."""

    def __init__(self):
        """Construct a New CPU.""" 
         # 256 Bytes of Mem with 8 GPRs
        self.ram = [0] * 256 # 256 Bytes of Mem for Instructions
        self.reg = [0] * 8 # 8 GPRs (General-Purpose Registers)
        self.pc = 0 # Helps Distinguish b/w Operands and Instructions
        self.reg[7] = 255
        self.sp = self.reg[7]
        self.flag = None

        def ram_read(self, MAR):
            return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a Program into Memory."""

        address = 0

        with open(filename) as file:
            for line in file:
                command_split = line.split('#')
                instruction = command_split[0]

                if instruction == "":
                    continue

                bit_One = instruction[0]

                if bit_One == '0' or bit_One == '1':
                    self.ram[address] = int(instruction[:8], 2) # convert instructions to binary
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations. Arithetic logic unit"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        A Handy Function to Print out the CPU State. You might want to call this
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

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            command = self.ram_read(self.pc) # get instructions

            op_A = self.ram_read(self.pc + 1) # Reg Location
            op_B = self.ram_read(self.pc + 2) # Value

            op_Size = int(command) >> 6 # Get Operand Size by Shifting Six
            self.pc += (1 + op_Size)

            if command == LDI:
                self.reg[op_A] = op_B
                # self.pc += 3
            
            elif command == PRN:
                op_A = self.ram[self.pc + 1]
                print(self.reg[op_A])
                # self.pc += 2

            elif command == MUL:
                self.alu("MUL", op_A, op_B)
                # self.pc += 3

            elif command == HLT:
                running = False

            elif command == PUSH:
                self.sp = (self.sp % 257) - 1
                self.ram[self.sp] = self.reg[op_A]
                # self.pc += 2
            
            elif command == POP:
                self.reg[op_A] = self.ram[self.sp]
                self.sp = (self.sp % 257) + 1
                # self.pc += 2
            
            elif command == CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2

            elif command == RET:
                self.pc = self.ram[self.sp]
            
            # Compare
            elif command == CMP:
                self.alu("CMP", op_A, op_B)

            # Jump to PC Address
            elif command == JMP:
                self.pc = self.reg[op_A]
            
            # Jump if Equal
            elif command == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.reg[op_A]

            # Jump if Not Equal
            elif command == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.reg[op_A]