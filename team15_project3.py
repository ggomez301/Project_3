""""""
Team: 15
Guillermo Gomez / Lucia Sorto
Due Date: 10/31/2018
Instructor: Prof. Greg Lakomski
""""""
#!usr/bin/env
import sys
import os

class Dissassemble:
    def __init__(self):
        pass

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

            opCode[i_count] = binToDec(first_eleven_int)
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

        opFormat[i_count] = 'R'
        Rm_dec[i_count] = self.binToDec(Rm_int)
        shamt_dec[i_count] = self.binToDec(shamt_int)
        Rn_dec[i_count] = self.binToDec(Rn_int)
        Rd_dec[i_count] = self.binToDec(Rd_int)

        alu_imm_int = int(alu_imm)
        alu_imm_offset[i_count] = self.binToDec(alu_imm_int)

        #### fill other lists ####
        Rt_dec[i_count] = 0
        addr_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        check_nop = int(line[1:32])
        check_nop_dec = self.binToDec(check_nop)

        if opCode[i_count] == 1112:
            opName[i_count] = 'ADD'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" +  \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", R" + str(Rm_dec[i_count]) + "\n")
        elif opCode[i_count] == 1624:
            opName[i_count] = 'SUB'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", R" + str(Rm_dec[i_count]) + "\n")
        elif opCode[i_count] == 1104:
            opName[i_count] = 'AND'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", R" + str(Rm_dec[i_count]) + "\n")
        elif opCode[i_count] == 1360:
            opName[i_count] = 'ORR'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", R" + str(Rm_dec[i_count]) + "\n")
        elif opCode[i_count] == 1690:
            opName[i_count] = 'LSR'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", #" + str(alu_imm_offset[i_count]) + "\n")
        elif opCode[i_count] == 1691:
            opName[i_count] = 'LSL'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", #" + str(alu_imm_offset[i_count]) + "\n")
        elif opCode[i_count] == 1692:
            opName[i_count] = 'ASR'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", #" + str(alu_imm_offset[i_count]) + "\n")
        elif opCode[i_count] == 1872:
            opName[i_count] = 'EOR'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", R" + str(Rm_dec[i_count]) + "\n")
        elif check_nop_dec == 0:
            opName[i_count] = 'NOP'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\n")

    def iFormat(self, line, output):
        alu_imm = line[10:22]
        Rn = line[22:27]
        Rd = line[27:32]

        alu_imm_int = int(alu_imm)
        Rn_int = int(Rn)
        Rd_int = int(Rd)

        opFormat[i_count] = 'I'
        alu_imm_offset[i_count] = self.binToDec(alu_imm_int)
        Rn_dec[i_count] = self.binToDec(Rn_int)
        Rd_dec[i_count] = self.binToDec(Rd_int)

        #### fill other lists ####
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rt_dec[i_count] = 0
        addr_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        if (alu_imm_offset[i_count] & (1 << (len(alu_imm) - 1))) != 0:
            alu_imm_offset[i_count] = alu_imm_offset[i_count] - (1 << len(alu_imm))

        if opCode[i_count] == 1160 or opCode[i_count] == 1161:
            opName[i_count] = 'ADDI'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", #" + str(alu_imm_offset[i_count]) + "\n")
        elif opCode[i_count] == 1672 or opCode[i_count] == 1673:
            opName[i_count] = 'SUBI'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" \
                + str(Rd_dec[i_count]) + ", R" + str(Rn_dec[i_count]) + ", #" + str(alu_imm_offset[i_count]) + "\n")

    def dFormat(self, line, output):
        dt_addr = line[12:20]
        Rn = line[23:27]
        Rt = line[28:32]

        dt_addr_int = int(dt_addr)
        Rn_int = int(Rn)
        Rt_int = int(Rt)

        opFormat[i_count] = 'D'
        addr_offset[i_count] = self.binToDec(dt_addr_int)
        Rn_dec[i_count] = self.binToDec(Rn_int)
        Rt_dec[i_count] = self.binToDec(Rt_int)

        #### fill other lists ####
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rd_dec[i_count] = 0
        alu_imm_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        if opCode[i_count] == 1984:
            opName[i_count] = 'STUR'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
            str(Rt_dec[i_count]) + ", [R" + str(Rn_dec[i_count]) + ", #" + str(dt_addr_offset[i_count]) + "]" + "\n")
        elif opCode[i_count] == 1986:
            opName[i_count] = 'LDUR'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
            str(Rt_dec[i_count]) + ", [R" + str(Rn_dec[i_count]) + ", #" + str(dt_addr_offset[i_count]) + "]" + "\n")

    def bFormat(self, line, output):
        br_addr = line[7:32]

        br_addr_int = int(br_addr)

        opFormat[i_count] = 'B'
        addr_offset[i_count] = self.binToDec(br_addr_int)

        #### fill other lists ####
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rn_dec[i_count] = 0
        Rd_dec[i_count] = 0
        Rt_dec[i_count] = 0
        alu_imm_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        if (addr_offset[i_count] & (1 << (len(br_addr) - 1))) != 0:
            br_addr_offset[i_count] = br_addr_offset[i_count] - (1 << len(br_addr))

        if opCode[i_count] >= 160 and opCode[i_count] <= 191:
            opName[i_count] = 'B'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "#" + \
                str(br_addr_offset[i_count]) + "\n")

    def cbFormat(self, line, output):
        cond_br_addr = line[7:27]
        Rt = line[27:32]

        cond_br_addr_int = int(cond_br_addr)
        Rt_int = int(Rt)

        opFormat[i_count] = 'CB'
        addr_offset[i_count] = self.binToDec(cond_br_addr_int)
        Rt_dec[i_count] = self.binToDec(Rt_int)

        #### fill other lists ####
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rn_dec[i_count] = 0
        Rd_dec[i_count] = 0
        alu_imm_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        if (addr_offset[i_count] & (1 << (len(cond_br_addr) - 1))) != 0:
            addr_offset[i_count] = addr_offset[i_count] - (1 << len(cond_br_addr))

        if opCode[i_count] >= 1440 and opCode[i_count] <= 1447:
            opName[i_count] = 'CBZ'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rt_dec[i_count]) + ", " + "#" + str(addr_offset[i_count]) + "\n")

        elif opCode[i_count] >= 1448 and opCode[i_count] <= 1455:
            opName[i_count] = 'CBNZ'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
                " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
                str(Rt_dec[i_count]) + ", " + "#" + str(addr_offset[i_count]) + "\n")

    def iwFormat(self, line, output):
        mov_imm = line[12:27]
        mov_imm_k = line[11:27]
        Rd = line[28:32]
        shift_bits = line[9:11]

        opFormat[i_count] = 'IW'
        mov_imm_int = int(mov_imm)
        mov_imm_int_k = int(mov_imm_k)
        Rd_int = int(Rd)
        shift_bits_int = int(shift_bits)

        iw_mov_imm_dec[i_count] = self.binToDec(mov_imm_int)
        iw_mov_imm_dec_k[i_count] = self.binToDec(mov_imm_int_k)
        Rd_dec[i_count] = self.binToDec(Rd_int)
        iw_shift_bits_dec[i_count] = self.binToDec(shift_bits_int)
        iw_shift_amount[i_count] = iw_shift_bits_dec[i_count] * 16

        #### fill other lists ####
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rn_dec[i_count] = 0
        Rt_dec[i_count] = 0
        alu_imm_offset[i_count] = 0
        addr_offset[i_count] = 0

        if opCode[i_count] >= 1684 and opCode[i_count] <= 1687:
            opName[i_count] = 'MOVZ'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
            str(Rd_dec[i_count]) + ", " + str(iw_mov_imm_dec[i_count]) + ", LSL " + str(iw_shift_amount[i_count]) + "\n")
        elif opCode[i_count] >= 1940 and opCode[i_count] <= 1943:
            opName[i_count] = 'MOVK'
            output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
            " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\t" + "R" + \
            str(Rd_dec[i_count]) + ", " + str(iw_mov_imm_dec_k[i_count]) + ", " + \
            "LSL " + str(iw_shift_amount[i_count]) + "\n")

    def Break(self, line, output):
        opName[i_count] = 'BREAK'
        mem_start = address[i_count] + 4

        #### fill other lists ####
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rn_dec[i_count] = 0
        Rd_dec[i_count] = 0
        Rt_dec[i_count] = 0
        alu_imm_offset[i_count] = 0
        addr_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        output.write(line[:8] + " " + line[8:11] + " " + line[11:16] + " " + line[16:21] + " " + line[21:26] + \
        " " + line[26:32] + "\t" + str(address[i_count]) + "\t" + opName[i_count] + "\n")

    def twosComplement(self, line, output):
        #### fill other lists ####
        opName[i_count] = ''
        Rm_dec[i_count] = 0
        shamt_dec[i_count] = 0
        Rn_dec[i_count] = 0
        Rd_dec[i_count] = 0
        Rt_dec[i_count] = 0
        alu_imm_offset[i_count] = 0
        addr_offset[i_count] = 0
        iw_mov_imm_dec[i_count] = 0
        iw_mov_imm_dec_k[i_count] = 0
        iw_shift_bits_dec[i_count] = 0
        iw_shift_amount[i_count] = 0

        line = line[:32]
        val = int(line, 2)

        if line[:1] == '0':
            line_dec = binToDec(int(line))
            output.write(line + "\t" + str(address[i_count]) + "\t" + str(line_dec) + "\n")
            memory[(address[i_count] - mem_start) / 4] = line_dec

        elif(val & (1 << (len(line) - 1))) != 0:
            val = val - (1 << len(line))
            output.write(line + "\t" + str(address[i_count]) + "\t" + str(val) + "\n")
            memory[(address[i_count] - mem_start) / 4] = val

class InstructionFetch:


class PreIssueBuffer:

class Issue:

class ALU:

class PostALU:

class MemUnit:

class WBUnit:
    def __init__(self, instrs, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2):
        self.instructions = instrs
        self.opcode = opcode
        self.memory = mem
        self.address = address
        self. 


class Cache:

class printState:
    def __init__(self, instructions, opcode, mem, valids, address, arg1, arg2, arg3,
                 instcount, dest, src1, src2):


def main:
