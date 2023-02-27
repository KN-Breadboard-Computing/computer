#include "defines.h"

//#include "alu_eeprom.h"
//#include "control_unit_eeprom_a1.h"
//#include "control_unit_eeprom_a2.h"
//#include "control_unit_eeprom_b1.h"
#include "control_unit_eeprom_b2.h"
//#include "control_unit_eeprom_c1.h"
//#include "control_unit_eeprom_c2.h"
//#include "control_unit_eeprom_d1.h"
//#include "control_unit_eeprom_d2.h"
//#include "control_unit_eeprom_e1.h"
//#include "control_unit_eeprom_e2.h"

void output_word(uint8_t word) {
  for(int i = 0; i < WORD_SIZE; i++) {
    if(word & (1 << i)) {
      digitalWrite(WORD_BITS[i], HIGH);
    }
    else {
      digitalWrite(WORD_BITS[i], LOW);
    }
  }
}


void output_address(uint16_t address) {
  for(int i = 0; i < ADDRESS_SIZE; i++) {
    if(address & (1 << i)) {
      digitalWrite(ADDRESS_BITS[i], HIGH);
    }
    else {
      digitalWrite(ADDRESS_BITS[i], LOW);
    }
  }
}


void write_memory_to_eeprom() {
  for(uint16_t i = 0; i < NON_ZERO_MEMORY_SIZE; i++) {
    // save given value to register 
    output_word(NON_ZERO_MEMORY[i].value);

    digitalWrite(REG_CLK, HIGH);
    delay(50);
    digitalWrite(REG_CLK, LOW);

    // save value at given address
    output_address(NON_ZERO_MEMORY[i].address);

    digitalWrite(EEPROM_WE, LOW);
    delay(10);

    digitalWrite(EEPROM_CE, HIGH);
    delay(10);
    digitalWrite(EEPROM_CE, LOW);
    delay(10);
    digitalWrite(EEPROM_CE, HIGH);

    delay(10);
    digitalWrite(EEPROM_WE, HIGH);
  }
}

 
void setup() {
  Serial.begin(115200);
  while (!Serial) { }

  Serial.println("Initializing outputs...");

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

  Serial.println("Writing to EEPROM...");
  write_memory_to_eeprom();

  Serial.println("Writing to EEPROM done!\n");
}

void loop() { }
