from typing import List
import json
from argparse import ArgumentParser
from pathlib import Path

MMB = "\\\\("  # math mode begin symbol
MME = "\\\\)"  # math mode end symbol
TEXT = "\\\\texttt"  # text mode function name
LEFTARROW = "\\\\leftarrow"  # left arrow symbol
AND = "\\\\ \\\\& \\\\"  # and symbol
SPACE = "\\\\ "  # space symbol

REGS8 = ["REG_A", "REG_B", "REG_TMPH", "REG_TMPL", "REG_F"]  # names of 8bit registers
REGS16 = ["REG_TMP"]  # names of 16bit registers

REGS8ABR = {"REG_A": "A", "REG_B": "B", "REG_TMPH": "TH", "REG_TMPL": "TL",
            "REG_F": "F"}  # abbreviated names of 8bit registers
REGS16ABR = {"REG_TMP": "T"}  # abbreviated names of 16bit registers

FLAGS = ["S", "P", "Z", "C", "O"]  # abbreviated names of flags
FLAGS_DESCRIPTION = ["sign", "parity", "zero", "carry", "overflow"]  # names of flags

# available operations with descriptions
# [mnemonic, possible arguments, operation name, math operator]
OPERATIONS = [
    ["NEG", [["REG_A"], ["REG_B"]], "negation", "-"],
    ["ADD", [[]], "sum", "+"],
    ["SUB", [["REG_A", "REG_B"], ["REG_B", "REG_A"]], "difference", "-"],
    # ["MUL2", [["REG_A"], ["REG_B"]],                    "product",              "*"],
    ["DIV2", [["REG_A"], ["REG_B"]], "quotient", "/"],
    ["INV", [["REG_A"], ["REG_B"]], "bit inversion", "not"],
    ["OR", [[]], "alternative", "or"],
    ["AND", [[]], "conjunction", "and"],
    ["XOR", [[]], "exclusive disjunction", "xor"],
    ["SHR", [["REG_A"], ["REG_B"]], "right shift", ">>"],
    ["SHL", [["REG_A"], ["REG_B"]], "left shift", "<<"]
]

# available operation result destinations with descriptions
OPERATION_DESTINATIONS = [["A", "REG_A", "REG_A"], ["B", "REG_B", "REG_B"],
                          ["MEM", "memory at given address", "MEM[MAR]"],
                          ["MEMZP", "zero page memory at given address", "ZP_MEM[MAR]"],
                          ["STC", "stack", "STC_MEM[MAR]"]]


class Instructions:
    def __init__(self):
        self._instructions = {}
        self._instructions_counter = 0

    def add(self, name: str, category: str, mnemonic: str, arguments: List[str], microcodes: List[str], description: str,
                        microcodes_description: str, total_microcodes_number: str = '', flag: str = '', branch = None):
        min_cycles = ""
        max_cycles = ""
        if total_microcodes_number != '':
            max_cycles, min_cycles = [x.strip() for x in total_microcodes_number.split("or")]
        microcodes_number = str(len(microcodes) - 1) if total_microcodes_number == '' else total_microcodes_number
        if max_cycles == '':
            max_cycles = min_cycles = microcodes_number

        branch_object = 'null' if branch is None else f"""{{
            "taken": "{branch['taken']}",
            "not-taken": "{branch['not_taken']}"
        }}"""

        self._instructions[name] = {
            "id": self._instructions_counter,
            "name": name,
            "category": category,
            "opcode": f"0b{bin(self._instructions_counter + 1)[2:].zfill(8)}",
            "mnemonic": mnemonic,
            "arguments": arguments,
            "microcodes": microcodes,
            "branch": branch_object,
            "description": description,
            "microcodes-description": microcodes_description,
            "depend-on-flag": flag,
            "min-cycles-number": min_cycles,
            "max-cycles-number": max_cycles,
            "total-microcodes-number": microcodes_number
        }

        self._instructions_counter += 1

    def to_file(self, file, pretty_print=False):
        def encode(obj):
            return obj

        indent = 4 if pretty_print else None
        json.dump(self._instructions, file, indent=indent, default=encode)

def build_text(text: str) -> str:
    return f"{TEXT}{{{text}}}"


parser = ArgumentParser(description='Script to generate the instructions config file') 
parser.add_argument('--output', help='Path to the output file. Default is ./microcodes.json', default='./microcodes.json')
parser.add_argument('--force', help='Generate even if destination exists', action='store_true')

args = parser.parse_args()

out_path = Path(args.output)

