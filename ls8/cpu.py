"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # step 1
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
    
    def ram_read(self, mem_address):
        # takes an address (mem_address) in ram and returns the value (mem_value) stored there
        mem_value = self.ram[mem_address]
        return mem_value

    def ram_write(self, mem_value, mem_address):
        # stores mem_value at given mem_address in ram
        self.ram[mem_address] = mem_value

    def load(self):
        """Load a program into memory."""
        # counter
        address = 0

        # open ls8 file
        with open(sys.argv[1]) as f:
            # read each line
            for line in f:
                #split on # to remove comments and empty spaces
                line_value = line.split("#")[0].strip()
                if line_value == '':
                    continue
                # convert to int (base 2 binary) and save to ram at address
                value = int(line_value, 2)
                self.ram[address] = value
                #increment address counter
                address += 1

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
            # self.ram[address] = instruction
            # address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # read memory address stored in pc and store result in opcode
            ir = self.ram_read(self.pc)
            # Read values at PC+1 into operand_a and PC+2 into operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # LDI command
            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc +=3  
                
            elif ir == PRN:
                # read value at PC+1 into operand_a
                prn_reg = self.ram[self.pc + 1]
                print(self.reg[prn_reg])
                self.pc += 2

            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
                self.pc += 3

            elif ir == HLT:
                running = False
            
            else:
                print('Unknown Command')
                running = False

