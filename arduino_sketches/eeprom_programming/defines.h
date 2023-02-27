#ifndef DEFINES_H
#define DEFINES_H

#define WORD_BIT_0      2
#define WORD_BIT_1      3
#define WORD_BIT_2      4
#define WORD_BIT_3      5
#define WORD_BIT_4      6
#define WORD_BIT_5      7
#define WORD_BIT_6      8
#define WORD_BIT_7      9

#define ADDRESS_BIT_0   2
#define ADDRESS_BIT_1   3
#define ADDRESS_BIT_2   4
#define ADDRESS_BIT_3   5
#define ADDRESS_BIT_4   6
#define ADDRESS_BIT_5   7
#define ADDRESS_BIT_6   8
#define ADDRESS_BIT_7   9
#define ADDRESS_BIT_8   10
#define ADDRESS_BIT_9   11
#define ADDRESS_BIT_10  12
#define ADDRESS_BIT_11  18
#define ADDRESS_BIT_12  19

#define REG_CLK         14
#define EEPROM_WE       15
#define EEPROM_CE       16


uint8_t WORD_BITS[8] = { WORD_BIT_0, WORD_BIT_1, WORD_BIT_2, WORD_BIT_3, WORD_BIT_4, WORD_BIT_5, WORD_BIT_6, WORD_BIT_7 };
uint8_t WORD_SIZE = 8;

uint8_t ADDRESS_BITS[13] = { ADDRESS_BIT_0, ADDRESS_BIT_1, ADDRESS_BIT_2, ADDRESS_BIT_3, ADDRESS_BIT_4, ADDRESS_BIT_5, ADDRESS_BIT_6, ADDRESS_BIT_7, ADDRESS_BIT_8, ADDRESS_BIT_9, ADDRESS_BIT_10, ADDRESS_BIT_11, ADDRESS_BIT_12 };
uint8_t ADDRESS_SIZE = 13;


typedef struct {
  uint16_t address;
  uint8_t value;
} MemoryCell;

#endif //DEFINES_H