if not args.force and out_path.exists():
    print('Output exists and force is not with us, bailing out')
    exit(1)

print(f'Destination is {out_path}')

instructions = Instructions()

# Generating move instructions
category = "Move Instructions"
mnemonic = "MOV"

# Moves between registers
for reg1_index in range(len(REGS8)):
    for reg2_index in range(len(REGS8)):
        reg1 = REGS8[reg1_index]
        reg2 = REGS8[reg2_index]
        if reg1 == reg2 or reg1 == "REG_F":
            continue

        name = f"{mnemonic}{REGS8ABR[reg1]}{REGS8ABR[reg2]}"
        microcodes = [
            "LOAD_PC_TO_MAR",
            "LOAD_MEM[MAR]_TO_IR_PC++",
            f"LOAD_{REGS8ABR[reg2]}_TO_{REGS8ABR[reg1]}",
            "RST_MC"
        ]
        description = f"Move value from {MMB} {build_text(reg2)} {MME} to {MMB} {build_text(reg1)} {MME}"
        microcodes_description = f"{MMB} {build_text(reg1)} {LEFTARROW} {build_text(reg2)} {MME}"

        instructions.add(name, category, mnemonic, [REGS8ABR[reg1], REGS8ABR[reg2]], microcodes, description, microcodes_description)

# Moves of constants to register
for reg in REGS8:
    if reg == "REG_F":
        continue

    name = f"{mnemonic}{REGS8ABR[reg]}IMM"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        "LOAD_PC_TO_MAR",
        f"LOAD_MEM[MAR]_TO_{REGS8ABR[reg]}_PC++",
        "RST_MC"
    ]
    description = f"Move given constant to {MMB} {build_text(reg)} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text(reg)} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME}"

    instructions.add(name, category, mnemonic, [REGS8ABR[reg], 'CONST'], microcodes, description, microcodes_description)

# Moves from memory at address given by constant to register
for reg in ["REG_A", "REG_B"]:
    name = f"{mnemonic}{REGS8ABR[reg]}ABS"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_TMPH_PC++",
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_TMPL_PC++",
        "LOAD_TMP_TO_MAR",
        f"LOAD_MEM[MAR]_TO_{REGS8ABR[reg]}",
        "RST_MC"
    ]
    description = f"Move constant from memory at given address to {MMB} {build_text(reg)} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('REG_A')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {MME}"

    instructions.add(name, category, mnemonic, [REGS8ABR[reg], 'MEM16'], microcodes, description, microcodes_description)

    name = f"{mnemonic}{REGS8ABR[reg]}ABSZP"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_TMPH_PC++",
        "LOAD_TMP_TO_MAR",
        f"LOAD_ZP_MEM[MAR]_TO_{REGS8ABR[reg]}",
        "RST_MC"
    ]
    description = f"Move constant from zero page memory at given address to {MMB} {build_text(reg)} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text(reg)} {LEFTARROW} {build_text('MEM[REG_MAR]')} {MME}"

    instructions.add(name, category, mnemonic, [REGS8ABR[reg], 'MEM8'], microcodes, description, microcodes_description)

# Moves from register to memory at address given by constant
mnemonic = "MOVAT"
for reg in ["REG_A", "REG_B"]:
    name = f"{mnemonic}ABS{REGS8ABR[reg]}"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_TMPH_PC++",
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_TMPL_PC++",
        f"LOAD_TMP_TO_MAR_{REGS8ABR[reg]}_TO_MBR",
        "LOAD_MBR_TO_MEM[MAR]",
        "RST_MC"
    ]
    description = f"Move value from {MMB} {build_text(reg)} {MME} to memory at given address"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text(reg)} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

    instructions.add(name, category, mnemonic, ['MEM16', REGS8ABR[reg]], microcodes, description, microcodes_description)

    name = f"{mnemonic}ABS{REGS8ABR[reg]}ZP"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_TMPH_PC++",
        f"LOAD_TMP_TO_MAR_{REGS8ABR[reg]}_TO_MBR",
        "LOAD_MBR_TO_ZP_MEM[MAR]",
        "RST_MC"
    ]
    description = f"Move value from {MMB} {build_text(reg)} {MME} to zero page memory at given address"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text(reg)} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

    instructions.add(name, category, mnemonic, ['MEM8', REGS8ABR[reg]], microcodes, description, microcodes_description)

# Moves constants to memory at address given by constant
name = f"{mnemonic}ABSIMM"
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR_PC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]",
    "RST_MC"
]
description = "Move given constant to memory at given address"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

