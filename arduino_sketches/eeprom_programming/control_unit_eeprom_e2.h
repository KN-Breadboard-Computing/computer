#include "defines.h"

#ifndef CONTROL_UNIT_EEPROM_E2_H
#define CONTROL_UNIT_EEPROM_E2_H

/*
| E0 |E1 | E2 | E3 | E4 | E5 | E6 | E7 |

-> E0 = MC++
-> E1 = ~OUT FLAGS
-> E2 = NOT DEFINED
-> E3 = NOT DEFINED
-> E4 = NOT DEFINED
-> E5 = NOT DEFINED
-> E6 = NOT DEFINED
-> E7 = NOT DEFINED
*/

uint16_t NON_ZERO_MEMORY_SIZE = 4;
MemoryCell NON_ZERO_MEMORY[4] = {
  { 0b0000000000000, 0b11000000 },  // EMPTY - MICROSTEP 0
  { 0b0000000000001, 0b11000000 },  // EMPTY - MICROSTEP 1
  { 0b0000000000010, 0b11000000 },  // EMPTY - MICROSTEP 2
  { 0b0000000000011, 0b11000000 }   // EMPTY - MICROSTEP 3
};

#endif //CONTROL_UNIT_EEPROM_E2_H