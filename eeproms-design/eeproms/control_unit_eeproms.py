import json

from eeproms.eeprom import Eeprom
from eeproms.config import Config

ENTER_PROGRAM_TO_MEMORY_MSB = 1
EXECUTE_ENTERED_PROGRAM_MSB = 0

OPERATING_MODE_BITS_NUMBER = 1
INSTRUCTION_OPCODE_BITS_NUMBER = 8
MICROCODE_COUNTER_BITS_NUMBER = 4

PRINT = False

# FIXME: the new config does not contain these instructions
FETCH_MICROCODES = ["LOAD_PC_TO_MAR", "LOAD_MEM[MAR]_TO_IR_PC++"]
ENTER_PROGRAM_MICROCODES = ["DO_NOTHING", "LOAD_DATA_FROM_BUTTONS_TO_MAR_AND_MBR", "LOAD_MBR_TO_MEM[MAR]", "RST_MC"]
# ENTER_PROGRAM_MICROCODES = ["DO_NOTHING", "LOAD_DATA_FROM_BUS_TO_MAR_AND_MBR", "LOAD_MBR_TO_MEM[MAR]", "RST_MC"]

FLAGS_COUNT = 5
FLAG_NAMES_LUT = {
    'S': 'sign',
    'NS': 'sign',
    'P': 'parity',
    'NP': 'parity',
    'Z': 'zero',
    'NZ': 'zero',
    'C': 'carry',
    'NC': 'carry',
    'O': 'overflow',
    'NO': 'overflow'
}

FLAG_OFFSETS = {
    'sign': 0,
    'parity': 1,
    'zero': 2,
    'carry': 3,
    'overflow': 4
}