instructions.add(name, category, mnemonic, ['MEM16', 'CONST'], microcodes, description, microcodes_description)

# Moves constants to zero page memory at address given by constant
name = f"{mnemonic}ABSIMMZP"
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR_PC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]",
    "RST_MC"
]
description = "Move given constant to zero page memory at given address"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

instructions.add(name, category, mnemonic, ['MEM8', 'CONST'], microcodes, description, microcodes_description)

# Moves from registers to memory at address given by REG_TMP
for reg in ["REG_A", "REG_B"]:
    name = f"{mnemonic}T{REGS8ABR[reg]}"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"LOAD_TMP_TO_MAR_{REGS8ABR[reg]}_TO_MBR",
        "LOAD_MBR_TO_MEM[MAR]",
        "RST_MC"
    ]
    description = f"Move value from {MMB} {build_text(reg)} {MME} to memory at address given by value of {MMB} {build_text('REG_TMP')} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text(reg)} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

    instructions.add(name, category, mnemonic, [REGS16ABR['REG_TMP'], REGS8ABR[reg]], microcodes, description, microcodes_description)

# Moves from registers to zero page memory at address given by other register
for reg1_index in range(len(REGS8)):
    for reg2_index in range(len(REGS8)):
        reg1 = REGS8[reg1_index]
        reg2 = REGS8[reg2_index]
        if reg1 == reg2 or reg1 == "REG_F" or reg2 == "REG_F":
            continue

        name = f"{mnemonic}{REGS8ABR[reg1]}{REGS8ABR[reg2]}"

        if reg1 == "REG_TMPL":
            microcodes = [
                "LOAD_PC_TO_MAR",
                "LOAD_MEM[MAR]_TO_IR_PC++",
                f"LOAD_TMP_TO_MAR_{REGS8ABR[reg2]}_TO_MBR",
                "LOAD_MBR_TO_ZP_MEM[MAR]",
                "RST_MC"
            ]
            description = f"Move value from {MMB} {build_text(reg2)} {MME} to zero page memory at address given by value of {MMB} {build_text(reg1)} {MME}"
            microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text(reg2)} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"
        else:
            microcodes = [
                "LOAD_PC_TO_MAR",
                "LOAD_MEM[MAR]_TO_IR_PC++",
                f"LOAD_{REGS8ABR[reg1]}_TO_TMPL",
                f"LOAD_TMP_TO_MAR_{REGS8ABR[reg2]}_TO_MBR",
                "LOAD_MBR_TO_ZP_MEM[MAR]",
                "RST_MC"
            ]
            description = f"Move value from {MMB} {build_text(reg2)} {MME} to zero page memory at address given by value of {MMB} {build_text(reg1)} {MME}"
            microcodes_description = f"{MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text(reg1)} {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text(reg2)} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

        instructions.add(name, category, mnemonic, [REGS8ABR[reg1], REGS8ABR[reg2]], microcodes, description, microcodes_description)

# Moves constants to memory at address given by REG_TMP
name = f"{mnemonic}TIMM"
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR_PC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]",
    "RST_MC"
]
description = f"Move given constant to memory at address given by value of {MMB} {build_text('REG_TMP')} {MME}"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

instructions.add(name, category, mnemonic, [REGS16ABR['REG_TMP'], 'CONST'], microcodes, description, microcodes_description)

# Moves constants to zero page memory at address given by register
for reg in REGS8:
    if reg == "REG_F":
        continue

    name = f"{mnemonic}{REGS8ABR[reg]}IMM"
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"LOAD_PC_TO_MAR_{REGS8ABR[reg]}_TO_TMPL",
        "LOAD_MEM[MAR]_TO_MBR_PC++",
        f"LOAD_TMP_TO_MAR",
        "LOAD_MBR_TO_ZP_MEM[MAR]",
        "RST_MC"
    ]
    description = f"Move given constant to zero page memory at address given by value of {MMB} {build_text(reg)} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {AND} {build_text('REG_TMPL')} {LEFTARROW} {build_text(reg)} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

    instructions.add(name, category, mnemonic, [REGS8ABR[reg], 'CONST'], microcodes, description, microcodes_description)

# Generating ALU instructions
category = "ALU Instructions"

