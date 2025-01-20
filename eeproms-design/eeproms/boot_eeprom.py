from eeproms.eeprom import Eeprom
from eeproms.config import Config

import json

BOOT_INSTRUCTIONS = [
    "MOVATABSIMMZP",
    "0b00000001",
    "0b10011110",
    "MOVATABSIMMZP",
    "0b00000010",
    "0b10011111",
    "MOVATABSIMMZP",
    "0b00000011",
    "0b11101100",
    "HALT"
]

class BootEeprom(Eeprom):
    def __init__(self, config=Config()):
        super().__init__()
        self._config = config
        self._write_all()

    def _write_all(self):
        instructions_translation = json.load(open(self._config.get_instructions()))

        for address, instruction in enumerate(BOOT_INSTRUCTIONS):
            if instruction in instructions_translation:
                opcode = instructions_translation[instruction]["opcode"]
                opcode_num = int(opcode, 2)
                self.write(f"BOOT_{address}", address, opcode_num)
            else:
                value_num = int(instruction, 2)
                self.write(f"BOOT_{address}", address, value_num)

    def _reverse_bits(self, n, num_bits):
        result = 0
        for _ in range(num_bits):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result