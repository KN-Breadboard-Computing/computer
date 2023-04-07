#include "defines.h"

#ifndef ALU_EEPROM_H
#define ALU_EEPROM_H

/*
| A0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 |

-> A0 = MULTIPLEXER OUTPUT SELECTOR 0
-> A1 = MULTIPLEXER OUTPUT SELECTOR 1
-> A2 = MULTIPLEXER OUTPUT SELECTOR 2
-> A3 = INVERSE A INPUT
-> A4 = INVERSE B INPUT
-> A5 = MAKE A NON-ZERO INPUT
-> A6 = MAKE B NON-ZERO INPUT
-> A7 = INVERSE (A OR B) OUTPUT
*/

uint16_t NON_ZERO_MEMORY_SIZE = 16;
MemoryCell NON_ZERO_MEMORY[16] = {
  { 0b0000000000000, 0b10000010 },  // send 0 on the data bus
  { 0b0000000000001, 0b10000100 },  // send A on the data bus
  { 0b0000000000010, 0b01000010 },  // send B on the data bus
  { 0b0000000000011, 0b00000110 },  // send A+B on the data bus
  { 0b0000000000100, 0b00010100 },  // send -A on the data bus
  { 0b0000000000101, 0b00001010 },  // send -B on the data bus
  { 0b0000000000110, 0b00001110 },  // send A-B on the data bus
  { 0b0000000000111, 0b00010110 },  // send B-A on the data bus
  { 0b0000000001000, 0b10010100 },  // send NOT A on the data bus
  { 0b0000000001001, 0b01001010 },  // send NOT B on the data bus
  { 0b0000000001010, 0b11000110 },  // send A OR B on the data bus
  { 0b0000000001011, 0b11011111 },  // send A AND B on the data bus
  { 0b0000000001100, 0b00100110 },  // send A << 1 on the data bus
  { 0b0000000001101, 0b10100110 },  // send B << 1 on the data bus
  { 0b0000000001110, 0b01100110 },  // send A >> 1 on the data bus
  { 0b0000000001111, 0b11100110 },  // send B >> 1 on the data bus
};

#endif //ALU_EEPROM_H