#include "defines.h"

//#include "regs_move.h"
#include "mem_move.h"

int buttonState = 0;


void tick() {
  digitalWrite(CLOCK_PIN, HIGH);
  delay(20);
  digitalWrite(CLOCK_PIN, LOW);
}


void latchAddress(uint16_t address) {
  for(int i = 0; i < ADDR_SIZE_LOW; i++) {
    if(address & (1 << i)) {
      digitalWrite(DATA_BITS[i], HIGH);
    }
    else {
      digitalWrite(DATA_BITS[i], LOW);
    }
  }

  digitalWrite(LATCH_ADDR_LOW, HIGH);
  delay(50);
  digitalWrite(LATCH_ADDR_LOW, LOW);

  for(int i = ADDR_SIZE_LOW; i < ADDR_SIZE_HIGH + ADDR_SIZE_LOW; i++) {
    if(address & (1 << i)) {
      digitalWrite(DATA_BITS[i - ADDR_SIZE_LOW], HIGH);
    }
    else {
      digitalWrite(DATA_BITS[i - ADDR_SIZE_LOW], LOW);
    }
  }

  digitalWrite(LATCH_ADDR_HIGH, HIGH);
  delay(50);
  digitalWrite(LATCH_ADDR_HIGH, LOW);
}


void latchWord(uint8_t word) {
  for(int i = 0; i < DATA_SIZE; i++) {
    if(word & (1 << i)) {
      digitalWrite(DATA_BITS[i], HIGH);
    }
    else {
      digitalWrite(DATA_BITS[i], LOW);
    }
  }

  digitalWrite(LATCH_WORD, HIGH);
  delay(50);
  digitalWrite(LATCH_WORD, LOW);
}


void writeProgram() {
  for(uint16_t i = 0; i < PROGRAM_SIZE; i++) {
    tick();
    tick();
    tick();
    tick();
    latchAddress(PROGRAM[i].address);
    latchWord(PROGRAM[i].word);
    tick();
    tick();
    tick();
    tick();
  }
}


void setup() {
  for(uint8_t i = 0; i < DATA_SIZE; i++) {
    pinMode(DATA_BITS[i], OUTPUT);
  }

  pinMode(LATCH_WORD, OUTPUT);
  pinMode(LATCH_ADDR_HIGH, OUTPUT);
  pinMode(LATCH_ADDR_LOW, OUTPUT);
  pinMode(OUT_REGISTERS, OUTPUT);

  pinMode(CLOCK_PIN, OUTPUT);

  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LATCH_WORD, LOW);
  digitalWrite(LATCH_ADDR_HIGH, LOW);
  digitalWrite(LATCH_ADDR_LOW, LOW);

  digitalWrite(CLOCK_PIN, LOW);
  digitalWrite(LED_BUILTIN, LOW);
}


void loop() { 
  buttonState = digitalRead(BUTTON_PIN);
  if(buttonState == HIGH) {
    delay(1000);

    digitalWrite(LED_BUILTIN, HIGH);
    digitalWrite(OUT_REGISTERS, LOW);

    writeProgram();

    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(OUT_REGISTERS, HIGH);

    
    while(1) {
      buttonState = digitalRead(BUTTON_PIN);
      if(buttonState == HIGH) {
        tick();
        delay(100);
      }
    }
    
  }
}