# Generating math operations
for operation in OPERATIONS:
    mnemonic = operation[0]
    for destination in OPERATION_DESTINATIONS:
        for args in operation[1]:
            args_abr = [REGS8ABR[arg] for arg in args]
            name = f"{mnemonic}{destination[0]}{''.join(args_abr)}"
            arguments = [destination[0]] + args_abr

            if len(args) == 0:
                operation_args = f"{MMB} {build_text('REG_A')} {MME} and {MMB} {build_text('REG_B')} {MME}"
                operation_args_mc = f"{build_text(f'REG_A {operation[3]} REG_B')}"
            elif len(args) == 1:
                operation_args = f"{MMB} {build_text(args[0])} {MME}"
                if operation[3] == "-":
                    operation_args_mc = f"{operation[3]}{build_text(args[0])}"
                elif operation[3] == "not":
                    operation_args_mc = f"{operation[3]} {SPACE} {build_text(args[0])}"
                elif operation[3] == ">>" or operation[3] == "<<":
                    operation_args_mc = f"{build_text(args[0])}{operation[3]}2"
                elif operation[3] == "*" or operation[3] == "/":
                    operation_args_mc = f"{build_text(args[0])}{operation[3]}2"
            else:
                operation_args = f"{MMB} {build_text(args[0])} {MME} and {MMB} {build_text(args[1])} {MME}"
                operation_args_mc = f"{build_text(f'{args[0]} {operation[3]} {args[1]}')}"

            if destination[0] == "A" or destination[0] == "B":
                operation_destination = f"{MMB} {build_text(destination[1])} {MME}"
                operation_destination_mc = f"{build_text(destination[2])}"
            else:
                operation_destination = destination[1]
                operation_destination_mc = destination[2]

            description = f"Calculate {operation[2]} of {operation_args} and save it to {operation_destination}"

            if destination[0] == "A" or destination[0] == "B":
                microcodes_core = [
                    f"MOV_{operation[0]}{''.join(args_abr)}_TO_{destination[0]}"
                ]
                microcodes_description = f"{MMB} {operation_destination_mc} {LEFTARROW} ({operation_args_mc}) {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"
            elif destination[0] == "MEM":
                microcodes_core = [
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_TMPH_PC++",
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_TMPL_PC++",
                    "LOAD_TMP_TO_MAR",
                    f"MOV_{operation[0]}{''.join(args_abr)}_TO_MBR_SAVE_FLAGS",
                    "LOAD_MBR_TO_MEM[MAR]",
                ]
                microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} ({operation_args_mc}) {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"
            elif destination[0] == "MEMZP":
                microcodes_core = [
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_TMPH_PC++",
                    "LOAD_TMP_TO_MAR",
                    f"MOV_{operation[0]}{''.join(args_abr)}_TO_MBR_SAVE_FLAGS",
                    "LOAD_MBR_TO_ZP_MEM[MAR]",
                ]
                microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} ({operation_args_mc}) {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"
            elif destination[0] == "STC":
                microcodes_core = [
                    f"MOV_{operation[0]}{''.join(args_abr)}_TO_MBR_SAVE_FLAGS_LOAD_STC_TO_MAR",
                    "LOAD_MBR_TO_STC_MEM[MAR]_STC--",
                ]
                microcodes_description = f"{MMB} {build_text('REG_MBR')} {LEFTARROW} ({operation_args_mc}) {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {AND} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME}"
            else:
                microcodes_core = []
                microcodes_description = f""

            microcodes = [
                             "LOAD_PC_TO_MAR",
                             "LOAD_MEM[MAR]_TO_IR_PC++",
                         ] + microcodes_core + ["RST_MC"]

            instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Generating compare operations
mnemonic = "CMP"
for reg1, reg2 in [("REG_A", "REG_B"), ("REG_B", "REG_A")]:
    name = f"{mnemonic}{REGS8ABR[reg1]}{REGS8ABR[reg2]}"
    arguments = [REGS8ABR[reg1], REGS8ABR[reg2]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"CALCULATE_{REGS8ABR[reg1]}-{REGS8ABR[reg2]}_SAVE_FLAGS_TO_REG_F",
        "RST_MC"
    ]
    description = f"Save flags of operation {MMB} {build_text(reg1)} - {build_text(reg2)} {MME} to {MMB} {build_text('REG_F')} {MME}"
    microcodes_description = f"{MMB} {build_text(f'calculate {reg1} - {reg2}')} {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

for reg1, reg2 in [("REG_TMPH", "REG_TMPL"), ("REG_TMPL", "REG_TMPH")]:
    name = f"{mnemonic}{REGS8ABR[reg1]}{REGS8ABR[reg2]}"
    arguments = [REGS8ABR[reg1], REGS8ABR[reg2]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"LOAD_{REGS8ABR[reg1]}_TO_{REGS8ABR['REG_A']}",
        f"LOAD_{REGS8ABR[reg2]}_TO_{REGS8ABR['REG_B']}",
        f"CALCULATE_A-B_SAVE_FLAGS_TO_REG_F",
        "RST_MC"
    ]
    description = f"Move {MMB} {build_text(reg1)} {MME} to {MMB} {build_text('REG_A')} {MME}, {MMB} {build_text(reg2)} {MME} to {MMB} {build_text('REG_B')} {MME} and save flags of operation {MMB} {build_text('REG_A')} - {build_text('REG_B')} {MME} to {MMB} {build_text('REG_F')} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_A')} {LEFTARROW} {build_text(reg1)} {MME} <br> {MMB} {build_text('REG_B')} {LEFTARROW} {build_text(reg2)} {MME} <br> {MMB} {build_text('calculate REG_A - REG_B')} {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

for reg1, reg2, reg3 in [("REG_TMPH", "REG_A", "REG_B"), ("REG_TMPH", "REG_B", "REG_A"), ("REG_TMPL", "REG_A", "REG_B"),
                         ("REG_TMPL", "REG_B", "REG_A")]:
    name = f"{mnemonic}{REGS8ABR[reg1]}{REGS8ABR[reg2]}"
    arguments = [REGS8ABR[reg1], REGS8ABR[reg2]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"LOAD_{REGS8ABR[reg1]}_TO_{REGS8ABR[reg3]}",
        f"CALCULATE_A-B_SAVE_FLAGS_TO_REG_F",
        "RST_MC"
    ]
    description = f"Move {MMB} {build_text(reg1)} {MME} to {MMB} {build_text(reg3)} {MME} and save flags of operation {MMB} {build_text('REG_A')} - {build_text('REG_B')} {MME} to {MMB} {build_text('REG_F')} {MME}"
    microcodes_description = f"{MMB} {build_text(reg3)} {LEFTARROW} {build_text(reg1)} {MME} <br> {MMB} {build_text('calculate REG_A - REG_B')} {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

    name = f"{mnemonic}{REGS8ABR[reg2]}{REGS8ABR[reg1]}"
    arguments = [REGS8ABR[reg2], REGS8ABR[reg1]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"LOAD_{REGS8ABR[reg1]}_TO_{REGS8ABR[reg3]}",
        f"CALCULATE_B-A_SAVE_FLAGS_TO_REG_F",
        "RST_MC"
    ]
    description = f"Move {MMB} {build_text(reg1)} {MME} to {MMB} {build_text(reg3)} {MME} and save flags of operation {MMB} {build_text('REG_B')} - {build_text('REG_A')} {MME} to {MMB} {build_text('REG_F')} {MME}"
    microcodes_description = f"{MMB} {build_text(reg3)} {LEFTARROW} {build_text(reg1)} {MME} <br> {MMB} {build_text('calculate REG_B - REG_A')} {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Generating clear operations
mnemonic = "CLR"
for reg in REGS8:
    if reg == "REG_F":
        continue

    name = f"{mnemonic}{REGS8ABR[reg]}"
    arguments = [REGS8ABR[reg]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"MOV_0_TO_{REGS8ABR[reg]}",
        "RST_MC"
    ]
    description = f"Set value of {MMB} {build_text(reg)} {MME} to {MMB} {build_text('0')} {MME}"
    microcodes_description = f"{MMB} {build_text(reg)} {LEFTARROW} {build_text('0')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

reg = "REG_TMP"
name = f"{mnemonic}{REGS16ABR[reg]}"
arguments = [REGS16ABR[reg]]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    f"MOV_0_TO_TMPH_AND_TMPL",
    "RST_MC"
]
description = f"Set value of {MMB} {build_text(reg)} {MME} to {MMB} {build_text('0')} {MME}"
microcodes_description = f"{MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('0')} {AND} {build_text('REG_TMPL')} {LEFTARROW} {build_text('0')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Generate increment operations
mnemonic = "INC"
for reg in ["REG_A", "REG_B"]:
    name = f"{mnemonic}{REGS8ABR[reg]}"
    arguments = [REGS8ABR[reg]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"MOV_{REGS8ABR[reg]}+1_TO{REGS8ABR[reg]}_SAVE_FLAGS_TO_REG_F",
        "RST_MC"
    ]
    description = f"Increment value of {MMB} {build_text(reg)} {MME} and save flags to {MMB} {build_text('REG_F')} {MME}"
    microcodes_description = f"{MMB} {build_text(reg)} {LEFTARROW} {build_text(reg)} + 1 {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