class ControlUnitEeproms:
    def __init__(self, config=Config()):
        self._exec_eeproms = {
            "A": Eeprom(),
            "B": Eeprom(),
            "C": Eeprom(),
            "D": Eeprom(),
            "E": Eeprom(),
            "F": Eeprom(),
        }
        self._eeproms = {name: eeprom for name, eeprom in self._exec_eeproms.items()}
        self._eeproms["BRANCH"] = Eeprom()
        self._config = config
        self._write_all()

    def get_eeprom(self, name):
        return self._eeproms[name]

    def _write_all(self):
        with open(self._config.get_instructions(), 'r') as input_file:
            instructions = json.load(input_file)

        with open(self._config.get_microcodes(), 'r') as input_file:
            microcodes = json.load(input_file)

        with open(self._config.get_signals(), 'r') as input_file:
            signals_identifiers = json.load(input_file)

        mode_opcode_to_enter = [{} for _ in range(2 ** (OPERATING_MODE_BITS_NUMBER + INSTRUCTION_OPCODE_BITS_NUMBER))]

        # Code for entering program to memory
        for opcode in range(0, 2 ** INSTRUCTION_OPCODE_BITS_NUMBER):
            branch = self._default_branch(opcode)
            mode_opcode_to_enter[ENTER_PROGRAM_TO_MEMORY_MSB * 2 ** INSTRUCTION_OPCODE_BITS_NUMBER + opcode] = {
                'name': f'ENTER_PROGRAM_{opcode}', 'microcodes': ENTER_PROGRAM_MICROCODES, 'branch': branch}

        # Code for executing entered program:
        for instruction_name, instruction in instructions.items():
            mode_opcode = (EXECUTE_ENTERED_PROGRAM_MSB * 2 ** INSTRUCTION_OPCODE_BITS_NUMBER +
                           int(instruction['opcode'], 2))
            # branch = self._generate_branch(instruction_name, instruction, instructions)   TODO: Fix this
            branch = self._default_branch(mode_opcode)
            mode_opcode_to_enter[mode_opcode] = {'name': instruction_name, 'microcodes': instruction['microcodes'],
                                                 'branch': branch}

        for i in range(len(mode_opcode_to_enter)):
            if len(mode_opcode_to_enter[i]) == 0:
                branch = self._default_branch(i & 0xFF)
                mode_opcode_to_enter[i] = {'name': f'ONLY_FETCH_{i}', 'microcodes': FETCH_MICROCODES, 'branch': branch}

        for opcode, instruction in enumerate(mode_opcode_to_enter):
            if PRINT:
                print(instruction['name'])

            for microcode_counter, microcode_name in enumerate(instruction['microcodes']):
                opcode_str = '0b' + bin(opcode)[2:].zfill(OPERATING_MODE_BITS_NUMBER + INSTRUCTION_OPCODE_BITS_NUMBER)
                description = instruction['name'] + '-' + str(microcode_counter) + '-' + microcode_name
                eeprom_input = f'{opcode_str}{bin(microcode_counter)[2:].zfill(MICROCODE_COUNTER_BITS_NUMBER)}'
                eeprom_outputs = {
                    "A": f'0b00000000',
                    "B": f'0b00000000',
                    "C": f'0b00000000',
                    "D": f'0b00000000',
                    "E": f'0b00000000',
                    "F": f'0b00000000'
                }

                if PRINT:
                    print(
                        f'  {microcode_name}\n  {opcode_str[2]} {opcode_str[3:].zfill(INSTRUCTION_OPCODE_BITS_NUMBER)} {bin(microcode_counter)[2:].zfill(MICROCODE_COUNTER_BITS_NUMBER)}',
                        end='  ')
                try:
                    signals = microcodes[microcode_name]
                except:
                    print(f"ERROR: {microcode_name} is not a defined microcode") # TODO: Fix this
                
                for signal_name, signal_id in signals_identifiers.items():
                    if PRINT:
                        print(f'{signal_id}: {signals[signal_name]}', end=' ')
                    eeprom_outputs[signal_id[0][0]] = self._set_char(eeprom_outputs[signal_id[0][0]],
                                                                     9 - int(signal_id[0][1]),
                                                                     str(signals[signal_name]))

                for eeprom_id, eeprom in self._eeproms.items():
                    if eeprom_id == "BRANCH":
                        continue
                    eeprom.write(description, int(eeprom_input, base=2), int(eeprom_outputs[eeprom_id], base=2))

                if PRINT:
                    print('')

            if (opcode & 0x100) == 0:  # Skip generating branch resolution for enter program opcodes
                branch = instruction['branch']
                (flag_mask, flag_values) = self._get_flag_bitmask_and_values(branch['flags'])
                for flags in range(0, (1 << FLAGS_COUNT)):
                    description = instruction['name'] + '-' + str(flags)
                    address = (opcode << FLAGS_COUNT) | flags
                    if flag_mask is None:
                        assert address < (1 << 13)
                        self._eeproms['BRANCH'].write(description, address, branch['taken'])
                    else:
                        if (flags & flag_mask) == flag_values:
                            self._eeproms['BRANCH'].write(description, address, branch['taken'])
                            print(flags, flags & flag_mask, flag_values, 'taken', branch['taken'])
                        else:
                            self._eeproms['BRANCH'].write(description, address, branch['not_taken'])
                            print(flags, flags & flag_mask, flag_values, 'not taken', branch['not_taken'])

            if PRINT:
                print('')

    def _set_char(self, word, position, character):
        res = word[:position] + character + word[(position + 1):]
        return res

    def _get_flag_bitmask_and_values(self, flags):
        print(flags)
        if len(flags) == 0:
            return (None, None)
        values = 0
        bitmask = 0
        for flag, state in flags.items():
            value = 1 if state else 0
            bitmask = bitmask | (1 << FLAG_OFFSETS[flag])
            values = values | (value << FLAG_OFFSETS[flag])
        print(flags, values, bitmask)
        return bitmask, values

    def _map_depend_on_flag(self, depend_on_flag):
        flags = {}
        on = False if depend_on_flag[0] == 'N' else True
        flags[FLAG_NAMES_LUT[depend_on_flag]] = on
        return flags

    def _generate_branch(self, instruction_name, instruction, instructions):
        depend_on_flag = instruction['depend-on-flag']
        flags = {} if depend_on_flag == '' else self._map_depend_on_flag(depend_on_flag)
        branch = instruction['branch']

        taken = not_taken = int(instruction['opcode'], 2)

        if branch is None:
            if len(flags) != 0:
                print(f"WARNING: {instruction_name} depends on flags, however it has a null branch config")
        else:
            try:
                taken = int(instructions[branch['taken']]['opcode'], 2)
                not_taken = int(instructions[branch['not-taken']]['opcode'], 2)
            except:
                print(f"ERROR: {instruction_name} has a branch to an unknown instruction")

        assert 0 <= taken <= 255, f"{instruction_name}"
        assert 0 <= not_taken <= 255, f"{instruction_name}"

        return {'flags': flags, 'taken': taken, 'not_taken': not_taken}

    def _default_branch(self, opcode):
        assert 0 <= opcode <= 255
        return {'flags': {}, 'taken': opcode, 'not_taken': opcode}
