#include "defines.h"

int buttonState;
MessageBuffer messageBuffer;


void tick() {
  digitalWrite(CLOCK_PIN, HIGH);
  delay(5);
  digitalWrite(CLOCK_PIN, LOW);
}


void latchAddress(uint16_t address) {
  for(int i = 0; i < ADDR_LOW_SIZE; i++) {
    if(address & (1 << i)) {
      digitalWrite(DATA_BITS[i], HIGH);
    }
    else {
      digitalWrite(DATA_BITS[i], LOW);
    }
  }

  digitalWrite(LATCH_ADDR_LOW, HIGH);
  delay(5);
  digitalWrite(LATCH_ADDR_LOW, LOW);

  for(int i = ADDR_LOW_SIZE; i < ADDR_HIGH_SIZE + ADDR_LOW_SIZE; i++) {
    if(address & (1 << i)) {
      digitalWrite(DATA_BITS[i - ADDR_LOW_SIZE], HIGH);
    }
    else {
      digitalWrite(DATA_BITS[i - ADDR_LOW_SIZE], LOW);
    }
  }

  digitalWrite(LATCH_ADDR_HIGH, HIGH);
  delay(5);
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
  delay(5);
  digitalWrite(LATCH_WORD, LOW);
}


void setup() {
  Serial.begin(115200);
  while (!Serial) { }
  
  for(uint8_t i = 0; i < DATA_SIZE; i++) {
    pinMode(DATA_BITS[i], OUTPUT);
  }

  pinMode(LATCH_WORD, OUTPUT);
  pinMode(LATCH_ADDR_HIGH, OUTPUT);
  pinMode(LATCH_ADDR_LOW, OUTPUT);
  pinMode(OUT_WORD, OUTPUT);
  pinMode(OUT_ADDR, OUTPUT);

  pinMode(CLOCK_PIN, OUTPUT);

  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LATCH_WORD, LOW);
  digitalWrite(LATCH_ADDR_HIGH, LOW);
  digitalWrite(LATCH_ADDR_LOW, LOW);

  digitalWrite(CLOCK_PIN, LOW);
  digitalWrite(LED_BUILTIN, LOW);

  digitalWrite(OUT_WORD, HIGH);
  digitalWrite(OUT_ADDR, HIGH);
}


void loop() { 
  buttonState = digitalRead(BUTTON_PIN);
  if(buttonState == HIGH) {  }

  if(Serial.available() >= 4) {
    Serial.readBytes(messageBuffer.bytes, 4);

    if(messageBuffer.message.action & OUT_WORD_BIT) {
      digitalWrite(OUT_WORD, LOW);
    }
    else {
      digitalWrite(OUT_WORD, HIGH);
    }

    if(messageBuffer.message.action & OUT_ADDR_BIT) {
      digitalWrite(OUT_ADDR, LOW);
    }
    else {
      digitalWrite(OUT_ADDR, HIGH);
    }

    if(messageBuffer.message.action & SAVE_WORD_BIT) {
      latchWord(messageBuffer.message.word);
    }

    if(messageBuffer.message.action & SAVE_ADDR_BIT) {
      latchAddress(messageBuffer.message.address); 
    }

    Serial.println(CALLBACK_CODE);
  }
}
