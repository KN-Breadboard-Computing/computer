import json

from eeprom import Eeprom

MICROCODES_DESCRIPTION_FILENAME = 'microcodes.json'
INSTRUCTIONS_DESCRIPTION_FILENAME  = 'instructions.json'
INSTRUCTIONS_OPCODES_FILENAME = 'instructions-opcodes.json'
SIGNALS_IDENTIFIERS_FILENAME = 'signals-identifiers.json'

ENTER_PROGRAM_TO_MEMORY_MSB = 1
EXECUTE_ENTERED_PROGRAM_MSB = 0

OPERATING_MODE_BITS_NUMBER = 1
INSTRUCTION_OPCODE_BITS_NUMBER = 8
MICROCODE_COUNTER_BITS_NUMBER = 4

PRINT = False


class ControlUnitEeproms():
    def __init__(self):
        self._eeproms = {
            "A": Eeprom(),
            "B": Eeprom(),
            "C": Eeprom(),
            "D": Eeprom(),
            "E": Eeprom(),
            "F": Eeprom()
        }

        self._write_all()

    def get_eeeprom(self, name):
        return self._eeproms[name]

    def _write_all(self):
        with open(INSTRUCTIONS_DESCRIPTION_FILENAME, 'r') as input_file:
            instructions = json.load(input_file)
            
        with open(MICROCODES_DESCRIPTION_FILENAME, 'r') as input_file:
            microcodes = json.load(input_file)

        with open(INSTRUCTIONS_OPCODES_FILENAME, 'r') as input_file:
            instructions_opcodes = json.load(input_file)

        with open(SIGNALS_IDENTIFIERS_FILENAME, 'r') as input_file:
            signals_identifiers = json.load(input_file)

        mode_opcode_to_enter = [{} for _ in range(2**(OPERATING_MODE_BITS_NUMBER + INSTRUCTION_OPCODE_BITS_NUMBER))]

        # Code for entering program to memory
        for opcode in range(0, 2**INSTRUCTION_OPCODE_BITS_NUMBER):
            mode_opcode_to_enter[ENTER_PROGRAM_TO_MEMORY_MSB * 2**(INSTRUCTION_OPCODE_BITS_NUMBER) + opcode] = {'name': f'ENTER_PROGRAM_{opcode}', 'microcodes': instructions['ENTER_PROGRAM']}

        # Code for executing entered program:
        for instruction_name, instruction_steps in instructions.items():
            mode_opcode = EXECUTE_ENTERED_PROGRAM_MSB * 2**(INSTRUCTION_OPCODE_BITS_NUMBER) + int(instructions_opcodes[instruction_name], base=2)
            mode_opcode_to_enter[mode_opcode] = {'name': instruction_name, 'microcodes': instruction_steps}

        for i in range(len(mode_opcode_to_enter)):
            if len(mode_opcode_to_enter[i]) == 0:
                mode_opcode_to_enter[i] = {'name': f'ONLY_FETCH_{i}', 'microcodes': instructions['FETCH']}

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
                    print(f'  {microcode_name}\n  {opcode_str[2]} {opcode_str[3:].zfill(INSTRUCTION_OPCODE_BITS_NUMBER)} {bin(microcode_counter)[2:].zfill(MICROCODE_COUNTER_BITS_NUMBER)}', end='  ')
                signals = microcodes[microcode_name]

                for signal_name, signal_id in signals_identifiers.items():
                    if PRINT:
                        print(f'{signal_id}: {signals[signal_name]}', end=' ')
                    eeprom_outputs[signal_id[0]] = self._set_char(eeprom_outputs[signal_id[0]], 9 - int(signal_id[1]), str(signals[signal_name]))

                for eeprom_id, eeprom in self._eeproms.items():
                    eeprom.write(description, int(eeprom_input, base=2), int(eeprom_outputs[eeprom_id], base=2))
                    
                if PRINT:
                    print('')
            if PRINT:
                print('')


    def _set_char(self, word, position, character):
        res = word[:position] + character + word[(position+1):]
        return res

