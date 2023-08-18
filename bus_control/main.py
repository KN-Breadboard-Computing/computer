import sys
import os
import serial
import time


SAVE_WORD_BIT = 1
SAVE_ADDR_BIT = 2
OUT_WORD_BIT  = 4
OUT_ADDR_BIT  = 8

out_word_enable = False
out_address_enable = False

def send_config(out_word, out_address, save_word, save_address, word = 0, address = 0):
    action = 0
    if out_word:
        action |= OUT_WORD_BIT
    if out_address:
        action |= OUT_ADDR_BIT
    if save_word:
        action |= SAVE_WORD_BIT
    if save_address:
        action |= SAVE_ADDR_BIT

    time.sleep(1)
    serial_device.write(action.to_bytes(length=1, byteorder='little'))
    serial_device.write(word.to_bytes(length=1, byteorder='little'))
    serial_device.write(address.to_bytes(length=2, byteorder='little'))

    response = ''
    while response != 'D':
        if serial_device.inWaiting():
            response = serial_device.readline().decode('utf').strip()


if __name__ == '__main__':
    device_name = '/dev/ttyUSB0'
    baud_rate = 115200

    if len(sys.argv) == 1:
        os.system(f'sudo chmod a+rw {device_name}')
        os.system(f'fuser -k {device_name}')
        serial_device = serial.Serial(device_name, baud_rate, timeout=1)
        
        while True:
            user_input = input("Enter a command ('quit' to exit): ")
            tokens = user_input.lower().strip().split()
            tokens_count = len(tokens)

            if tokens_count == 1 and tokens[0] == 'quit':
                break
            elif tokens_count == 1 and tokens[0] == 'disable':
                out_word_enable = False
                out_address_enable = False
                send_config(False, False, False, False)
            elif tokens_count == 1 and tokens[0] == 'disableword':
                out_word_enable = False
                send_config(False, out_address_enable, False, False)
            elif tokens_count == 1 and tokens[0] == 'disableaddress':
                out_address_enable = False
                send_config(out_word_enable, False, False, False)
            elif tokens_count == 1 and tokens[0] == 'enable':
                out_word_enable = True
                out_address_enable = True
                send_config(True, True, False, False)
            elif tokens_count == 1 and tokens[0] == 'enableword':
                out_word_enable = True
                send_config(True, out_address_enable, False, False)
            elif tokens_count == 1 and tokens[0] == 'enableaddress':
                out_address_enable = True
                send_config(out_word_enable, True, False, False)
            elif tokens_count == 2 and tokens[0] == 'writeword':
                send_config(out_word_enable, out_address_enable, True, False, word=0b11001100)
            elif tokens_count == 2 and tokens[0] == 'writeaddress':
                send_config(out_word_enable, out_address_enable, False, True, address=0b1111000011110000)

        serial_device.flushInput()
        serial_device.flushOutput()
        serial_device.close()