#include "defines.h"

#ifndef CONTROL_UNIT_EEPROM_B2_H
#define CONTROL_UNIT_EEPROM_B2_H

/*
| B0 | B1 | B2 | B3 | B4 | B5 | B6 | B7 |

-> B0 = PC++
-> B1 = ~LOAD PC
-> B2 = ~OUT PC
-> B3 = STC++ / ~STC--
-> B4 = STC TICK
-> B5 = ~LOAD STC
-> B6 = ~OUT STC
-> B7 = LD MAR
*/

uint16_t NON_ZERO_MEMORY_SIZE = 147;
MemoryCell NON_ZERO_MEMORY[147] = {
  /*
  { 0b0000000000000, 0b01000111 },  // EMPTY - MICROSTEP 0
  { 0b0000000000001, 0b11100110 },  // EMPTY - MICROSTEP 1
  { 0b0000000000010, 0b01100110 },  // EMPTY - MICROSTEP 2
  { 0b0000000000011, 0b01100110 },  // EMPTY - MICROSTEP 3

  { 0b0000000010000, 0b01000111 },  // MOVAB - MICROSTEP 0
  { 0b0000000010001, 0b11100110 },  // MOVAB - MICROSTEP 1
  { 0b0000000010010, 0b01100110 },  // MOVAB - MICROSTEP 2
  { 0b0000000010011, 0b01100110 },  // MOVAB - MICROSTEP 3

  { 0b0000000100000, 0b01000111 },  // MOVBA - MICROSTEP 0
  { 0b0000000100001, 0b11100110 },  // MOVBA - MICROSTEP 1
  { 0b0000000100010, 0b01100110 },  // MOVBA - MICROSTEP 2
  { 0b0000000100011, 0b01100110 },  // MOVBA - MICROSTEP 3

  { 0b0000000110000, 0b01000111 },  // MOVAIMM - MICROSTEP 0
  { 0b0000000110001, 0b11100110 },  // MOVAIMM - MICROSTEP 1
  { 0b0000000110010, 0b01000111 },  // MOVAIMM - MICROSTEP 2
  { 0b0000000110011, 0b01100110 },  // MOVAIMM - MICROSTEP 3
  { 0b0000000110100, 0b01100110 },  // MOVAIMM - MICROSTEP 4

  { 0b0000001000000, 0b01000111 },  // MOVBIMM - MICROSTEP 0
  { 0b0000001000001, 0b11100110 },  // MOVBIMM - MICROSTEP 1
  { 0b0000001000010, 0b01000111 },  // MOVBIMM - MICROSTEP 2
  { 0b0000001000011, 0b01100110 },  // MOVBIMM - MICROSTEP 3
  { 0b0000001000100, 0b01100110 },  // MOVBIMM - MICROSTEP 4

  { 0b0000001010000, 0b01000111 },  // MOVAABS - MICROSTEP 0
  { 0b0000001010001, 0b11100110 },  // MOVAABS - MICROSTEP 1
  { 0b0000001010010, 0b01000111 },  // MOVAABS - MICROSTEP 2
  { 0b0000001010011, 0b11100110 },  // MOVAABS - MICROSTEP 3
  { 0b0000001010100, 0b01000111 },  // MOVAABS - MICROSTEP 4
  { 0b0000001010101, 0b11100110 },  // MOVAABS - MICROSTEP 5
  { 0b0000001010110, 0b01100111 },  // MOVAABS - MICROSTEP 6
  { 0b0000001010111, 0b01100110 },  // MOVAABS - MICROSTEP 7
  { 0b0000001011000, 0b01100110 },  // MOVAABS - MICROSTEP 8

  { 0b0000001100000, 0b01000111 },  // MOVBABS - MICROSTEP 0
  { 0b0000001100001, 0b11100110 },  // MOVBABS - MICROSTEP 1
  { 0b0000001100010, 0b01000111 },  // MOVBABS - MICROSTEP 2
  { 0b0000001100011, 0b11100110 },  // MOVBABS - MICROSTEP 3
  { 0b0000001100100, 0b01000111 },  // MOVBABS - MICROSTEP 4
  { 0b0000001100101, 0b11100110 },  // MOVBABS - MICROSTEP 5
  { 0b0000001100110, 0b01100111 },  // MOVBABS - MICROSTEP 6
  { 0b0000001100111, 0b01100110 },  // MOVBABS - MICROSTEP 7
  { 0b0000001101000, 0b01100110 },  // MOVBABS - MICROSTEP 8

  { 0b0000001110000, 0b01000111 },  // MOVABSA - MICROSTEP 0
  { 0b0000001110001, 0b11100110 },  // MOVABSA - MICROSTEP 1
  { 0b0000001110010, 0b01000111 },  // MOVABSA - MICROSTEP 2
  { 0b0000001110011, 0b11100110 },  // MOVABSA - MICROSTEP 3
  { 0b0000001110100, 0b01000111 },  // MOVABSA - MICROSTEP 4
  { 0b0000001110101, 0b11100110 },  // MOVABSA - MICROSTEP 5
  { 0b0000001110110, 0b01100111 },  // MOVABSA - MICROSTEP 6
  { 0b0000001110111, 0b01100110 },  // MOVABSA - MICROSTEP 7
  { 0b0000001111000, 0b01100110 },  // MOVABSA - MICROSTEP 8

  { 0b0000010000000, 0b01000111 },  // MOVABSB - MICROSTEP 0
  { 0b0000010000001, 0b11100110 },  // MOVABSB - MICROSTEP 1
  { 0b0000010000010, 0b01000111 },  // MOVABSB - MICROSTEP 2
  { 0b0000010000011, 0b11100110 },  // MOVABSB - MICROSTEP 3
  { 0b0000010000100, 0b01000111 },  // MOVABSB - MICROSTEP 4
  { 0b0000010000101, 0b11100110 },  // MOVABSB - MICROSTEP 5
  { 0b0000010000110, 0b01100111 },  // MOVABSB - MICROSTEP 6
  { 0b0000010000111, 0b01100110 },  // MOVABSB - MICROSTEP 7
  { 0b0000010001000, 0b01100110 },  // MOVABSB - MICROSTEP 8

  { 0b0000010010000, 0b01000111 },  // MOVABSIMM - MICROSTEP 0
  { 0b0000010010001, 0b11100110 },  // MOVABSIMM - MICROSTEP 1
  { 0b0000010010010, 0b01000111 },  // MOVABSIMM - MICROSTEP 2
  { 0b0000010010011, 0b11100110 },  // MOVABSIMM - MICROSTEP 3
  { 0b0000010010100, 0b01000111 },  // MOVABSIMM - MICROSTEP 4
  { 0b0000010010101, 0b11100110 },  // MOVABSIMM - MICROSTEP 5
  { 0b0000010010110, 0b01000111 },  // MOVABSIMM - MICROSTEP 6
  { 0b0000010010111, 0b11100110 },  // MOVABSIMM - MICROSTEP 7
  { 0b0000010011000, 0b01100111 },  // MOVABSIMM - MICROSTEP 8
  { 0b0000010011001, 0b01100110 },  // MOVABSIMM - MICROSTEP 9
  { 0b0000010011010, 0b01100110 },  // MOVABSIMM - MICROSTEP 10

  { 0b0000010100000, 0b01000111 },  // MOVAF - MICROSTEP 0
  { 0b0000010100001, 0b11100110 },  // MOVAF - MICROSTEP 1
  { 0b0000010100010, 0b01100110 },  // MOVAF - MICROSTEP 2
  { 0b0000010100011, 0b01100110 },  // MOVAF - MICROSTEP 3

  { 0b0000010110000, 0b01000111 },  // MOVBF - MICROSTEP 0
  { 0b0000010110001, 0b11100110 },  // MOVBF - MICROSTEP 1
  { 0b0000010110010, 0b01100110 },  // MOVBF - MICROSTEP 2
  { 0b0000010110011, 0b01100110 },  // MOVBF - MICROSTEP 3

  { 0b0000011000000, 0b01000111 },  // PUSHA - MICROSTEP 0
  { 0b0000011000001, 0b11100110 },  // PUSHA - MICROSTEP 1
  { 0b0000011000010, 0b01100101 },  // PUSHA - MICROSTEP 2
  { 0b0000011000011, 0b01101110 },  // PUSHA - MICROSTEP 3
  { 0b0000011000100, 0b01100110 },  // PUSHA - MICROSTEP 4

  { 0b0000011010000, 0b01000111 },  // PUSHB - MICROSTEP 0
  { 0b0000011010001, 0b11100110 },  // PUSHB - MICROSTEP 1
  { 0b0000011010010, 0b01100101 },  // PUSHB - MICROSTEP 2
  { 0b0000011010011, 0b01101110 },  // PUSHB - MICROSTEP 3
  { 0b0000011010100, 0b01100110 },  // PUSHB - MICROSTEP 4

  { 0b0000011100000, 0b01000111 },  // PUSHIMM - MICROSTEP 0
  { 0b0000011100001, 0b11100110 },  // PUSHIMM - MICROSTEP 1
  { 0b0000011100010, 0b01000111 },  // PUSHIMM - MICROSTEP 2
  { 0b0000011100011, 0b11100110 },  // PUSHIMM - MICROSTEP 3
  { 0b0000011100100, 0b01100101 },  // PUSHIMM - MICROSTEP 4
  { 0b0000011100101, 0b01101110 },  // PUSHIMM - MICROSTEP 5
  { 0b0000011100110, 0b01100110 },  // PUSHIMM - MICROSTEP 6

  { 0b0000011110000, 0b01000111 },  // PUSHABS - MICROSTEP 0
  { 0b0000011110001, 0b11100110 },  // PUSHABS - MICROSTEP 1
  { 0b0000011110010, 0b01000111 },  // PUSHABS - MICROSTEP 2
  { 0b0000011110011, 0b11100110 },  // PUSHABS - MICROSTEP 3
  { 0b0000011110100, 0b01000111 },  // PUSHABS - MICROSTEP 4
  { 0b0000011110101, 0b11100110 },  // PUSHABS - MICROSTEP 5
  { 0b0000011110110, 0b01100111 },  // PUSHABS - MICROSTEP 6
  { 0b0000011110111, 0b01100110 },  // PUSHABS - MICROSTEP 7
  { 0b0000011111000, 0b01100101 },  // PUSHABS - MICROSTEP 8
  { 0b0000011111001, 0b01101110 },  // PUSHABS - MICROSTEP 9
  { 0b0000011111010, 0b01100110 },  // PUSHABS - MICROSTEP 10

  { 0b0000100000000, 0b01000111 },  // POPA - MICROSTEP 0
  { 0b0000100000001, 0b11100110 },  // POPA - MICROSTEP 1
  { 0b0000100000010, 0b01100101 },  // POPA - MICROSTEP 2
  { 0b0000100000011, 0b01100110 },  // POPA - MICROSTEP 3
  { 0b0000100000100, 0b01100110 },  // POPA - MICROSTEP 4

  { 0b0000100010000, 0b01000111 },  // POPB - MICROSTEP 0
  { 0b0000100010001, 0b11100110 },  // POPB - MICROSTEP 1
  { 0b0000100010010, 0b01100101 },  // POPB - MICROSTEP 2
  { 0b0000100010011, 0b01100110 },  // POPB - MICROSTEP 3
  { 0b0000100010100, 0b01100110 },  // POPB - MICROSTEP 4

  { 0b0000100100000, 0b01000111 },  // POPMEM - MICROSTEP 0
  { 0b0000100100001, 0b11100110 },  // POPMEM - MICROSTEP 1
  { 0b0000100100010, 0b01000111 },  // POPMEM - MICROSTEP 2
  { 0b0000100100011, 0b11100110 },  // POPMEM - MICROSTEP 3
  { 0b0000100100100, 0b01000111 },  // POPMEM - MICROSTEP 4
  { 0b0000100100101, 0b11100110 },  // POPMEM - MICROSTEP 5
  { 0b0000100100110, 0b01100101 },  // POPMEM - MICROSTEP 6
  { 0b0000100100111, 0b01100110 },  // POPMEM - MICROSTEP 7
  { 0b0000100101000, 0b01100111 },  // POPMEM - MICROSTEP 8
  { 0b0000100101001, 0b01100110 },  // POPMEM - MICROSTEP 9
  { 0b0000100101010, 0b01100110 },  // POPMEM - MICROSTEP 10

  { 0b0000100110000, 0b01000111 },  // JMPABS - MICROSTEP 0
  { 0b0000100110001, 0b11100110 },  // JMPABS - MICROSTEP 1
  { 0b0000100110010, 0b01000111 },  // JMPABS - MICROSTEP 2
  { 0b0000100110011, 0b11100110 },  // JMPABS - MICROSTEP 3
  { 0b0000100110100, 0b01000111 },  // JMPABS - MICROSTEP 4
  { 0b0000100110101, 0b11100110 },  // JMPABS - MICROSTEP 5
  { 0b0000100110110, 0b00100110 },  // JMPABS - MICROSTEP 6
  { 0b0000100110111, 0b01100110 },  // JMPABS - MICROSTEP 7

  { 0b0000101000000, 0b01000111 },  // JMPFUN - MICROSTEP 0
  { 0b0000101000001, 0b11100110 },  // JMPFUN - MICROSTEP 1
  { 0b0000101000010, 0b01000110 },  // JMPFUN - MICROSTEP 2
  { 0b0000101000011, 0b01100101 },  // JMPFUN - MICROSTEP 3
  { 0b0000101000100, 0b01101110 },  // JMPFUN - MICROSTEP 4
  { 0b0000101000101, 0b01100101 },  // JMPFUN - MICROSTEP 5
  { 0b0000101000110, 0b01101110 },  // JMPFUN - MICROSTEP 6
  { 0b0000101000111, 0b01000111 },  // JMPFUN - MICROSTEP 7
  { 0b0000101001000, 0b11100110 },  // JMPFUN - MICROSTEP 8
  { 0b0000101001001, 0b01000111 },  // JMPFUN - MICROSTEP 9
  { 0b0000101001010, 0b11100110 },  // JMPFUN - MICROSTEP 10
  { 0b0000101001011, 0b00100110 },  // JMPFUN - MICROSTEP 11
  { 0b0000101001100, 0b01100110 },  // JMPFUN - MICROSTEP 12

  { 0b0000101010000, 0b01000111 },  // JMPBACK - MICROSTEP 0
  { 0b0000101010001, 0b11100110 },  // JMPBACK - MICROSTEP 1
  { 0b0000101010010, 0b01100101 },  // JMPBACK - MICROSTEP 2
  { 0b0000101010011, 0b01111110 },  // JMPBACK - MICROSTEP 3
  { 0b0000101010100, 0b01100101 },  // JMPBACK - MICROSTEP 4
  { 0b0000101010101, 0b01111110 },  // JMPBACK - MICROSTEP 5
  { 0b0000101010110, 0b00100110 },  // JMPBACK - MICROSTEP 6
  { 0b0000101010111, 0b11100110 },  // JMPBACK - MICROSTEP 7
  { 0b0000101011000, 0b01100110 },  // JMPBACK - MICROSTEP 8
  */
  
  { 0b0000101100000, 0b01000111 },  // ADDA - MICROSTEP 0
  { 0b0000101100001, 0b11100110 },  // ADDA - MICROSTEP 1
  { 0b0000101100010, 0b01100110 },  // ADDA - MICROSTEP 2
  { 0b0000101100011, 0b01100110 },  // ADDA - MICROSTEP 3

  { 0b0000101110000, 0b01000111 },  // ADDB - MICROSTEP 0
  { 0b0000101110001, 0b11100110 },  // ADDB - MICROSTEP 1
  { 0b0000101110010, 0b01100110 },  // ADDB - MICROSTEP 2
  { 0b0000101110011, 0b01100110 },  // ADDB - MICROSTEP 3

  { 0b0000110000000, 0b01000111 },  // ADDMEM - MICROSTEP 0
  { 0b0000110000001, 0b11100110 },  // ADDMEM - MICROSTEP 1
  { 0b0000110000010, 0b01000111 },  // ADDMEM - MICROSTEP 2
  { 0b0000110000011, 0b11100110 },  // ADDMEM - MICROSTEP 3
  { 0b0000110000100, 0b01000111 },  // ADDMEM - MICROSTEP 4
  { 0b0000110000101, 0b11100110 },  // ADDMEM - MICROSTEP 5
  { 0b0000110000110, 0b01100110 },  // ADDMEM - MICROSTEP 6
  { 0b0000110000111, 0b01100111 },  // ADDMEM - MICROSTEP 7
  { 0b0000110001000, 0b01100110 },  // ADDMEM - MICROSTEP 8
  { 0b0000110001001, 0b01100110 },  // ADDMEM - MICROSTEP 9

  { 0b0000110010000, 0b01000111 },  // SUBABA - MICROSTEP 0
  { 0b0000110010001, 0b11100110 },  // SUBABA - MICROSTEP 1
  { 0b0000110010010, 0b01100110 },  // SUBABA - MICROSTEP 2

  { 0b0000110100000, 0b01000111 },  // SUBABB - MICROSTEP 0
  { 0b0000110100001, 0b11100110 },  // SUBABB - MICROSTEP 1
  { 0b0000110100010, 0b01100110 },  // SUBABB - MICROSTEP 2 

  { 0b0000110110000, 0b01000111 },  // SUBABMEM - MICROSTEP 0
  { 0b0000110110001, 0b11100110 },  // SUBABMEM - MICROSTEP 1
  { 0b0000110110010, 0b01000111 },  // SUBABMEM - MICROSTEP 2
  { 0b0000110110011, 0b11100110 },  // SUBABMEM - MICROSTEP 3

  { 0b0000111000000, 0b01000111 },  // SUBBAA - MICROSTEP 0
  { 0b0000111000001, 0b11100110 },  // SUBBAA - MICROSTEP 1
  { 0b0000111000010, 0b01100110 },  // SUBBAA - MICROSTEP 2

  { 0b0000111010000, 0b01000111 },  // SUBBAB - MICROSTEP 0
  { 0b0000111010001, 0b11100110 },  // SUBBAB - MICROSTEP 1
  { 0b0000111010010, 0b01100110 },  // SUBBAB - MICROSTEP 2

  { 0b0000111100000, 0b01000111 },  // SUBBAMEM - MICROSTEP 0
  { 0b0000111100001, 0b11100110 },  // SUBBAMEM - MICROSTEP 1
  { 0b0000111100010, 0b01000111 },  // SUBBAMEM - MICROSTEP 2
  { 0b0000111100011, 0b11100110 },  // SUBBAMEM - MICROSTEP 3

  { 0b0000111110000, 0b01000111 },  // ORA - MICROSTEP 0
  { 0b0000111110001, 0b11100110 },  // ORA - MICROSTEP 1
  { 0b0000111110010, 0b01100110 },  // ORA - MICROSTEP 2

  { 0b0001000000000, 0b01000111 },  // ORB - MICROSTEP 0
  { 0b0001000000001, 0b11100110 },  // ORB - MICROSTEP 1
  { 0b0001000000010, 0b01100110 },  // ORB - MICROSTEP 2

  { 0b0001000010000, 0b01000111 },  // ORMEM - MICROSTEP 0
  { 0b0001000010001, 0b11100110 },  // ORMEM - MICROSTEP 1
  { 0b0001000010010, 0b01000111 },  // ORMEM - MICROSTEP 2
  { 0b0001000010011, 0b11100110 },  // ORMEM - MICROSTEP 3

  { 0b0001000100000, 0b01000111 },  // ANDA - MICROSTEP 0
  { 0b0001000100001, 0b11100110 },  // ANDA - MICROSTEP 1
  { 0b0001000100010, 0b01100110 },  // ANDA - MICROSTEP 2

  { 0b0001000110000, 0b01000111 },  // ANDB - MICROSTEP 0
  { 0b0001000110001, 0b11100110 },  // ANDB - MICROSTEP 1
  { 0b0001000110010, 0b01100110 },  // ANDB - MICROSTEP 2

  { 0b0001001000000, 0b01000111 },  // ANDMEM - MICROSTEP 0
  { 0b0001001000001, 0b11100110 },  // ANDMEM - MICROSTEP 1
  { 0b0001001000010, 0b01000111 },  // ANDMEM - MICROSTEP 2
  { 0b0001001000011, 0b11100110 },  // ANDMEM - MICROSTEP 3

  { 0b0001001010000, 0b01000111 },  // NEGAA - MICROSTEP 0
  { 0b0001001010001, 0b11100110 },  // NEGAA - MICROSTEP 1
  { 0b0001001010010, 0b01100110 },  // NEGAA - MICROSTEP 2

  { 0b0001001100000, 0b01000111 },  // NEGAB - MICROSTEP 0
  { 0b0001001100001, 0b11100110 },  // NEGAB - MICROSTEP 1
  { 0b0001001100010, 0b01100110 },  // NEGAB - MICROSTEP 2

  { 0b0001001110000, 0b01000111 },  // NEGAMEM - MICROSTEP 0
  { 0b0001001110001, 0b11100110 },  // NEGAMEM - MICROSTEP 1
  { 0b0001001110010, 0b01000111 },  // NEGAMEM - MICROSTEP 2
  { 0b0001001110011, 0b11100110 },  // NEGAMEM - MICROSTEP 3

  { 0b0001010000000, 0b01000111 },  // NEGBA - MICROSTEP 0
  { 0b0001010000001, 0b11100110 },  // NEGBA - MICROSTEP 1
  { 0b0001010000010, 0b01100110 },  // NEGBA - MICROSTEP 2

  { 0b0001010010000, 0b01000111 },  // NEGBB - MICROSTEP 0
  { 0b0001010010001, 0b11100110 },  // NEGBB - MICROSTEP 1
  { 0b0001010010010, 0b01100110 },  // NEGBB - MICROSTEP 2

  { 0b0001010100000, 0b01000111 },  // NEGBMEM - MICROSTEP 0
  { 0b0001010100001, 0b11100110 },  // NEGBMEM - MICROSTEP 1
  { 0b0001010100010, 0b01000111 },  // NEGBMEM - MICROSTEP 2
  { 0b0001010100011, 0b11100110 },  // NEGBMEM - MICROSTEP 3

  { 0b0001010110000, 0b01000111 },  // INVAA - MICROSTEP 0
  { 0b0001010110001, 0b11100110 },  // INVAA - MICROSTEP 1
  { 0b0001010110010, 0b01100110 },  // INVAA - MICROSTEP 2

  { 0b0001011000000, 0b01000111 },  // INVAB - MICROSTEP 0
  { 0b0001011000001, 0b11100110 },  // INVAB - MICROSTEP 1
  { 0b0001011000010, 0b01100110 },  // INVAB - MICROSTEP 2

  { 0b0001011010000, 0b01000111 },  // INVAMEM - MICROSTEP 0
  { 0b0001011010001, 0b11100110 },  // INVAMEM - MICROSTEP 1
  { 0b0001011010010, 0b01000111 },  // INVAMEM - MICROSTEP 2
  { 0b0001011010011, 0b11100110 },  // INVAMEM - MICROSTEP 3

  { 0b0001011100000, 0b01000111 },  // INVBA - MICROSTEP 0
  { 0b0001011100001, 0b11100110 },  // INVBA - MICROSTEP 1
  { 0b0001011100010, 0b01100110 },  // INVBA - MICROSTEP 2

  { 0b0001011110000, 0b01000111 },  // INVBB - MICROSTEP 0
  { 0b0001011110001, 0b11100110 },  // INVBB - MICROSTEP 1
  { 0b0001011110010, 0b01100110 },  // INVBB - MICROSTEP 2

  { 0b0001100000000, 0b01000111 },  // INVBMEM - MICROSTEP 0
  { 0b0001100000001, 0b11100110 },  // INVBMEM - MICROSTEP 1
  { 0b0001100000010, 0b01000111 },  // INVBMEM - MICROSTEP 2
  { 0b0001100000011, 0b11100110 },  // INVBMEM - MICROSTEP 3

  { 0b0001100010000, 0b01000111 },  // SHRAA - MICROSTEP 0
  { 0b0001100010001, 0b11100110 },  // SHRAA - MICROSTEP 1
  { 0b0001100010010, 0b01100110 },  // SHRAA - MICROSTEP 2

  { 0b0001100100000, 0b01000111 },  // SHRAB - MICROSTEP 0
  { 0b0001100100001, 0b11100110 },  // SHRAB - MICROSTEP 1
  { 0b0001100100010, 0b01100110 },  // SHRAB - MICROSTEP 2

  { 0b0001100110000, 0b01000111 },  // SHRAMEM - MICROSTEP 0
  { 0b0001100110001, 0b11100110 },  // SHRAMEM - MICROSTEP 1
  { 0b0001100110010, 0b01000111 },  // SHRAMEM - MICROSTEP 2
  { 0b0001100110011, 0b11100110 },  // SHRAMEM - MICROSTEP 3

  { 0b0001101000000, 0b01000111 },  // SHRBA - MICROSTEP 0
  { 0b0001101000001, 0b11100110 },  // SHRBA - MICROSTEP 1
  { 0b0001101000010, 0b01100110 },  // SHRBA - MICROSTEP 2

  { 0b0001101010000, 0b01000111 },  // SHRBB - MICROSTEP 0
  { 0b0001101010001, 0b11100110 },  // SHRBB - MICROSTEP 1
  { 0b0001101010010, 0b01100110 },  // SHRBB - MICROSTEP 2

  { 0b0001101100000, 0b01000111 },  // SHRBMEM - MICROSTEP 0
  { 0b0001101100001, 0b11100110 },  // SHRBMEM - MICROSTEP 1
  { 0b0001101100010, 0b01000111 },  // SHRBMEM - MICROSTEP 2
  { 0b0001101100011, 0b11100110 },  // SHRBMEM - MICROSTEP 3

  { 0b0001101110000, 0b01000111 },  // SHLAA - MICROSTEP 0
  { 0b0001101110001, 0b11100110 },  // SHLAA - MICROSTEP 1
  { 0b0001101110010, 0b01100110 },  // SHLAA - MICROSTEP 2

  { 0b0001110000000, 0b01000111 },  // SHLAB - MICROSTEP 0
  { 0b0001110000001, 0b11100110 },  // SHLAB - MICROSTEP 1
  { 0b0001110000010, 0b01100110 },  // SHLAB - MICROSTEP 2

  { 0b0001110010000, 0b01000111 },  // SHLAMEM - MICROSTEP 0
  { 0b0001110010001, 0b11100110 },  // SHLAMEM - MICROSTEP 1
  { 0b0001110010010, 0b01000111 },  // SHLAMEM - MICROSTEP 2
  { 0b0001110010011, 0b11100110 },  // SHLAMEM - MICROSTEP 3

  { 0b0001110100000, 0b01000111 },  // SHLBA - MICROSTEP 0
  { 0b0001110100001, 0b11100110 },  // SHLBA - MICROSTEP 1
  { 0b0001110100010, 0b01100110 },  // SHLBA - MICROSTEP 2

  { 0b0001110110000, 0b01000111 },  // SHLBB - MICROSTEP 0
  { 0b0001110110001, 0b11100110 },  // SHLBB - MICROSTEP 1
  { 0b0001110110010, 0b01100110 },  // SHLBB - MICROSTEP 2

  { 0b0001111000000, 0b01000111 },  // SHLBMEM - MICROSTEP 0
  { 0b0001111000001, 0b11100110 },  // SHLBMEM - MICROSTEP 1
  { 0b0001111000010, 0b01000111 },  // SHLBMEM - MICROSTEP 2
  { 0b0001111000011, 0b11100110 },  // SHLBMEM - MICROSTEP 3

  { 0b0001111010000, 0b01000111 },  // CMPAB - MICROSTEP 0
  { 0b0001111010001, 0b11100110 },  // CMPAB - MICROSTEP 1
  { 0b0001111010010, 0b01100110 },  // CMPAB - MICROSTEP 2

  { 0b0001111100000, 0b01000111 },  // CMPBA - MICROSTEP 0
  { 0b0001111100001, 0b11100110 },  // CMPBA - MICROSTEP 1
  { 0b0001111100010, 0b01100110 },  // CMPBA - MICROSTEP 2

  { 0b0001111110000, 0b01000111 },  // HALT - MICROSTEP 0
  { 0b0001111110001, 0b11100110 },  // HALT - MICROSTEP 1
  { 0b0001111110010, 0b01100110 }   // HALT - MICROSTEP 2
};

#endif //CONTROL_UNIT_EEPROM_B2_H