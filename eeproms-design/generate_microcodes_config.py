import json

from argparse import ArgumentParser
from pathlib import Path


class Reg:
    def __init__(self, name, altname = None):
        self._name = name.upper()
        self._altname = altname.upper() if altname is not None else self._name

    def __str__(self):
        return self._name

    def __eq__(self, other):
        return self._name == other._name and self._altname == other._altname

    def name(self):
        return self._name

    def altname(self):
        return self._altname

    def asmname(self):
        return self._name.tolower()


REG_A = Reg('A')
REG_B = Reg('B')
REG_TH = Reg('TMPH', 'TH')
REG_TL = Reg('TMPL', 'TL')
WORD_REGS = [REG_A, REG_B, REG_TH, REG_TL]
DATA_REGS = [REG_A, REG_B]
TMP_REGS = [REG_TH, REG_TL]

REG_MBR = Reg('MBR')
REG_F = Reg('F')


class Microcode:
    _alu_lut = {
            'a+b': 'REG_A_PLUS_REG_B',
            '-a': 'MINUS_REG_A',
            '-b': 'MINUS_REG_B',
            'a-b': 'REG_A_MINUS_REG_B',
            'b-a': 'REG_B_MINUS_REG_A',
            'a>>>1': 'ARITHMETIC_RIGHT_SHIFT_REG_A',
            'b>>>1': 'ARITHMETIC_RIGHT_SHIFT_REG_B',
            '~a': 'NOT_REG_A',
            '~b': 'NOT_REG_B',
            'a|b': 'REG_A_OR_REG_B',
            'a&b': 'REG_A_AND_REG_B',
            'a^b': 'REG_A_XOR_REG_B',
            'a>>1': 'LOGIC_RIGHT_SHIFT_REG_A',
            'b>>1': 'LOGIC_RIGHT_SHIFT_REG_B',
            'a<<1': 'LOGIC_LEFT_SHIFT_REG_A',
            'b<<1': 'LOGIC_LEFT_SHIFT_REG_B',
            '0': 'CONST_ZERO',

    }

    def __init__(self, name):
        self._name = name
        self._signals = {
                'REG_A_LOAD': 0,
                'REG_B_LOAD': 0,
                'ALU_OPC_0': 0,
                'ALU_OPC_1': 0,
                'ALU_OPC_2': 0,
                'ALU_OPC_3': 0,
                'ALU_OPC_4': 0,
                'REG_F_LOAD': 0,
                '~REG_F_OUT': 1,
                '~ALU_OUT': 1,
                'REG_TMPH_LOAD': 0,
                'REG_TMPL_LOAD': 0,
                '~REG_TMPH_OUT': 1,
                '~REG_TMPL_OUT': 1,
                '~REG_TMP_PASS_ADDRESS': 1,
                '~REG_TMPH_PASS_DATA': 1,
                '~REG_TMPL_PASS_DATA': 1,
                'REG_TMP_ADDRESS_DIR': 1,
                'REG_TMPH_DATA_DIR': 1,
                'REG_TMPL_DATA_DIR': 1,
                '~PC_LOAD': 1,
                '~PC_RST': 1,
                'PC_TICK': 0,
                '~PC_OUT': 1,
                '~STC_LOAD': 1,
                'STC_RST': 0,
                'STC_TICK': 0,
                'STC_MODE': 0,
                '~STC_OUT': 1,
                'REG_MAR_LOAD': 0,
                'REG_MBR_LOAD': 0,
                '~MEM_OUT': 1,
                '~MEM_IN': 1,
                'MEM_PART': 0,
                '~ZERO_PAGE': 1,
                'REG_MBR_WORD_DIR': 1,
                '~REG_MAR_USE_BTTNS': 1,
                '~REG_MBR_USE_BTTNS': 1,
                '~REG_MBR_USE_BUS': 1,
                'MEMORY_SELECTOR': 1,
                'REG_IR_LOAD': 0,
                'MCC_TICK': 1,
                '~MCC_RST': 1,
                'INT_OUT_0': 0,
                'INT_OUT_1': 0,
                'INT_OUT_2': 0,
                'INT_OUT_3': 0,
                'INT_OUT_4': 0,
                'SET_INT_ENABLE': 0,
                'RST_INT_ENABLE': 0,
                '~INT_ADDRESS_OUT': 0
        }

    def _alu_operation(self, code):
        self._signals['~ALU_OUT'] = 0
        for i in range(0, 5):
            self._signals[f'ALU_OPC_{i}'] = (code >> i) & 0x1
    
    def no_mcc_tick(self):
        self._signals['MCC_TICK'] = 0
        return self 

    def mcc_rst(self):
        self._signals['~MCC_RST'] = 0

    def reg_to_bus(self, reg):
        assert reg in WORD_REGS or reg == REG_F
        if reg in DATA_REGS:
            alu_code = f'REG_{reg}'
            self._alu_operation(self.alu_opcodes[alu_code])

        if reg in TMP_REGS:
            self._signals[f'~REG_{reg}_OUT'] = 0
            self._signals[f'REG_{reg}_DATA_DIR'] = 0
            self._signals[f'~REG_{reg}_PASS_DATA'] = 0

        if reg == REG_F:
            self._signals['~REG_F_OUT'] = 0

        return self

    def reg_from_bus(self, reg):
        assert reg in WORD_REGS
        self._signals[f'REG_{reg}_LOAD'] = 1

        if reg in TMP_REGS:
            self._signals[f'REG_{reg}_DATA_DIR'] = 1
            self._signals[f'~REG_{reg}_PASS_DATA'] = 0

        return self

    def pc_out(self):
        self._signals['~PC_OUT'] = 0
        return self

    def pc_in(self):
        self._signals['~PC_LOAD'] = 0
        return self

    def pc_inc(self):
        self._signals['PC_TICK'] = 1
        return self

    def mar_in(self):
        self._signals['REG_MAR_LOAD'] = 1
        return self

    def ir_in(self):
        self._signals['REG_IR_LOAD'] = 1
        return self

    def mbr_in(self):
        self._signals['REG_MBR_LOAD'] = 1
        self._signals['~REG_MBR_USE_BUS'] = 0
        self._signals['REG_MBR_WORD_DIR'] = 1
        return self

    def mem_to_bus(self, zero_page=False, stack=False):
        self._signals['REG_MBR_WORD_DIR'] = 0
        self._signals['~MEM_OUT'] = 0
        self._signals['~REG_MBR_USE_BUS'] = 0
        self._signals['~ZERO_PAGE'] = 0 if zero_page else 1
        self._signals['MEM_PART'] = 1 if stack else 0
        return self

    def mem_to_mbr(self, zero_page=False, stack=False):
        self._signals['REG_MBR_LOAD'] = 1
        self._signals['~MEM_OUT'] = 0
        self._signals['~ZERO_PAGE'] = 0 if zero_page else 1
        self._signals['MEM_PART'] = 1 if stack else 0
        return self

    def mbr_to_mem(self, zero_page=False, stack=False):
        self._signals['~MEM_IN'] = 0
        self._signals['~ZERO_PAGE'] = 0 if zero_page else 1
        self._signals['MEM_PART'] = 1 if stack else 0
        return self

    def alu_operation(self, op, dst, latch_flags):
        self._alu_operation(self.alu_opcodes[self._alu_lut[op.lower()]])
        self._signals[f'REG_F_LOAD'] = 1 if latch_flags else 0

        if dst is not None:
            assert dst in DATA_REGS or dst == REG_MBR
            self._signals[f'REG_{dst}_LOAD'] = 1

            if dst == REG_MBR:
                self._signals['~REG_MBR_USE_BUS'] = 0

        return self

    def tmp_out(self):
        self._signals['~REG_TMPH_OUT'] = 0
        self._signals['~REG_TMPL_OUT'] = 0
        self._signals['REG_TMP_ADDRESS_DIR'] = 0
        self._signals['~REG_TMP_PASS_ADDRESS'] = 0
        return self

    def tmp_in(self):
        return self.reg_from_bus(REG_TL).reg_from_bus(REG_TH)

    def tmp_addr_in(self):
        self._signals['REG_TMPH_LOAD'] = 1
        self._signals['REG_TMPL_LOAD'] = 1
        self._signals['REG_TMP_ADDRESS_DIR'] = 1
        self._signals['~REG_TMP_PASS_ADDRESS'] = 0
        return self

    def stc_out(self):
        self._signals['~STC_OUT'] = 0
        return self

    def stc_dec(self):
        self._signals['STC_TICK'] = 1
        return self

    def stc_inc(self):
        self._signals['STC_TICK'] = 1
        self._signals['STC_MODE'] = 1
        return self

    def set_int_enable(self):
        self._signals['SET_INT_ENABLE'] = 1
        return self

    def rst_int_enable(self):
        self._signals['RST_INT_ENABLE'] = 1
        return self

    def int_addr_out(self):
        self._signals['~INT_ADDRESS_OUT'] = 1
        return self

    def to_json(self):
        return self._signals

    @classmethod
    def load_alu_opcodes(cls, path):
        def extract_code(t):
            key, value = t
            bin_value = int(value['CODE'], 2) & 0x1F
            return key, bin_value

        with open(path) as file:
            alu_config = json.load(file)
            codes = alu_config['codes']
            cls.alu_opcodes = dict(map(extract_code, codes.items()))