reg = "REG_TMP"
name = f"{mnemonic}{REGS16ABR[reg]}"
arguments = [REGS16ABR[reg]]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    f"MOV_{REGS8ABR['REG_TMPL']}+1_TO{REGS8ABR['REG_TMPL']}_SAVE_FLAGS_TO_REG_F",

    "RST_MC"
]
description = f"Increment value of {MMB} {build_text(reg)} {MME} and save flags to {MMB} {build_text('REG_F')} {MME}"
microcodes_description = f"{MMB} {build_text(reg)} {LEFTARROW} {build_text(reg)} + 1 {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Generate decrement operations
mnemonic = "DEC"
for reg in ["REG_A", "REG_B"]:
    if reg == "REG_F":
        continue

    name = f"{mnemonic}{REGS8ABR[reg]}"
    arguments = [REGS8ABR[reg]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"MOV_{REGS8ABR[reg]}-1_TO{REGS8ABR[reg]}_SAVE_FLAGS_TO_REG_F",
        "RST_MC"
    ]
    description = f"Decrement value of {MMB} {build_text(reg)} {MME} and save flags to {MMB} {build_text('REG_F')} {MME}"
    microcodes_description = f"{MMB} {build_text(reg)} {LEFTARROW} {build_text(reg)} - 1 {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

