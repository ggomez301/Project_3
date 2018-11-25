""""""
Team: 15
Guillermo Gomez / Lucia Sorto
Due Date: 10/31/2018
Instructor: Prof. Greg Lakomski
""""""
#!usr/bin/env
import sys
import os

instructions = []
reglist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
opcode = []
opname = []
memory = []
opformat = []
address = []
arg1 = []
arg2 = []
arg3 = []
instcount = 0
dest = []
src1 = []
src2 = []
cycle = 0
PC = 96



class Dissassemble:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC

    def run(self):

        for i in range (len (sys.argv)):
            if (sys.argv[i] == '-i' and i < (len (sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
            elif (sys.argv[i] == '-o' and i < (len (sys.argv) - 1)):
                outputFileName = sys.argv[i + 1] + "_dis.txt"

        output = open(outputFileName, "w+")

        instructions = [line.rstrip() for line in
                            open(inputFileName, 'rb')]

        address[0] = 96

        for i in range(len(instructions)):
            line = instructions[i]
            first_eleven = line[:11]
            first_eleven_int = int(first_eleven)

            opcode.append(first_eleven_int)
            self.getFormat(line, output)
            i_count++
            address[i_count] = address[i_count - 1] + 4

    def binToDec(self, x):
        decNum = 0
        power = 0
        while x > 0:
            decNum += 2 ** power * (x % 10)
            x //= 10
            power += 1
        return decNum

    def getFormat(self, line, output):
        check_nop = int(line[1:32])
        check_nop_dec = binToDec(check_nop)

        if opCode[i_count] == 1104 or opCode[i_count] == 1112 or opCode[i_count] == 1360 or opCode[i_count] == 1624:
            self.rFormat(line, output)
        elif opCode[i_count] == 1690 or opCode[i_count] == 1691 or opCode[i_count] == 1872 or check_nop_dec == 0:
            self.rFormat(line, output)
        elif opCode[i_count] == 1692:
            self.rFormat(line, output)
        elif opCode[i_count] == 1160 or opCode[i_count] == 1161 or opCode[i_count] == 1672 or opCode[i_count] == 1673:
            self.iFormat(line, output)
        elif opCode[i_count] == 1984 or opCode[i_count] == 1986:
            self.dFormat(line, output)
        elif opCode[i_count] >= 160 and opCode[i_count] <= 191:
            self.bFormat(line, output)
        elif (opCode[i_count] >= 1440 and opCode[i_count] <= 1447) or (opCode[i_count] >= 1148 and opCode[i_count] <= 1455):
            self.cbFormat(line, output)
        elif (opCode[i_count] >= 1684 and opCode[i_count] <= 1687) or (opCode[i_count] >= 1940 and opCode[i_count] <= 1943):
            self.iwFormat(line, output)
        elif opCode[i_count] == 2038:
            self.Break(line, output)
        else:
            self.twosComplement(line, output)

    def rFormat(self, line, output):
        alu_imm = line[11:22]
        Rm = line[12:16]
        shamt = line[17:22]
        Rn = line[23:27]
        Rd = line[28:32]

        Rm_int = int(Rm)
        shamt_int = int(shamt)
        Rn_int = int(Rn)
        Rd_int = int(Rd)

        opformat.append('R')
        Rm_dec = self.binToDec(Rm_int)
        shamt_dec = self.binToDec(shamt_int)
        Rn_dec = self.binToDec(Rn_int)
        Rd_dec = self.binToDec(Rd_int)

        arg1.append(Rd_dec)
        arg2.append(Rn_dec)
        arg3.append(Rm_dec)

        alu_imm_int = int(alu_imm)
        alu_imm_offset = self.binToDec(alu_imm_int)

        src1.append(alu_imm_offset)

        #### fill other lists ####
        src2.append(0)

        check_nop = int(line[1:32])
        check_nop_dec = self.binToDec(check_nop)

        if opCode[i_count] == 1112:
            opname.append('ADD')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" +  \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", R" + str(Rm_dec) + "\n")
        elif opCode[i_count] == 1624:
            opname.append('SUB')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", R" + str(Rm_dec) + "\n")
        elif opCode[i_count] == 1104:
            opname.append('AND')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", R" + str(Rm_dec) + "\n")
        elif opCode[i_count] == 1360:
            opname.append('ORR')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", R" + str(Rm_dec) + "\n")
        elif opCode[i_count] == 1690:
            opname.append('LSR')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opName + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", #" + str(alu_imm_offset) + "\n")
        elif opCode[i_count] == 1691:
            opname.append('LSL')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opName + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", #" + str(alu_imm_offset) + "\n")
        elif opCode[i_count] == 1692:
            opname.append('ASR')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", #" + str(alu_imm_offset) + "\n")
        elif opCode[i_count] == 1872:
            opname.append('EOR')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opName + "\t" + "R" + \
                str(Rd_dec) + ", R" + str(Rn_dec) + ", R" + str(Rm_dec) + "\n")
        elif check_nop_dec == 0:
            opname.append('NOP')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\n")

    def iFormat(self, line, output):
        alu_imm = line[10:22]
        Rn = line[22:27]
        Rd = line[27:32]

        alu_imm_int = int(alu_imm)
        Rn_int = int(Rn)
        Rd_int = int(Rd)

        opformat.append('I')
        alu_imm_offset = self.binToDec(alu_imm_int)
        Rn_dec = self.binToDec(Rn_int)
        Rd_dec = self.binToDec(Rd_int)

        arg1.append(Rd_dec)
        arg2.append(Rn_dec)

        #### fill other lists ####
        dest.append(0)
        src1.append(0)
        src2.append(0)

        if (alu_imm_offset & (1 << (len(alu_imm) - 1))) != 0:
            alu_imm_offset = alu_imm_offset - (1 << len(alu_imm))

        arg3.append(alu_imm_offset)

        if opCode[i_count] == 1160 or opCode[i_count] == 1161:
            opname.append('ADDI')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", #" + str(alu_imm_offset[i_count]) + "\n")
        elif opCode[i_count] == 1672 or opCode[i_count] == 1673:
            opname.append('SUBI')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" \
                + str(Rd_dec) + ", R" + str(Rn_dec) + ", #" + str(alu_imm_offset) + "\n")

    def dFormat(self, line, output):
        dt_addr = line[12:20]
        Rn = line[23:27]
        Rt = line[28:32]

        dt_addr_int = int(dt_addr)
        Rn_int = int(Rn)
        Rt_int = int(Rt)

        opformat.append('D')
        addr_offset = self.binToDec(dt_addr_int)
        Rn_dec = self.binToDec(Rn_int)
        Rt_dec = self.binToDec(Rt_int)

        arg1.append(Rt_dec)
        arg2.append(Rn_dec)
        arg3.append(addr_offset)

        #### fill other lists ####
        dest.append(0)
        src1.append(0)
        src2.append(0)


        if opcode == 1984:
            opname.append('STUR')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
            str(Rt_dec) + ", [R" + str(Rn_dec) + ", #" + str(dt_addr_offset) + "]" + "\n")
        elif opcode == 1986:
            opname.append('LDUR')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
            str(Rt_dec) + ", [R" + str(Rn_dec) + ", #" + str(dt_addr_offset) + "]" + "\n")

    def bFormat(self, line, output):
        br_addr = line[7:32]

        br_addr_int = int(br_addr)

        opformat.append('B')
        addr_offset = self.binToDec(br_addr_int)


        #### fill other lists ####
        arg1.append(0)
        arg2.append(0)
        arg3.append(0)
        src1.append(0)
        src2.append(0)

        if (addr_offset & (1 << (len(br_addr) - 1))) != 0:
            br_addr_offset = br_addr_offset - (1 << len(br_addr))

        dest.append(br_addr_offset)

        if opCode[i_count] >= 160 and opCode[i_count] <= 191:
            opname.append('B')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "#" + \
                str(br_addr_offset) + "\n")

    def cbFormat(self, line, output):
        cond_br_addr = line[7:27]
        Rt = line[27:32]

        cond_br_addr_int = int(cond_br_addr)
        Rt_int = int(Rt)

        opformat.append('CB')
        addr_offset = self.binToDec(cond_br_addr_int)
        Rt_dec = self.binToDec(Rt_int)

        arg1.append(Rt_dec)

        #### fill other lists ####
        arg2.append(0)
        arg3.append(0)
        src1.append(0)
        src2.append(0)

        if (addr_offset & (1 << (len(cond_br_addr) - 1))) != 0:
            addr_offset = addr_offset - (1 << len(cond_br_addr))

        dest.append(addr_offset)

        if opcode >= 1440 and opcode <= 1447:
            opname.append('CBZ')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rt_dec) + ", " + "#" + str(addr_offset) + "\n")

        elif opCode[i_count] >= 1448 and opCode[i_count] <= 1455:
            opname.append('CBNZ')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
                str(Rt_dec) + ", " + "#" + str(addr_offset) + "\n")

    def iwFormat(self, line, output):
        mov_imm = line[12:27]
        mov_imm_k = line[11:27]
        Rd = line[28:32]
        shift_bits = line[9:11]

        opformat.append('IW')
        mov_imm_int = int(mov_imm)
        mov_imm_int_k = int(mov_imm_k)
        Rd_int = int(Rd)
        shift_bits_int = int(shift_bits)

        iw_mov_imm_dec = self.binToDec(mov_imm_int)
        iw_mov_imm_dec_k = self.binToDec(mov_imm_int_k)
        Rd_dec = self.binToDec(Rd_int)
        iw_shift_bits_dec = self.binToDec(shift_bits_int)
        iw_shift_amount = iw_shift_bits_dec * 16

        arg1.append(Rd_dec)
        src1.append(iw_mov_imm_dec)
        src2.append(iw_mov_imm_dec_k)
        dest.append(iw_shift_amount)

        #### fill other lists ####
        arg2.append(0)
        arg3.append(0)


        if opcode >= 1684 and opcode <= 1687:
            opname.append('MOVZ')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address) + "\t" + opname + "\t" + "R" + \
            str(Rd_dec) + ", " + str(iw_mov_imm_dec) + ", LSL " + str(iw_shift_amount) + "\n")
        elif opcode >= 1940 and opcode <= 1943:
            opname.append('MOVK')
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName + "\t" + "R" + \
            str(Rd_dec) + ", " + str(iw_mov_imm_dec_k) + ", " + \
            "LSL " + str(iw_shift_amount) + "\n")

    def Break(self, line, output):
        opname.append('BREAK')
        mem_start = address + 4

        #### fill other lists ####
        arg1.append(0)
        arg2.append(0)
        arg3.append(0)
        dest.append(0)
        src1.append(0)
        src2.append(0)

        output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
        " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\n")

    def twosComplement(self, line, output):
        #### fill other lists ####
        opname.append('')
        arg1.append(0)
        arg2.append(0)
        arg3.append(0)
        dest.append(0)
        src1.append(0)
        src2.append(0)

        line = line[:32]
        val = int(line, 2)

        if line[:1] == '0':
            line_dec = binToDec(int(line))
            output.write(line + "\t" + str(address) + "\t" + str(line_dec) + "\n")
            memory[(address - mem_start) / 4] = line_dec

        elif(val & (1 << (len(line) - 1))) != 0:
            val = val - (1 << len(line))
            output.write(line + "\t" + str(address) + "\t" + str(val) + "\n")
            memory[(address - mem_start) / 4] = val

class InstructionFetch:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.PC = PC
        self.cycle = 0



class PreIssue:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC
        self.entry0 = 0
        self.entry1 = 0
        self.entry2 = 0
        self.entry3 = 0
class Issue:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC
        self.inst0 = 0
        self.inst1 = 0

class PreMEM:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC
        self.entry0 = 0
        self.entry1 = 0

class PreALU:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC
        self.entry0 = 0

class ALU:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC


class MemUnit:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC

class PostMEM:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC
        self.entry0 = 0

class PostALU:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, cycle, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
        self.PC = PC
        self.entry0 = 0


class WBUnit:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.PC = PC

class Cache:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.PC = PC

class control:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.PC = PC

class printState:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2, PC):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.instcount = instcount
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.PC = PC


def main:

dis = dissassemble()
dis.run
con = control()
con.run