class Microcodes:
    def __init__(self):
        self._microcodes = {}

    def add(self, name):
        microcode = Microcode(name)
        self._microcodes[name] = microcode
        return microcode

    def to_file(self, file, pretty_print=False):
        def encode(obj):
            return obj.to_json() if isinstance(obj, Microcode) else obj

        indent = 4 if pretty_print else None
        json.dump(self._microcodes, file, indent=indent, default=encode)


parser = ArgumentParser(description='Script to generate the microcodes config file') 
parser.add_argument('--alu-config', help='Path to the ALU config JSON. Default is ../config/alu.json', default='../config/alu.json')
parser.add_argument('--output', help='Path to the output file. Default is ./microcodes.json', default='./microcodes.json')
parser.add_argument('--force', help='Generate even if destination exists', action='store_true')

args = parser.parse_args()

out_path = Path(args.output)

if not args.force and out_path.exists():
    print('Output exists and force is not with us, bailing out')
    exit(1)

print(f'Destination is {out_path}')

Microcode.load_alu_opcodes(Path(args.alu_config))

microcodes = Microcodes()

microcodes.add('LOAD_PC_TO_MAR').pc_out().mar_in()
microcodes.add('LOAD_MEM[MAR]_TO_IR_PC++').mem_to_bus().ir_in().pc_inc()
microcodes.add('RST_MC').no_mcc_tick().mcc_rst()