reg = "REG_TMP"
name = f"{mnemonic}{REGS16ABR[reg]}"
arguments = [REGS16ABR[reg]]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    f"MOV_{REGS8ABR['REG_TMPL']}+1_TO{REGS8ABR['REG_TMPL']}_SAVE_FLAGS_TO_REG_F",
    "RST_MC"
]
description = f"Decrement value of {MMB} {build_text(reg)} {MME} and save flags to {MMB} {build_text('REG_F')} {MME}"
microcodes_description = f"{MMB} {build_text(reg)} {LEFTARROW} {build_text(reg)} - 1 {MME} <br> {MMB} {AND} {build_text('save flags to REG_F')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Generate jump operations
category = "Jump instructions"
mnemonic = "JMPIMM"

name = f"{mnemonic}"
arguments = ["MEM16"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_TMP_TO_PC",
    "RST_MC"
]
description = f"Jump to given address"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('REG_TMP')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

for flag_index, flag in enumerate(FLAGS):
    for type in ["", "T"]:
        if type == "":
            type_name = "given address"
            target_instruction = "JMPIMM"
            arguments = ["MEM16"]
            branch = { "taken": "JMPIMM", "not_taken": "SKIP2" }
        else:
            type_name = f"address from {MMB} {build_text('REG_TMP')} {MME}"
            target_instruction = "JMPIMMT"
            arguments = ["T"]
            branch = { "taken": "JMPIMMT", "not_taken": "SKIP" }

        for condition in ["", "N"]:
            name = f"{mnemonic}{type}{condition}{flag}"
            if condition == "":
                microcodes = [
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_IR_PC++",
                ]
                description = f"Jump to {type_name} if {FLAGS_DESCRIPTION[flag_index]} flag is set"
                microcodes_description = f"{MMB} {build_text('if')} {SPACE} {build_text(f'REG_F[{flag_index}]')} {SPACE} {build_text('is set:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text(target_instruction)} {MME} <br> {MMB} {build_text('else:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text('SKIP2')} {MME}"
            else:
                microcodes = [
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_IR_PC++",
                ]
                description = f"Jump to {type_name} if {FLAGS_DESCRIPTION[flag_index]} flag is not set"
                microcodes_description = f"{MMB} {build_text('if')} {SPACE} {build_text(f'REG_F[{flag_index}]')} {SPACE} {build_text('is not set:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text(target_instruction)} {MME} <br> {MMB} {build_text('else:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text('SKIP2')} {MME}"

            instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description,
                                  flag=condition + flag, total_microcodes_number='7 or 4', branch=branch)

mnemonic = "JMPREL"

