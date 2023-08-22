import time

# INPUT : |A12|A11|A10|A9|A8|A7|A6|A5|A4|A3|A2|A1|A0|
# OUTPUT: |IO7|IO6|IO5|IO4|IO3|IO2|IO1|IO0|

INPUT_BITS_NUMBER = 13
OUTPUT_BITS_NUMBER = 8

PRINT = True


class Eeprom:
    def __init__(self):
        self._values = {}

    def __str__(self):
        result = ''
        for desc, vals in self._values.items():
            result += f'{desc}: 0b{vals[0]:0{INPUT_BITS_NUMBER}b} -> 0b{vals[1]:0{OUTPUT_BITS_NUMBER}b}\n'

        return result

    def write(self, description, address, word):
        self._values[description] = (address, word)

    def send_to_serial(self, serial_device):
        if PRINT:
            print('Initializing...')
        time.sleep(5)

        data = [0 for _ in range(2**INPUT_BITS_NUMBER)]
        for desc, val in self._values.items():
            data[val[0]] = val[1]

        if PRINT:
            print('Writing to EEPROM...')

        for address, word in enumerate(data):
            serial_device.write(address.to_bytes(length=2, byteorder='little'))
            serial_device.write(word.to_bytes(length=1, byteorder='little'))
            if PRINT:
                print(f'0b{address:0{INPUT_BITS_NUMBER}b} -> 0b{word:0{OUTPUT_BITS_NUMBER}b}')

            response = ''
            while response != 'D':
                if serial_device.inWaiting():
                    response = serial_device.readline().decode('utf').strip()
        
        if PRINT:
            print('Writing to EEPROM done!')