mov_srcs = WORD_REGS + [ REG_F ]
mov_dsts = WORD_REGS
for dst in mov_dsts:
    microcodes.add(f'LOAD_TMP_TO_MAR_{dst.altname()}_TO_MBR').tmp_out().mar_in().reg_to_bus(dst).mbr_in()
    microcodes.add(f'LOAD_STC_TO_MAR_{dst.altname()}_TO_MBR').stc_out().mar_in().reg_to_bus(dst).mbr_in()
    microcodes.add(f'LOAD_MEM[MAR]_TO_{dst.altname()}_STC++').stc_inc().mem_to_bus().reg_from_bus(dst)
    microcodes.add(f'MOV_0_TO_{dst.altname()}').alu_operation('0', None, False).reg_from_bus(dst)
    for src in mov_srcs:
         if src == dst: continue
         microcodes.add(f'LOAD_{src.altname()}_TO_{dst.altname()}').reg_to_bus(src).reg_from_bus(dst)
         microcodes.add(f'LOAD_{src.altname()}_TO_{dst}').reg_to_bus(src).reg_from_bus(dst)
         microcodes.add(f'LOAD_{src}_TO_{dst}').reg_to_bus(src).reg_from_bus(dst)

microcodes.add('LOAD_MEM[MAR]_TO_A').mem_to_bus().reg_from_bus(REG_A)
microcodes.add('LOAD_MEM[MAR]_TO_A_PC++').mem_to_bus().reg_from_bus(REG_A).pc_inc()
microcodes.add('LOAD_MEM[MAR]_TO_B').mem_to_bus().reg_from_bus(REG_B)
microcodes.add('LOAD_MEM[MAR]_TO_B_PC++').mem_to_bus().reg_from_bus(REG_B).pc_inc()
microcodes.add('LOAD_MEM[MAR]_TO_TMPH_PC++').mem_to_bus().reg_from_bus(REG_TH).pc_inc()
microcodes.add('LOAD_MEM[MAR]_TO_TH_PC++').mem_to_bus().reg_from_bus(REG_TH).pc_inc()
microcodes.add('LOAD_MEM[MAR]_TO_TMPL_PC++').mem_to_bus().reg_from_bus(REG_TL).pc_inc()
microcodes.add('LOAD_MEM[MAR]_TO_TL_PC++').mem_to_bus().reg_from_bus(REG_TL).pc_inc()
microcodes.add('LOAD_TMP_TO_MAR').tmp_out().mar_in()
microcodes.add('LOAD_MEM[MAR]_TO_MBR_PC++').mem_to_mbr().pc_inc()
microcodes.add('LOAD_MBR_TO_MEM[MAR]').mbr_to_mem()
microcodes.add('LOAD_ZP_MEM[MAR]_TO_A').mem_to_bus(zero_page=True).reg_from_bus(REG_A)
microcodes.add('LOAD_ZP_MEM[MAR]_TO_B').mem_to_bus(zero_page=True).reg_from_bus(REG_B)
microcodes.add('LOAD_MBR_TO_ZP_MEM[MAR]').mbr_to_mem(zero_page=True)
microcodes.add('LOAD_PC_TO_MAR_A_TO_TMPL').pc_out().mar_in().reg_to_bus(REG_A).reg_from_bus(REG_TL)
microcodes.add('LOAD_PC_TO_MAR_B_TO_TMPL').pc_out().mar_in().reg_to_bus(REG_B).reg_from_bus(REG_TL)
microcodes.add('LOAD_PC_TO_MAR_TH_TO_TMPL').pc_out().mar_in().reg_to_bus(REG_TH).reg_from_bus(REG_TL)
microcodes.add('LOAD_PC_TO_MAR_TL_TO_TMPL').pc_out().mar_in().reg_to_bus(REG_TL).reg_from_bus(REG_TL)

