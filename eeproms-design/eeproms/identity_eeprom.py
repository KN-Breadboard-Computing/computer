from eeproms.eeprom import Eeprom


class IdentityEeprom(Eeprom):
    def __init__(self):
        super().__init__()
        self._write_all()

    def _write_all(self):
        for i in range(2**13):
            self.write(f"IDENTITY_{i}", i, i % (2**8))
