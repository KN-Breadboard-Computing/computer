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

uint16_t NON_ZERO_MEMORY_SIZE = 5;
uint16_t NON_ZERO_MEMORY[5][2] = {
  { 0b0000000001111, 0b10000000 }, 
  { 0b0000000001001, 0b10010011 }, 
  { 0b0000000001011, 0b10000011 }, 
  { 0b0000000001101, 0b10000111 }, 
  { 0b0000000001010, 0b10001111 }
};


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
    output_word((uint8_t) NON_ZERO_MEMORY[i][1]);

    digitalWrite(REG_CLK, HIGH);
    delay(50);
    digitalWrite(REG_CLK, LOW);

    // save value at given address
    output_address(NON_ZERO_MEMORY[i][0]);

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