name = f"{mnemonic}"
arguments = ["CONST"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_A_LOAD_PC_TO_TMP",
    "LOAD_TMPL_TO_B",
    "MOV_A+B_TO_TMPL",
    "RST_MC"
]
description = f"Jump to address with given offset from current address"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_A')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('REG_TMP')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_B')} {LEFTARROW} {build_text('REG_TMPL')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('REG_A')} + {build_text('REG_B')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

for flag_index, flag in enumerate(FLAGS):
    for type in ["", "TL"]:
        if type == "":
            type_name = "address with given offset"
            target_instruction = "JMPREL"
            arguments = ["MEM8"]
            branch = { "taken": "JMPREL", "not_taken": "SKIP1" }
        else:
            type_name = f"address with given offset from {MMB} {build_text('REG_TMPL')} {MME}"
            target_instruction = "JMPRELTL"
            arguments = ["T"]
            branch = { "taken": "JMPRELTL", "not_taken": "SKIP" }

        for condition in ["", "N"]:
            name = f"{mnemonic}{type}{condition}{flag}"
            if condition == "":
                microcodes = [
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_IR_PC++",
                ]
                description = f"Jump to {type_name} if {FLAGS_DESCRIPTION[flag_index]} flag is set"
                microcodes_description = f"{MMB} {build_text('if')} {SPACE} {build_text(f'REG_F[{flag_index}]')} {SPACE} {build_text('is set:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text(target_instruction)} {MME} <br> {MMB} {build_text('else:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text('SKIP1')} {MME}"
            else:
                microcodes = [
                    "LOAD_PC_TO_MAR",
                    "LOAD_MEM[MAR]_TO_IR_PC++",
                ]
                description = f"Jump to {type_name} if {FLAGS_DESCRIPTION[flag_index]} flag is not set"
                microcodes_description = f"{MMB} {build_text('if')} {SPACE} {build_text(f'REG_F[{flag_index}]')} {SPACE} {build_text('is not set:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text(target_instruction)} {MME} <br> {MMB} {build_text('else:')} {MME} <br> {MMB} {SPACE} {SPACE} {build_text('SKIP1')} {MME}"

            
            instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description,
                                  flag=condition + flag, total_microcodes_number='6 or 3', branch=branch)

name = f"{mnemonic}FUN"
arguments = ["MEM16"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_TMP",
    "LOAD_STC_TO_MAR_LOAD_TMPL_TO_MBR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "LOAD_STC_TO_MAR_LOAD_TMPH_TO_MBR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_TMP_TO_PC",
    "RST_MC"
]
description = f"Push {MMB} {build_text('PC')} {MME} to stack and jump to given address"
microcodes_description = f"{MMB} {build_text('REG_TMP')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text('REG_TMPL')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text('REG_TMPH')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('REG_TMP')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = f"{mnemonic}RET"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_STC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_STC++",
    "LOAD_TMP_TO_PC",
    "PC++",
    "RST_MC"
]
description = f"Pop address from stack and jump to it"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

category = "Stack Instructions"

# Generate push operations
mnemonic = "PUSH"

for reg in REGS8:
    if reg == "REG_F":
        continue

    name = f"{mnemonic}{REGS8ABR[reg]}"
    arguments = [REGS8ABR[reg]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        f"LOAD_STC_TO_MAR_{REGS8ABR[reg]}_TO_MBR",
        "LOAD_MBR_TO_MEM[MAR]_STC--",
        "RST_MC"
    ]
    description = f"Push value of {MMB} {build_text(reg)} {MME} to stack"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text(reg)} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

reg = "REG_TMP"
name = f"{mnemonic}{REGS16ABR[reg]}"
arguments = [REGS16ABR[reg]]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    f"LOAD_STC_TO_MAR_{REGS8ABR['REG_TMPH']}_TO_MBR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    f"LOAD_STC_TO_MAR_{REGS8ABR['REG_TMPL']}_TO_MBR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "RST_MC"
]
description = f"Push value of {MMB} {build_text(reg)} {MME} to stack"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text('REG_TMPH')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text('REG_TMPL')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "PUSHIMM"
arguments = ["CONST"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR_PC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "RST_MC"
]
description = f"Push given constant to stack"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "PUSHABS"
arguments = ["MEM16"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR",
    "LOAD_STC_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "RST_MC"
]
description = f"Push value from given address to stack"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "PUSHABSZP"
arguments = ["MEM8"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR",
    "LOAD_STC_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "RST_MC"
]
description = f"Push value from given zero page address to stack"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Generate pop operations
mnemonic = "POP"

for reg in REGS8:
    if reg == "REG_F":
        continue

    name = f"{mnemonic}{REGS8ABR[reg]}"
    arguments = [REGS8ABR[reg]]
    microcodes = [
        "LOAD_PC_TO_MAR",
        "LOAD_MEM[MAR]_TO_IR_PC++",
        "LOAD_STC_TO_MAR",
        f"LOAD_MEM[MAR]_TO_{REGS8ABR[reg]}_STC++",
        "RST_MC"
    ]
    description = f"Pop value from stack to {MMB} {build_text(reg)} {MME}"
    microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text(reg)} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME}"

    instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

