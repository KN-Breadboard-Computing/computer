#include "../defines.h"

#ifndef EEPROM_A_MAN_ACS_2
#define EEPROM_A_MAN_ACS_2

/*
| A0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 |

-> A0 = LD A
-> A1 = LD B
-> A2 = LD F
-> A3 = ~ALU OUT
-> A4 = ALU OPC 0
-> A5 = ALU OPC 1
-> A6 = ALU OPC 2
-> A7 = ALU OPC 3
*/

uint16_t NON_ZERO_MEMORY_SIZE = 512;
MemoryCell NON_ZERO_MEMORY[512] = {
  { 0b1010000000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010000000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010000000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010000000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010000000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010000000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010000000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010000000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010000010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010000010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010000010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010000010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010000010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010000010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010000010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010000010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010000100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010000100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010000100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010000100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010000100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010000100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010000100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010000100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010000110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010000110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010000110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010000110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010000110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010000110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010000110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010000110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010001000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010001000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010001000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010001000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010001000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010001000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010001000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010001000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010001010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010001010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010001010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010001010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010001010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010001010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010001010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010001010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010001100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010001100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010001100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010001100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010001100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010001100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010001100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010001100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010001110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010001110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010001110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010001110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010001110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010001110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010001110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010001110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010010000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010010000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010010000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010010000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010010000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010010000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010010000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010010000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010010010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010010010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010010010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010010010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010010010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010010010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010010010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010010010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010010100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010010100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010010100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010010100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010010100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010010100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010010100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010010100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010010110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010010110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010010110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010010110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010010110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010010110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010010110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010010110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010011000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010011000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010011000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010011000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010011000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010011000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010011000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010011000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010011010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010011010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010011010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010011010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010011010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010011010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010011010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010011010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010011100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010011100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010011100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010011100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010011100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010011100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010011100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010011100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010011110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010011110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010011110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010011110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010011110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010011110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010011110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010011110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010100000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010100000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010100000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010100000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010100000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010100000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010100000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010100000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010100010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010100010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010100010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010100010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010100010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010100010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010100010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010100010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010100100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010100100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010100100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010100100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010100100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010100100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010100100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010100100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010100110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010100110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010100110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010100110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010100110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010100110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010100110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010100110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010101000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010101000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010101000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010101000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010101000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010101000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010101000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010101000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010101010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010101010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010101010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010101010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010101010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010101010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010101010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010101010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010101100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010101100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010101100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010101100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010101100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010101100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010101100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010101100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010101110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010101110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010101110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010101110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010101110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010101110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010101110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010101110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010110000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010110000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010110000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010110000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010110000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010110000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010110000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010110000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010110010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010110010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010110010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010110010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010110010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010110010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010110010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010110010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010110100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010110100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010110100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010110100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010110100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010110100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010110100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010110100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010110110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010110110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010110110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010110110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010110110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010110110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010110110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010110110111, 0b00010000 }, // MICROSTEP 7

  { 0b1010111000000, 0b00010000 }, // MICROSTEP 0
  { 0b1010111000001, 0b00010000 }, // MICROSTEP 1
  { 0b1010111000010, 0b00010000 }, // MICROSTEP 2
  { 0b1010111000011, 0b00010000 }, // MICROSTEP 3
  { 0b1010111000100, 0b00010000 }, // MICROSTEP 4
  { 0b1010111000101, 0b00010000 }, // MICROSTEP 5
  { 0b1010111000110, 0b00010000 }, // MICROSTEP 6
  { 0b1010111000111, 0b00010000 }, // MICROSTEP 7

  { 0b1010111010000, 0b00010000 }, // MICROSTEP 0
  { 0b1010111010001, 0b00010000 }, // MICROSTEP 1
  { 0b1010111010010, 0b00010000 }, // MICROSTEP 2
  { 0b1010111010011, 0b00010000 }, // MICROSTEP 3
  { 0b1010111010100, 0b00010000 }, // MICROSTEP 4
  { 0b1010111010101, 0b00010000 }, // MICROSTEP 5
  { 0b1010111010110, 0b00010000 }, // MICROSTEP 6
  { 0b1010111010111, 0b00010000 }, // MICROSTEP 7

  { 0b1010111100000, 0b00010000 }, // MICROSTEP 0
  { 0b1010111100001, 0b00010000 }, // MICROSTEP 1
  { 0b1010111100010, 0b00010000 }, // MICROSTEP 2
  { 0b1010111100011, 0b00010000 }, // MICROSTEP 3
  { 0b1010111100100, 0b00010000 }, // MICROSTEP 4
  { 0b1010111100101, 0b00010000 }, // MICROSTEP 5
  { 0b1010111100110, 0b00010000 }, // MICROSTEP 6
  { 0b1010111100111, 0b00010000 }, // MICROSTEP 7

  { 0b1010111110000, 0b00010000 }, // MICROSTEP 0
  { 0b1010111110001, 0b00010000 }, // MICROSTEP 1
  { 0b1010111110010, 0b00010000 }, // MICROSTEP 2
  { 0b1010111110011, 0b00010000 }, // MICROSTEP 3
  { 0b1010111110100, 0b00010000 }, // MICROSTEP 4
  { 0b1010111110101, 0b00010000 }, // MICROSTEP 5
  { 0b1010111110110, 0b00010000 }, // MICROSTEP 6
  { 0b1010111110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011000000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011000000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011000000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011000000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011000000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011000000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011000000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011000000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011000010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011000010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011000010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011000010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011000010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011000010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011000010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011000010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011000100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011000100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011000100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011000100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011000100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011000100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011000100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011000100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011000110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011000110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011000110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011000110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011000110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011000110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011000110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011000110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011001000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011001000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011001000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011001000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011001000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011001000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011001000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011001000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011001010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011001010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011001010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011001010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011001010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011001010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011001010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011001010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011001100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011001100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011001100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011001100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011001100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011001100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011001100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011001100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011001110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011001110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011001110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011001110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011001110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011001110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011001110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011001110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011010000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011010000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011010000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011010000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011010000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011010000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011010000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011010000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011010010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011010010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011010010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011010010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011010010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011010010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011010010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011010010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011010100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011010100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011010100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011010100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011010100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011010100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011010100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011010100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011010110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011010110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011010110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011010110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011010110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011010110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011010110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011010110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011011000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011011000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011011000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011011000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011011000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011011000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011011000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011011000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011011010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011011010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011011010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011011010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011011010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011011010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011011010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011011010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011011100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011011100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011011100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011011100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011011100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011011100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011011100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011011100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011011110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011011110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011011110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011011110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011011110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011011110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011011110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011011110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011100000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011100000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011100000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011100000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011100000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011100000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011100000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011100000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011100010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011100010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011100010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011100010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011100010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011100010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011100010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011100010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011100100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011100100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011100100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011100100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011100100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011100100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011100100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011100100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011100110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011100110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011100110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011100110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011100110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011100110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011100110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011100110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011101000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011101000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011101000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011101000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011101000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011101000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011101000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011101000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011101010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011101010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011101010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011101010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011101010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011101010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011101010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011101010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011101100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011101100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011101100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011101100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011101100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011101100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011101100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011101100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011101110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011101110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011101110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011101110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011101110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011101110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011101110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011101110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011110000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011110000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011110000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011110000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011110000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011110000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011110000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011110000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011110010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011110010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011110010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011110010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011110010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011110010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011110010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011110010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011110100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011110100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011110100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011110100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011110100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011110100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011110100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011110100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011110110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011110110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011110110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011110110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011110110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011110110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011110110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011110110111, 0b00010000 }, // MICROSTEP 7

  { 0b1011111000000, 0b00010000 }, // MICROSTEP 0
  { 0b1011111000001, 0b00010000 }, // MICROSTEP 1
  { 0b1011111000010, 0b00010000 }, // MICROSTEP 2
  { 0b1011111000011, 0b00010000 }, // MICROSTEP 3
  { 0b1011111000100, 0b00010000 }, // MICROSTEP 4
  { 0b1011111000101, 0b00010000 }, // MICROSTEP 5
  { 0b1011111000110, 0b00010000 }, // MICROSTEP 6
  { 0b1011111000111, 0b00010000 }, // MICROSTEP 7

  { 0b1011111010000, 0b00010000 }, // MICROSTEP 0
  { 0b1011111010001, 0b00010000 }, // MICROSTEP 1
  { 0b1011111010010, 0b00010000 }, // MICROSTEP 2
  { 0b1011111010011, 0b00010000 }, // MICROSTEP 3
  { 0b1011111010100, 0b00010000 }, // MICROSTEP 4
  { 0b1011111010101, 0b00010000 }, // MICROSTEP 5
  { 0b1011111010110, 0b00010000 }, // MICROSTEP 6
  { 0b1011111010111, 0b00010000 }, // MICROSTEP 7

  { 0b1011111100000, 0b00010000 }, // MICROSTEP 0
  { 0b1011111100001, 0b00010000 }, // MICROSTEP 1
  { 0b1011111100010, 0b00010000 }, // MICROSTEP 2
  { 0b1011111100011, 0b00010000 }, // MICROSTEP 3
  { 0b1011111100100, 0b00010000 }, // MICROSTEP 4
  { 0b1011111100101, 0b00010000 }, // MICROSTEP 5
  { 0b1011111100110, 0b00010000 }, // MICROSTEP 6
  { 0b1011111100111, 0b00010000 }, // MICROSTEP 7

  { 0b1011111110000, 0b00010000 }, // MICROSTEP 0
  { 0b1011111110001, 0b00010000 }, // MICROSTEP 1
  { 0b1011111110010, 0b00010000 }, // MICROSTEP 2
  { 0b1011111110011, 0b00010000 }, // MICROSTEP 3
  { 0b1011111110100, 0b00010000 }, // MICROSTEP 4
  { 0b1011111110101, 0b00010000 }, // MICROSTEP 5
  { 0b1011111110110, 0b00010000 }, // MICROSTEP 6
  { 0b1011111110111, 0b00010000 }  // MICROSTEP 7
};

#endif // EEPROM_A_MAN_ACS_2