from eeprom import Eeprom


class MultiplexerOutput:
    CONST_ONE = 0b00000000
    CONST_MINUS_ONE = 0b00000001
    ARITHMETIC_RESULT = 0b00000010
    LOGIC_RESULT = 0b00000011
    XOR_RESULT = 0b00000100
    SHIFT_LEFT = 0b00000101
    SHIFT_RIGHT_ARITHMETIC = 0b00000110
    SHIFT_RIGHT_LOGIC = 0b00000111


class SignalMask:
    INVERSE_REG_A = 0b00001000
    INVERSE_REG_B = 0b00010000
    NON_ZERO_REG_A = 0b00100000
    NON_ZERO_REG_B = 0b01000000
    INVERSE_OR_RESULT = 0b10000000


class AluLogicEeprom(Eeprom):
    def __init__(self):
        super().__init__()
        self._write_all()

    def _write_single(self, description, code, inverse_reg_a, inverse_reg_b, zero_reg_a, zero_reg_b,
                      inverse_or_result, multiplexer_output):
        word = 0b00000000

        if inverse_reg_a:
            word |= SignalMask.INVERSE_REG_A

        if inverse_reg_b:
            word |= SignalMask.INVERSE_REG_B

        if not zero_reg_a:
            word |= SignalMask.NON_ZERO_REG_A

        if not zero_reg_b:
            word |= SignalMask.NON_ZERO_REG_B

        if inverse_or_result:
            word |= SignalMask.INVERSE_OR_RESULT

        word |= multiplexer_output

        self.write(description, code, word)

    def _write_all(self):
        self._write_single(description='CONST_ZERO', code=0b0000000000000, 
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='CONST_ONE', code=0b0000000000001,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.CONST_ONE)

        self._write_single(description='CONST_MINUS_ONE', code=0b0000000000010,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.CONST_MINUS_ONE)

        self._write_single(description='REG_A', code=0b0000000000011,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='REG_B', code=0b0000000000100,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='MINUS_REG_A', code=0b0000000000101,
                           inverse_reg_a=True, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='MINUS_REG_B', code=0b0000000000110,
                           inverse_reg_a=False, inverse_reg_b=True, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='REG_A_PLUS_REG_B', code=0b0000000000111,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='REG_A_MINUS_REG_B', code=0b0000000001000,
                           inverse_reg_a=False, inverse_reg_b=True, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='REG_B_MINUS_REG_A', code=0b0000000001001,
                           inverse_reg_a=True, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.ARITHMETIC_RESULT)

        self._write_single(description='NOT_REG_A', code=0b0000000001010,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=True, multiplexer_output=MultiplexerOutput.LOGIC_RESULT)

        self._write_single(description='NOT_REG_B', code=0b0000000001011,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=True, multiplexer_output=MultiplexerOutput.LOGIC_RESULT)

        self._write_single(description='REG_A_OR_REG_B', code=0b0000000001100,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.LOGIC_RESULT)

        self._write_single(description='REG_A_AND_REG_B', code=0b0000000001101,
                           inverse_reg_a=True, inverse_reg_b=True, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=True, multiplexer_output=MultiplexerOutput.LOGIC_RESULT)

        self._write_single(description='REG_A_XOR_REG_B', code=0b0000000001110,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.XOR_RESULT)

        self._write_single(description='ARITHMETIC_RIGHT_SHIFT_REG_A', code=0b0000000001111,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_RIGHT_ARITHMETIC)

        self._write_single(description='ARITHMETIC_RIGHT_SHIFT_REG_B', code=0b0000000010000,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_RIGHT_ARITHMETIC)

        self._write_single(description='ARITHMETIC_LEFT_SHIFT_REG_A', code=0b0000000010001,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_LEFT)

        self._write_single(description='ARITHMETIC_LEFT_SHIFT_REG_B', code=0b0000000010010,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_LEFT)

        self._write_single(description='LOGIC_RIGHT_SHIFT_REG_A', code=0b0000000010011,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_RIGHT_LOGIC)

        self._write_single(description='LOGIC_RIGHT_SHIFT_REG_B', code=0b0000000010100,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_RIGHT_LOGIC)

        self._write_single(description='LOGIC_LEFT_SHIFT_REG_A', code=0b0000000010101,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=False, zero_reg_b=True,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_LEFT)

        self._write_single(description='LOGIC_LEFT_SHIFT_REG_B', code=0b0000000010110,
                           inverse_reg_a=False, inverse_reg_b=False, zero_reg_a=True, zero_reg_b=False,
                           inverse_or_result=False, multiplexer_output=MultiplexerOutput.SHIFT_LEFT)
