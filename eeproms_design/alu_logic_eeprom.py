from enum import Enum
from eeprom import Eeprom

#
# INPUT : |A4|A3|A2|A1|A0|
# OUTPUT: |IO7|IO6|IO5|IO4|IO3|IO2|IO1|IO0|


class MultiplexerOutputEnum:
    CONST_ONE = 0b00000000
    CONST_MINUS_ONE = 0b00000001
    ARITHMETIC_RESULT = 0b00000010
    LOGIC_RESULT = 0b00000011
    XOR_RESULT = 0b00000100
    SHIFT_LEFT = 0b00000101
    SHIFT_RIGHT = 0b00000110


class InverseRegAEnum:
    INVERSE = 0b00001000
    NO_INVERSE = 0b00000000


class InverseRegBEnum:
    INVERSE = 0b00010000
    NO_INVERSE = 0b00000000


class ZeroRegAEnum:
    ZERO = 0b00000000
    NON_ZERO = 0b00100000


class ZeroRegBEnum:
    ZERO = 0b00000000
    NON_ZERO = 0b01000000


class InverseRegAOrRegBEnum:
    INVERSE = 0b10000000
    NO_INVERSE = 0b00000000


class AluLogicEeprom(Eeprom):



ALU_LOGIC = {
    'CONST_ZERO': (0b00000, [

    ]),
    'CONST_ONE': (0b00001, [
        
    ]),
    'CONST_MINUS_ONE': (0b00010, [
        
    ]),
    'REG_A': (0b00001, [
        
    ]),
    'REG_B': (0b00001, [
        
    ]),
    'MINUS_REG_A': (0b00001, [
        
    ]),
    'MINUS_REG_B': (0b00001, [
        
    ]),
    'REG_A_PLUS_REG_B': (0b00001, [
        
    ]),
    'REG_A_MINUS_REG_B': (0b00001, [
        
    ]),
    'REG_B_MINUS_REG_A': (0b00001, [
        
    ]),
    'NOT_REG_A': (0b00001, [
        
    ]),
    'NOT_REG_B': (0b00001, [
        
    ]),
    'REG_A_OR_REG_B': (0b00001, [
        
    ]),
    'REG_A_AND_REG_B': (0b00001, [
        
    ]),
    'REG_A_ARITHMETIC_SHIFT_LEFT': (0b00001, [
        
    ]),
    'REG_B_ARITHMETIC_SHIFT_LEFT': (0b00001, [
        
    ]),
    'REG_A_ARITHMETIC_SHIFT_RIGHT': (0b00001, [
        
    ]),
    'REG_B_ARITHMETIC_SHIFT_RIGHT': (0b00001, [
        
    ]),
    'REG_A_LOGIC_SHIFT_LEFT': (0b00001, [
        
    ]),
    'REG_B_LOGIC_SHIFT_LEFT': (0b00001, [
        
    ]),
    'REG_A_LOGIC_SHIFT_RIGHT': (0b00001, [
        
    ]),
    'REG_B_LOGIC_SHIFT_RIGHT': (0b00001, [

    ])
}
