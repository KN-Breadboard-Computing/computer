#ifndef DEFINES_H
#define DEFINES_H

#define DATA_BIT_0        2     // D2
#define DATA_BIT_1        3     // D3
#define DATA_BIT_2        4     // D4
#define DATA_BIT_3        5     // D5
#define DATA_BIT_4        6     // D6
#define DATA_BIT_5        7     // D7
#define DATA_BIT_6        8     // D8
#define DATA_BIT_7        9     // D9 

#define LATCH_WORD        15    // A1
#define LATCH_ADDR_LOW    16    // A2
#define LATCH_ADDR_HIGH   17    // A3
#define OUT_WORD          18    // A4
#define OUT_ADDR          19    // A5

#define CLOCK_PIN         14    // A0

#define BUTTON_PIN        12    // D12


// action bits description
#define SAVE_WORD_BIT             1
#define SAVE_ADDR_BIT             2
#define OUT_WORD_BIT              4
#define OUT_ADDR_BIT              8
#define CALLBACK_CODE             'D' 


uint8_t DATA_BITS[8] = { DATA_BIT_7, DATA_BIT_6, DATA_BIT_5, DATA_BIT_4, DATA_BIT_3, DATA_BIT_2, DATA_BIT_1, DATA_BIT_0 };


uint8_t DATA_SIZE = 8;
uint8_t ADDR_HIGH_SIZE = 8;
uint8_t ADDR_LOW_SIZE = 8;


typedef struct {
  uint8_t action;
  uint8_t word;
  uint16_t address;
} Message;

typedef union {
  Message message;
  uint8_t bytes[4];
} MessageBuffer;

#endif //DEFINES_H
