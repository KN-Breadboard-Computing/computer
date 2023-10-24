import json

INSTRUCTION_OPCODES = "instructions-opcodes.json"

with open(INSTRUCTION_OPCODES, "r") as input_file:
    opcodes = json.load(input_file)

    for instruction, opcode in opcodes.items():
        print(f"{int(opcode, base=2)}: {instruction}")