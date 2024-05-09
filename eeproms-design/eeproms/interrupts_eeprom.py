from eeproms.eeprom import Eeprom

INTERRRUPT_SOLVE_ROUTINE_OPCODE = 0b11011000

class InterruptsEeprom(Eeprom):
    def __init__(self):
        super().__init__()
        self._write_all()

    def _write_all(self):
        for i in range(2**13):
            interrupts = i >> 8     # 5 highest bits
            opcode = i % (2**8)     # 8 lowest bits
            
            if interrupts == 0:
                self.write(f"INTERRUPTS_{i}", i, opcode)
            else:
                self.write(f"INTERRUPTS_{i}", i, INTERRRUPT_SOLVE_ROUTINE_OPCODE)