for reg in DATA_REGS:
    for dst in DATA_REGS:
        microcodes.add(f'MOV_NEG{reg}_TO_{dst}').alu_operation(f'-{reg}', dst, True)
        microcodes.add(f'MOV_DIV2{reg}_TO_{dst}').alu_operation(f'{reg}>>>1', dst, True)
        microcodes.add(f'MOV_INV{reg}_TO_{dst}').alu_operation(f'~{reg}', dst, True)
        microcodes.add(f'MOV_SHR{reg}_TO_{dst}').alu_operation(f'{reg}>>1', dst, True)
        microcodes.add(f'MOV_SHL{reg}_TO_{dst}').alu_operation(f'{reg}<<1', dst, True)

    microcodes.add(f'MOV_NEG{reg}_TO_MBR_SAVE_FLAGS').alu_operation(f'-{reg}', REG_MBR, latch_flags=True)
    microcodes.add(f'MOV_NEG{reg}_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation(f'-{reg}', REG_MBR, latch_flags=True).stc_out().mar_in()
    microcodes.add(f'MOV_ADD_TO_{reg}').alu_operation('a+b', reg, True)
    microcodes.add(f'MOV_SUBAB_TO_{reg}').alu_operation('a-b', reg, True)
    microcodes.add(f'MOV_SUBBA_TO_{reg}').alu_operation('b-a', reg, True)
    microcodes.add(f'MOV_DIV2{reg}_TO_MBR_SAVE_FLAGS').alu_operation(f'{reg}>>>1', reg, True)
    microcodes.add(f'MOV_DIV2{reg}_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation(f'{reg}>>>1', reg, True).stc_out().mar_in()
    microcodes.add(f'MOV_INV{reg}_TO_MBR_SAVE_FLAGS').alu_operation(f'~{reg}', reg, True)
    microcodes.add(f'MOV_INV{reg}_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation(f'~{reg}', reg, True).stc_out().mar_in()
    microcodes.add(f'MOV_OR_TO_{reg}').alu_operation('a|b', reg, True)
    microcodes.add(f'MOV_AND_TO_{reg}').alu_operation('a&b', reg, True)
    microcodes.add(f'MOV_XOR_TO_{reg}').alu_operation('a^b', reg, True)
    microcodes.add(f'MOV_SHR{reg}_TO_MBR_SAVE_FLAGS').alu_operation(f'{reg}>>1', reg, True)
    microcodes.add(f'MOV_SHR{reg}_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation(f'{reg}>>1', reg, True).stc_out().mar_in()
    microcodes.add(f'MOV_SHL{reg}_TO_MBR_SAVE_FLAGS').alu_operation(f'{reg}<<1', reg, True)
    microcodes.add(f'MOV_SHL{reg}_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation(f'{reg}<<1', reg, True).stc_out().mar_in()

microcodes.add('LOAD_MBR_TO_STC_MEM[MAR]_STC--').mbr_to_mem(stack=True).stc_dec()
microcodes.add('MOV_ADD_TO_MBR_SAVE_FLAGS').alu_operation('a+b', REG_MBR, True)
microcodes.add('MOV_ADD_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation('a+b', REG_MBR, True).stc_out().mar_in()
microcodes.add('MOV_SUBAB_TO_MBR_SAVE_FLAGS').alu_operation('a-b', REG_MBR, True)
microcodes.add('MOV_SUBBA_TO_MBR_SAVE_FLAGS').alu_operation('b-a', REG_MBR, True)
microcodes.add('MOV_SUBAB_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation('a-b', REG_MBR, True).stc_out().mar_in()
microcodes.add('MOV_SUBBA_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation('b-a', REG_MBR, True).stc_out().mar_in()
microcodes.add('MOV_OR_TO_MBR_SAVE_FLAGS').alu_operation('a|b', REG_MBR, True)
microcodes.add('MOV_OR_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation('a|b', REG_MBR, True).stc_out().mar_in()
microcodes.add('MOV_AND_TO_MBR_SAVE_FLAGS').alu_operation('a&b', REG_MBR, True)
microcodes.add('MOV_AND_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation('a&b', REG_MBR, True).stc_out().mar_in()
microcodes.add('MOV_XOR_TO_MBR_SAVE_FLAGS').alu_operation('a^b', REG_MBR, True)
microcodes.add('MOV_XOR_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR').alu_operation('a^b', REG_MBR, True).stc_out().mar_in()
microcodes.add('CALCULATE_A-B_SAVE_FLAGS_TO_REG_F').alu_operation('a-b', None, True)
microcodes.add('CALCULATE_B-A_SAVE_FLAGS_TO_REG_F').alu_operation('b-a', None, True)
microcodes.add('MOV_0_TO_TMPH_AND_TMPL').alu_operation('0', None, False).reg_from_bus(REG_TL).reg_from_bus(REG_TH)
# TODO: Fix increment microcodes, for now make them noops
microcodes.add('MOV_A+1_TOA_SAVE_FLAGS_TO_REG_F')
microcodes.add('MOV_B+1_TOB_SAVE_FLAGS_TO_REG_F')
microcodes.add('MOV_TL+1_TOTL_SAVE_FLAGS_TO_REG_F')
microcodes.add('MOV_A-1_TOA_SAVE_FLAGS_TO_REG_F')
microcodes.add('MOV_B-1_TOB_SAVE_FLAGS_TO_REG_F')
microcodes.add('MOV_TL-1_TOTL_SAVE_FLAGS_TO_REG_F')

microcodes.add('LOAD_TMP_TO_PC').tmp_out().pc_in()
microcodes.add('LOAD_MEM[MAR]_TO_A_LOAD_PC_TO_TMP').mem_to_bus().reg_from_bus(REG_A).tmp_out().pc_in()
microcodes.add('MOV_A+B_TO_TMPL').alu_operation('a+b', None, False).reg_from_bus(REG_TL)
microcodes.add('LOAD_PC_TO_TMP').tmp_addr_in().pc_out()
microcodes.add('LOAD_PC_TO_TMP_SET_ISR_FLAG').tmp_addr_in().pc_out().set_int_enable()
microcodes.add('LOAD_STC_TO_MAR_LOAD_TMPL_TO_MBR').stc_out().mar_in().reg_to_bus(REG_TL).mbr_in()
microcodes.add('LOAD_MBR_TO_MEM[MAR]_STC--').stc_dec().mbr_to_mem(stack=True)
microcodes.add('LOAD_STC_TO_MAR_LOAD_TMPH_TO_MBR').stc_out().mar_in().reg_to_bus(REG_TH).mbr_in()
microcodes.add('LOAD_STC_TO_MAR').stc_out().mar_in()
microcodes.add('LOAD_MEM[MAR]_TO_TMPH_STC++').mem_to_bus(stack=True).reg_from_bus(REG_TH).stc_inc()
microcodes.add('LOAD_MEM[MAR]_TO_TMPL_STC++').mem_to_bus(stack=True).reg_from_bus(REG_TL).stc_inc()
microcodes.add('PC++').pc_inc()
microcodes.add('PC++_RESET_ISR_FLAG').pc_inc().rst_int_enable()
microcodes.add('LOAD_MEM[MAR]_TO_MBR').mem_to_mbr()
microcodes.add('LOAD_MEM[MAR]_TO_MBR_STC++').mem_to_mbr(stack=True).stc_inc()
microcodes.add('DO_NOTHING')
microcodes.add('HALT').no_mcc_tick()
microcodes.add('LOAD_DATA_FROM_BUS_TO_MAR_AND_MBR').mbr_in().mar_in()
microcodes.add('LOAD_ISR_ADDRESS_TO_PC_AND_MAR').pc_in().mar_in().int_addr_out()

with open(out_path, 'w') as out_file:
    microcodes.to_file(out_file, pretty_print=True)
