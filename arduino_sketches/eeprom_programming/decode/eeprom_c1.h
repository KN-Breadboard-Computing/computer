#include "../defines.h"

#ifndef EEPROM_C_DECODE_1_H
#define EEPROM_C_DECODE_1_H

/*
| C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 |

-> C0 = LD MBR
-> C1 = WORD IN / ~WORD OUT
-> C2 = ~MEM IN
-> C3 = ~MEM OUT
-> C4 = ~OUT MBR
-> C5 = MEM PART
-> C6 = LD TMP HIGH
-> C7 = LD TMP LOW
*/

uint16_t NON_ZERO_MEMORY_SIZE = 124;
MemoryCell NON_ZERO_MEMORY[124] = {
  { 0b0000000000010, 0b00111000 }, // EMPTY - MICROSTEP 2
  { 0b0000000000011, 0b00111000 }, // EMPTY - MICROSTEP 3

  { 0b0000000010010, 0b00111000 }, // MOVAB - MICROSTEP 2
  { 0b0000000010011, 0b00111000 }, // MOVAB - MICROSTEP 3

  { 0b0000000100010, 0b00111000 }, // MOVBA - MICROSTEP 2
  { 0b0000000100011, 0b00111000 }, // MOVBA - MICROSTEP 3

  { 0b0000000110010, 0b00111000 }, // MOVAIMM - MICROSTEP 2
  { 0b0000000110011, 0b00101000 }, // MOVAIMM - MICROSTEP 3
  { 0b0000000110100, 0b00111000 }, // MOVAIMM - MICROSTEP 4

  { 0b0000001000010, 0b00111000 }, // MOVBIMM - MICROSTEP 2
  { 0b0000001000011, 0b00101000 }, // MOVBIMM - MICROSTEP 3
  { 0b0000001000100, 0b00111000 }, // MOVBIMM - MICROSTEP 4

  { 0b0000001010010, 0b00111000 }, // MOVAABS - MICROSTEP 2
  { 0b0000001010011, 0b00101010 }, // MOVAABS - MICROSTEP 3
  { 0b0000001010100, 0b00111000 }, // MOVAABS - MICROSTEP 4
  { 0b0000001010101, 0b00101001 }, // MOVAABS - MICROSTEP 5
  { 0b0000001010110, 0b00111000 }, // MOVAABS - MICROSTEP 6
  { 0b0000001010111, 0b00101000 }, // MOVAABS - MICROSTEP 7
  { 0b0000001011000, 0b00111000 }, // MOVAABS - MICROSTEP 8

  { 0b0000001100010, 0b00111000 }, // MOVBABS - MICROSTEP 2
  { 0b0000001100011, 0b00101010 }, // MOVBABS - MICROSTEP 3
  { 0b0000001100100, 0b00111000 }, // MOVBABS - MICROSTEP 4
  { 0b0000001100101, 0b00101001 }, // MOVBABS - MICROSTEP 5
  { 0b0000001100110, 0b00111000 }, // MOVBABS - MICROSTEP 6
  { 0b0000001100111, 0b00101000 }, // MOVBABS - MICROSTEP 7
  { 0b0000001101000, 0b00111000 }, // MOVBABS - MICROSTEP 8

  { 0b0000001110010, 0b11111000 }, // MOVABSA - MICROSTEP 2
  { 0b0000001110011, 0b00101010 }, // MOVABSA - MICROSTEP 3
  { 0b0000001110100, 0b00111000 }, // MOVABSA - MICROSTEP 4
  { 0b0000001110101, 0b00101001 }, // MOVABSA - MICROSTEP 5
  { 0b0000001110110, 0b00111000 }, // MOVABSA - MICROSTEP 6
  { 0b0000001110111, 0b01010000 }, // MOVABSA - MICROSTEP 7
  { 0b0000001111000, 0b00111000 }, // MOVABSA - MICROSTEP 8

  { 0b0000010000010, 0b11111000 }, // MOVABSB - MICROSTEP 2
  { 0b0000010000011, 0b00101010 }, // MOVABSB - MICROSTEP 3
  { 0b0000010000100, 0b00111000 }, // MOVABSB - MICROSTEP 4
  { 0b0000010000101, 0b00101001 }, // MOVABSB - MICROSTEP 5
  { 0b0000010000110, 0b00111000 }, // MOVABSB - MICROSTEP 6
  { 0b0000010000111, 0b01010000 }, // MOVABSB - MICROSTEP 7
  { 0b0000010001000, 0b00111000 }, // MOVABSB - MICROSTEP 8

  { 0b0000010010010, 0b00111000 }, // MOVABSIMM - MICROSTEP 2
  { 0b0000010010011, 0b00101010 }, // MOVABSIMM - MICROSTEP 3
  { 0b0000010010100, 0b00111000 }, // MOVABSIMM - MICROSTEP 4
  { 0b0000010010101, 0b00101001 }, // MOVABSIMM - MICROSTEP 5
  { 0b0000010010110, 0b00111000 }, // MOVABSIMM - MICROSTEP 6
  { 0b0000010010111, 0b10101000 }, // MOVABSIMM - MICROSTEP 7
  { 0b0000010011000, 0b00111000 }, // MOVABSIMM - MICROSTEP 8
  { 0b0000010011001, 0b01010000 }, // MOVABSIMM - MICROSTEP 9
  { 0b0000010011010, 0b00111000 }, // MOVABSIMM - MICROSTEP 10

  { 0b0000010100010, 0b00111000 }, // MOVAF - MICROSTEP 2
  { 0b0000010100011, 0b00111000 }, // MOVAF - MICROSTEP 3

  { 0b0000010110010, 0b00111000 }, // MOVBF - MICROSTEP 2
  { 0b0000010110011, 0b00111000 }, // MOVBF - MICROSTEP 3

  { 0b0000011000010, 0b11111000 }, // PUSHA - MICROSTEP 2
  { 0b0000011000011, 0b01010000 }, // PUSHA - MICROSTEP 3
  { 0b0000011000100, 0b00111000 }, // PUSHA - MICROSTEP 4

  { 0b0000011010010, 0b11111000 }, // PUSHB - MICROSTEP 2
  { 0b0000011010011, 0b01010000 }, // PUSHB - MICROSTEP 3
  { 0b0000011010100, 0b00111000 }, // PUSHB - MICROSTEP 4

  { 0b0000011100010, 0b00111000 }, // PUSHIMM - MICROSTEP 2
  { 0b0000011100011, 0b10101000 }, // PUSHIMM - MICROSTEP 3
  { 0b0000011100100, 0b00111000 }, // PUSHIMM - MICROSTEP 4
  { 0b0000011100101, 0b01010000 }, // PUSHIMM - MICROSTEP 5
  { 0b0000011100110, 0b00111000 }, // PUSHIMM - MICROSTEP 6

  { 0b0000011110010, 0b00111000 }, // PUSHABS - MICROSTEP 2
  { 0b0000011110011, 0b00101010 }, // PUSHABS - MICROSTEP 3
  { 0b0000011110100, 0b00111000 }, // PUSHABS - MICROSTEP 4
  { 0b0000011110101, 0b00101001 }, // PUSHABS - MICROSTEP 5
  { 0b0000011110110, 0b00111000 }, // PUSHABS - MICROSTEP 6
  { 0b0000011110111, 0b10101000 }, // PUSHABS - MICROSTEP 7
  { 0b0000011111000, 0b00111000 }, // PUSHABS - MICROSTEP 8
  { 0b0000011111001, 0b01010000 }, // PUSHABS - MICROSTEP 9
  { 0b0000011111010, 0b00111000 }, // PUSHABS - MICROSTEP 10

  { 0b0000100000010, 0b00111000 }, // POPA - MICROSTEP 2
  { 0b0000100000011, 0b00101000 }, // POPA - MICROSTEP 3
  { 0b0000100000100, 0b00111000 }, // POPA - MICROSTEP 4

  { 0b0000100010010, 0b00111000 }, // POPB - MICROSTEP 2
  { 0b0000100010011, 0b00101000 }, // POPB - MICROSTEP 3
  { 0b0000100010100, 0b00111000 }, // POPB - MICROSTEP 4

  { 0b0000100100010, 0b00111000 }, // POPMEM - MICROSTEP 2
  { 0b0000100100011, 0b00101010 }, // POPMEM - MICROSTEP 3
  { 0b0000100100100, 0b00111000 }, // POPMEM - MICROSTEP 4
  { 0b0000100100101, 0b00101001 }, // POPMEM - MICROSTEP 5
  { 0b0000100100110, 0b00111000 }, // POPMEM - MICROSTEP 6
  { 0b0000100100111, 0b10101000 }, // POPMEM - MICROSTEP 7
  { 0b0000100101000, 0b00111000 }, // POPMEM - MICROSTEP 8
  { 0b0000100101001, 0b01010000 }, // POPMEM - MICROSTEP 9
  { 0b0000100101010, 0b00111000 }, // POPMEM - MICROSTEP 10

  { 0b0000100110010, 0b00111000 }, // JMPABS - MICROSTEP 2
  { 0b0000100110011, 0b00101010 }, // JMPABS - MICROSTEP 3
  { 0b0000100110100, 0b00111000 }, // JMPABS - MICROSTEP 4
  { 0b0000100110101, 0b00101001 }, // JMPABS - MICROSTEP 5
  { 0b0000100110110, 0b00111000 }, // JMPABS - MICROSTEP 6
  { 0b0000100110111, 0b00111000 }, // JMPABS - MICROSTEP 7

  { 0b0000101000010, 0b00111000 }, // JMPFUN - MICROSTEP 2
  { 0b0000101000011, 0b10111000 }, // JMPFUN - MICROSTEP 3
  { 0b0000101000100, 0b01010000 }, // JMPFUN - MICROSTEP 4
  { 0b0000101000101, 0b10111000 }, // JMPFUN - MICROSTEP 5
  { 0b0000101000110, 0b01010000 }, // JMPFUN - MICROSTEP 6
  { 0b0000101000111, 0b00111000 }, // JMPFUN - MICROSTEP 7
  { 0b0000101001000, 0b00101010 }, // JMPFUN - MICROSTEP 8
  { 0b0000101001001, 0b00111000 }, // JMPFUN - MICROSTEP 9
  { 0b0000101001010, 0b00101001 }, // JMPFUN - MICROSTEP 10
  { 0b0000101001011, 0b00111000 }, // JMPFUN - MICROSTEP 11
  { 0b0000101001100, 0b00111000 }, // JMPFUN - MICROSTEP 12

  { 0b0000101010010, 0b00111000 }, // JMPBACK - MICROSTEP 2
  { 0b0000101010011, 0b00101010 }, // JMPBACK - MICROSTEP 3
  { 0b0000101010100, 0b00111000 }, // JMPBACK - MICROSTEP 4
  { 0b0000101010101, 0b00101001 }, // JMPBACK - MICROSTEP 5
  { 0b0000101010110, 0b00111000 }, // JMPBACK - MICROSTEP 6
  { 0b0000101010111, 0b00111000 }, // JMPBACK - MICROSTEP 7
  { 0b0000101011000, 0b00111000 }, // JMPBACK - MICROSTEP 8

  { 0b0000101100010, 0b00111000 }, // ADDA - MICROSTEP 2
  { 0b0000101100011, 0b00111000 }, // ADDA - MICROSTEP 3

  { 0b0000101110010, 0b00111000 }, // ADDB - MICROSTEP 2
  { 0b0000101110011, 0b00111000 }, // ADDB - MICROSTEP 3

  { 0b0000110000010, 0b00111000 }, // ADDMEM - MICROSTEP 2
  { 0b0000110000011, 0b00101010 }, // ADDMEM - MICROSTEP 3
  { 0b0000110000100, 0b00111000 }, // ADDMEM - MICROSTEP 4
  { 0b0000110000101, 0b00101001 }, // ADDMEM - MICROSTEP 5
  { 0b0000110000110, 0b10111000 }, // ADDMEM - MICROSTEP 6
  { 0b0000110000111, 0b00111000 }, // ADDMEM - MICROSTEP 7
  { 0b0000110001000, 0b01010000 }, // ADDMEM - MICROSTEP 8
  { 0b0000110001001, 0b00111000 }  // ADDMEM - MICROSTEP 9
};

#endif // EEPROM_C_DECODE_1_H