reg = "REG_TMP"
name = f"{mnemonic}{REGS16ABR[reg]}"
arguments = [REGS16ABR[reg]]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_STC_TO_MAR",
    f"LOAD_MEM[MAR]_TO_{REGS8ABR['REG_TMPL']}_STC++",
    "LOAD_STC_TO_MAR",
    f"LOAD_MEM[MAR]_TO_{REGS8ABR['REG_TMPH']}_STC++",
    "RST_MC"
]
description = f"Pop value from stack to {MMB} {build_text(reg)} {MME}"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "POPMEM"
arguments = ["MEM16"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR_STC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MBR_TO_MEM[MAR]",
    "RST_MC"
]
description = f"Pop value from stack to memory at given address"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "POPMEMZP"
arguments = ["MEM8"]
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_PC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MEM[MAR]_TO_MBR_STC++",
    "LOAD_TMP_TO_MAR",
    "LOAD_MBR_TO_ZP_MEM[MAR]",
    "RST_MC"
]
description = f"Pop value from stack to zero page memory at given address"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_MBR')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

category = "Other Instructions"

name = "NOP"
mnemonic = "NOP"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "DO_NOTHING",
    "RST_MC"
]
description = f"No nothing for one cycle"
microcodes_description = f"{MMB} {build_text('do nothing')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "SKIP"
mnemonic = "SKIP"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "RST_MC"
]
description = f"Skip instruction"
microcodes_description = f""

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "SKIP1"
mnemonic = "SKIP1"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "PC++",
    "RST_MC"
]
description = f"Skip next program line"
microcodes_description = f"{MMB} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "SKIP2"
mnemonic = "SKIP2"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "PC++",
    "PC++",
    "RST_MC"
]
description = f"Skip next two program lines"
microcodes_description = f"{MMB} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "ISR"
mnemonic = "ISR"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_PC_TO_TMP_SET_ISR_FLAG",
    "LOAD_STC_TO_MAR_LOAD_TMPL_TO_MBR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "LOAD_STC_TO_MAR_LOAD_TMPH_TO_MBR",
    "LOAD_MBR_TO_MEM[MAR]_STC--",
    "LOAD_ISR_ADDRESS_TO_PC_AND_MAR",
    "LOAD_MEM[MAR]_TO_TH_PC++",
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TL_PC++",
    "LOAD_TMP_TO_PC_SET_ISR_FLAG",
    "RST_MC"
]
description = f"Enter interrupt service routine"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TMP')} {LEFTARROW} {build_text('PC')} {AND} {build_text('set ISR flag')} {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text('REG_TMPL')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {AND} {build_text('REG_MBR')} {LEFTARROW} {build_text('REG_TMPH')} {MME} <br> {MMB} {build_text('MEM[REG_MAR]')} {LEFTARROW} {build_text('REG_MBR')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} - 1 {MME} <br> {MMB} {build_text('load ISR address to PC and MAR')} {MME} <br> {MMB} {build_text('REG_TH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('PC')} {MME} <br> {MMB} {build_text('REG_TL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('REG_TMP')} {AND} {build_text('set ISR flag')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "IRET"
mnemonic = "IRET"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPH_STC++",
    "LOAD_STC_TO_MAR",
    "LOAD_MEM[MAR]_TO_TMPL_STC++",
    "LOAD_TMP_TO_PC",
    "PC++_RESET_ISR_FLAG",
    "RST_MC"
]
description = f"Return from interrupt service routine"
microcodes_description = f"{MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_TMPH')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('REG_MAR')} {LEFTARROW} {build_text('STC')} {MME} <br> {MMB} {build_text('REG_TMPL')} {LEFTARROW} {build_text('MEM[REG_MAR]')} {AND} {build_text('STC')} {LEFTARROW} {build_text('STC')} + 1 {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('REG_TMP')} {MME} <br> {MMB} {build_text('PC')} {LEFTARROW} {build_text('PC')} + 1 {AND} {build_text('reset ISR flag')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

name = "HALT"
mnemonic = "HALT"
arguments = []
microcodes = [
    "LOAD_PC_TO_MAR",
    "LOAD_MEM[MAR]_TO_IR_PC++",
    "HALT"
]
description = f"Stop executing program"
microcodes_description = f"{MMB} {build_text('HALT')} {MME}"

instructions.add(name, category, mnemonic, arguments, microcodes, description, microcodes_description)

# Save instructions configuration to file
with open(out_path, 'w') as out_file:
    instructions.to_file(out_file, pretty_print=True)