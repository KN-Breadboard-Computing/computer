from eeproms_design.eeproms.eeprom import Eeprom
import json

ALU_LOGIC_DESCRIPTION_FILENAME = "alu-logic.json"

class AluLogicEeprom(Eeprom):
    def __init__(self):
        super().__init__()
        self._write_all()

    def _write_single(self, description, code, inverse_reg_a, inverse_reg_b, zero_reg_a, zero_reg_b,
                      inverse_or_result, multiplexer_output, config):
        word = 0b00000000

        if inverse_reg_a:
            word |= int(config['INVERSE_REG_A'], 2)

        if inverse_reg_b:
            word |= int(config['INVERSE_REG_B'], 2)

        if not zero_reg_a:
            word |= int(config['NON_ZERO_REG_A'], 2)

        if not zero_reg_b:
            word |= int(config['NON_ZERO_REG_B'], 2)

        if inverse_or_result:
            word |= int(config['INVERSE_OR_RESULT'], 2)

        word |= int(config['multiplexer-output'][multiplexer_output], 2)

        self.write(description, int(code, 2), word)

    def _write_all(self):
        with open(ALU_LOGIC_DESCRIPTION_FILENAME) as input_file:
            alu_desc = json.load(input_file)
            alu_config = alu_desc['config']
            alu_codes = alu_desc['codes']

        for key, value in alu_codes.items():
            self._write_single(key, 
                                value['CODE'],
                                value['INVERSE_REG_A'],
                                value['INVERSE_REG_B'],
                                value['ZERO_REG_A'],
                                value['ZERO_REG_B'],
                                value['INVERSE_OR_RESULT'],
                                value['MULTIPLEXER_OUTPUT'],
                                alu_config)
