#include "defines.h"

MessageBuffer messageBuffer;


void output_word(uint8_t word) {
  for(uint8_t i = 0; i < WORD_SIZE; i++) {
    if(word & (1 << i)) {
      digitalWrite(WORD_BITS[i], HIGH);
    }
    else {
      digitalWrite(WORD_BITS[i], LOW);
    }
  }
}


void output_address(uint16_t address) {
  for(uint8_t i = 0; i < ADDRESS_SIZE; i++) {
    if(address & (1 << i)) {
      digitalWrite(ADDRESS_BITS[i], HIGH);
    }
    else {
      digitalWrite(ADDRESS_BITS[i], LOW);
    }
  }
} 


void setup() {
  Serial.begin(115200);
  while (!Serial) { }

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  pinMode(REG_CLK, OUTPUT);
  digitalWrite(REG_CLK, LOW);

  pinMode(EEPROM_WE, OUTPUT);
  digitalWrite(EEPROM_WE, HIGH);

  pinMode(EEPROM_CE, OUTPUT);
  digitalWrite(EEPROM_CE, LOW);

  for(uint8_t i = 0; i < WORD_SIZE; i++) {
    pinMode(WORD_BITS[i], OUTPUT);
  }

  for(uint8_t i = 0; i < ADDRESS_SIZE; i++) {
    pinMode(ADDRESS_BITS[i], OUTPUT);
  }
}


void loop() { 
  if(Serial.available() >= 3) {
    Serial.readBytes(messageBuffer.bytes, 3);

    // save given value to register 
    output_word(messageBuffer.message.word);

    digitalWrite(REG_CLK, HIGH);
    delay(5);
    digitalWrite(REG_CLK, LOW);

    // save value at given address
    output_address(messageBuffer.message.address);

    digitalWrite(EEPROM_WE, LOW);
    delay(1);

    digitalWrite(EEPROM_CE, HIGH);
    delay(1);
    digitalWrite(EEPROM_CE, LOW);
    delay(1);
    digitalWrite(EEPROM_CE, HIGH);

    delay(1);
    digitalWrite(EEPROM_WE, HIGH);

    Serial.println('D');
  }
}
