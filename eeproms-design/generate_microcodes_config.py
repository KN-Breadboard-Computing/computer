import json

from argparse import ArgumentParser
from pathlib import Path

class Reg:
    def __init__(self, name, altname = None):
        self._name = name.upper()
        self._altname = altname.upper() if altname is not None else ''

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
            'a+b': 'REG_A_PLUS_REG_B'
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
                'REG_IR_LOAD': 0,
                'MCC_TICK': 1,
                '~MCC_RST': 1
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

    def pc_inc(self):
        self._signals['PC_TICK'] = 1
        return self

    def mar_in(self):
        self._signals['REG_MAR_LOAD'] = 1
        return self

    def ir_in(self):
        self._signals['REG_IR_LOAD'] = 1
        return self

    def mem_to_bus(self):
        self._signals['REG_MBR_WORD_DIR'] = 0
        self._signals['~MEM_OUT'] = 0
        self._signals['~REG_MBR_USE_BUS'] = 0
        return self

    def mem_to_mbr(self):
        self._signals['REG_MBR_LOAD'] = 1
        self._signals['~MEM_OUT'] = 0
        return self

    def mbr_to_mem(self):
        self._signals['~MEM_IN'] = 0
        return self

    def alu_operation(self, op, dst, latch_flags):
        assert dst in DATA_REGS or dst == REG_MBR
        self._signals[f'REG_{dst}_LOAD'] = 1
        self._signals[f'REG_F_LOAD'] = 1 if latch_flags else 0
        self._alu_operation(self.alu_opcodes[self._alu_lut[op]])

        if dst == REG_MBR:
            self._signals['~REG_MBR_USE_BUS'] = 0

        return self

    def tmp_out(self):
        self._signals['~REG_TMPH_OUT'] = 0
        self._signals['~REG_TMPL_OUT'] = 0
        self._signals['REG_TMP_ADDRESS_DIR'] = 0
        self._signals['~REG_TMP_PASS_ADDRESS'] = 0
        return self

    def to_json(self):
        return self._signals

    @classmethod
    def load_alu_opcodes(cls, path):
        def extract_code(t):
            key, value = t
            bin_value = int(value['CODE'], 2) & 0x1FF
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
parser.add_argument('--alu-config', help='Path to the ALU config JSON')
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

LOAD_PC_TO_MAR = microcodes.add('LOAD_PC_TO_MAR').pc_out().mar_in()
LOAD_MEM_AT_MAR_TO_IR_PCpp = microcodes.add('LOAD_MEM[MAR]_TO_IR_PC++').mem_to_bus().ir_in().pc_inc()
RST_MC = microcodes.add('RST_MC').no_mcc_tick().mcc_rst()
LOAD_B_TO_A = microcodes.add('LOAD_B_TO_A').reg_to_bus(REG_B).reg_from_bus(REG_A)
LOAD_A_TO_B = microcodes.add('LOAD_A_TO_B').reg_to_bus(REG_A).reg_from_bus(REG_B)
LOAD_TH_TO_A = microcodes.add('LOAD_TH_TO_A').reg_to_bus(REG_TH).reg_from_bus(REG_A)
LOAD_TL_TO_A = microcodes.add('LOAD_TL_TO_A').reg_to_bus(REG_TL).reg_from_bus(REG_A)
LOAD_SUM_TO_A_LATCH_FLAGS = microcodes.add('LOAD_(A+B)_TO_A_LATCH_FLAGS').alu_operation('a+b', REG_A, True)
LOAD_SUM_TO_B_LATCH_FLAGS = microcodes.add('LOAD_(A+B)_TO_B_LATCH_FLAGS').alu_operation('a+b', REG_B, True)
LOAD_SUM_TO_MBR_LATCH_FLAGS = microcodes.add('LOAD_(A+B)_TO_MBR_LATCH_FLAGS').alu_operation('a+b', REG_MBR, True)
LOAD_MEM_AT_MAR_TO_A = microcodes.add('LOAD_MEM[MAR]_TO_A').mem_to_bus().reg_from_bus(REG_A)
LOAD_MEM_AT_MAR_TO_A_PCpp = microcodes.add('LOAD_MEM[MAR]_TO_A_PC++').mem_to_bus().reg_from_bus(REG_A).pc_inc()
LOAD_MEM_AT_MAR_TO_B = microcodes.add('LOAD_MEM[MAR]_TO_B').mem_to_bus().reg_from_bus(REG_B)
LOAD_MEM_AT_MAR_TO_B_PCpp = microcodes.add('LOAD_MEM[MAR]_TO_B_PC++').mem_to_bus().reg_from_bus(REG_B).pc_inc()
LOAD_MEM_AT_MAR_TO_TMPH_PCpp = microcodes.add('LOAD_MEM[MAR]_TO_TMPH_PC++').mem_to_bus().reg_from_bus(REG_TH).pc_inc()
LOAD_MEM_AT_MAR_TO_TMPL_PCpp = microcodes.add('LOAD_MEM[MAR]_TO_TMPL_PC++').mem_to_bus().reg_from_bus(REG_TL).pc_inc()
LOAD_TMP_TO_MAR = microcodes.add('LOAD_TMP_TO_MAR').tmp_out().mar_in()
LOAD_MEM_AT_MAR_TO_MBR_PCpp = microcodes.add('LOAD_MEM[MAR]_TO_MBR_PC++').mem_to_mbr().pc_inc()
LOAD_F_TO_A = microcodes.add('LOAD_F_TO_A').reg_to_bus(REG_F).reg_from_bus(REG_A)
LOAD_F_TO_B = microcodes.add('LOAD_F_TO_B').reg_to_bus(REG_F).reg_from_bus(REG_B)
LOAD_MBR_TO_MEM_AT_MAR = microcodes.add('LOAD_MBR_TO_MEM[MAR]').mbr_to_mem()
DO_NOTHING = microcodes.add('DO_NOTHING')
HALT_PROGRAM = microcodes.add('HALT_PROGRAM').no_mcc_tick()

with open(out_path, 'w') as out_file:
    microcodes.to_file(out_file, pretty_print=True)
