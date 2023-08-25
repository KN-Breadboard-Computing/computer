import sys
import os
import serial
import time


SAVE_WORD_BIT                       = 1
SAVE_ADDR_BIT                       = 2
OUT_WORD_BIT                        = 4
OUT_ADDR_BIT                        = 8
TICK_BIT                            = 16
SET_MID_TICK_DELAY_BIT              = 32
SET_AFTER_TICK_DELAY_BIT            = 64
WRITE_INSTRUCTION_TO_MEMORY_BIT     = 128


out_word_enable = False
out_address_enable = False


def get_val(num_str):
    if 'x' in num_str:
        return int(num_str, base=16)
    
    if 'b' in num_str:
        return int(num_str, base=2)

    return int(num_str, base=10)


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

    #time.sleep(1)
    serial_device.write(action.to_bytes(length=1, byteorder='little'))
    serial_device.write(word.to_bytes(length=1, byteorder='little'))
    serial_device.write(address.to_bytes(length=2, byteorder='little'))

    response = ''
    while response != 'D':
        if serial_device.inWaiting():
            response = serial_device.readline().decode('utf').strip()


def make_ticks(tick_num):
    action = TICK_BIT
    if out_word_enable:
        action |= OUT_WORD_BIT
    if out_address_enable:
        action |= OUT_ADDR_BIT

    empty = 0

    #time.sleep(1)
    serial_device.write(action.to_bytes(length=1, byteorder='little'))
    serial_device.write(tick_num.to_bytes(length=1, byteorder='little'))
    serial_device.write(empty.to_bytes(length=2, byteorder='little'))

    response = ''
    while response != 'D':
        if serial_device.inWaiting():
            response = serial_device.readline().decode('utf').strip()


def set_mid_tick_delay(val):
    action = SET_MID_TICK_DELAY_BIT
    if out_word_enable:
        action |= OUT_WORD_BIT
    if out_address_enable:
        action |= OUT_ADDR_BIT

    empty = 0

    #time.sleep(1)
    serial_device.write(action.to_bytes(length=1, byteorder='little'))
    serial_device.write(empty.to_bytes(length=1, byteorder='little'))
    serial_device.write(val.to_bytes(length=2, byteorder='little'))

    response = ''
    while response != 'D':
        if serial_device.inWaiting():
            response = serial_device.readline().decode('utf').strip()


def set_after_tick_delay(val):
    action = SET_AFTER_TICK_DELAY_BIT
    if out_word_enable:
        action |= OUT_WORD_BIT
    if out_address_enable:
        action |= OUT_ADDR_BIT

    empty = 0

    #time.sleep(1)
    serial_device.write(action.to_bytes(length=1, byteorder='little'))
    serial_device.write(empty.to_bytes(length=1, byteorder='little'))
    serial_device.write(val.to_bytes(length=2, byteorder='little'))

    response = ''
    while response != 'D':
        if serial_device.inWaiting():
            response = serial_device.readline().decode('utf').strip()


def write_instruction_to_memory(address, word):
    action = WRITE_INSTRUCTION_TO_MEMORY_BIT
    action |= OUT_WORD_BIT
    action |= OUT_ADDR_BIT

    serial_device.write(action.to_bytes(length=1, byteorder='little'))
    serial_device.write(word.to_bytes(length=1, byteorder='little'))
    serial_device.write(address.to_bytes(length=2, byteorder='little'))

    response = ''
    while response != 'D':
        if serial_device.inWaiting():
            response = serial_device.readline().decode('utf').strip()


def write_program_to_memory(filename):
    try:
        with open(filename, 'r') as program_file:
            lines = [line for line in [line.strip().split() for line in program_file.readlines() if '#' not in line] if line]
            for line in lines:
                address, word = line

                write_instruction_to_memory(int(address, base=2), int(word, base=2))
                time.sleep(2)

                print(f'{address}: {word}')
    except Exception as e:
        print(e)
    finally:
        send_config(out_word_enable, out_address_enable, False, False)


def initialize():
    set_mid_tick_delay(1)
    set_after_tick_delay(1)

    for _ in range(10000):
        write_instruction_to_memory(1023, 7)


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

        if tokens_count == 1 and (tokens[0] == 'quit' or tokens[0] == 'q'):
            break
        elif tokens_count == 1 and (tokens[0] == 'clear' or tokens[0] == 'c'):
            os.system('clear')      # for Linux
            #os.system('cls')       # for Windows
        elif tokens_count == 1 and (tokens[0] == 'init' or tokens[0] == 'i'):
            initialize()
        elif tokens_count == 1 and (tokens[0] == 'disable' or tokens[0] == 'd'):
            out_word_enable = False
            out_address_enable = False
            send_config(False, False, False, False)
        elif tokens_count == 1 and (tokens[0] == 'disableword' or tokens[0] == 'dw'):
            out_word_enable = False
            send_config(False, out_address_enable, False, False)
        elif tokens_count == 1 and (tokens[0] == 'disableaddress' or tokens[0] == 'da'):
            out_address_enable = False
            send_config(out_word_enable, False, False, False)
        elif tokens_count == 1 and (tokens[0] == 'enable' or tokens[0] == 'e'):
            out_word_enable = True
            out_address_enable = True
            send_config(True, True, False, False)
        elif tokens_count == 1 and (tokens[0] == 'enableword' or tokens[0] == 'ew'):
            out_word_enable = True
            send_config(True, out_address_enable, False, False)
        elif tokens_count == 1 and (tokens[0] == 'enableaddress' or tokens[0] == 'ea'):
            out_address_enable = True
            send_config(out_word_enable, True, False, False)
        elif tokens_count == 2 and (tokens[0] == 'writeword' or tokens[0] == 'ww'):
            word_val = get_val(tokens[1])
            send_config(out_word_enable, out_address_enable, True, False, word=word_val)
        elif tokens_count == 2 and (tokens[0] == 'writeaddress' or tokens[0] == 'wa'):
            address_val = get_val(tokens[1])
            send_config(out_word_enable, out_address_enable, False, True, address=address_val)
        elif tokens_count == 3 and (tokens[0] == 'writewordaddress' or tokens[0] == 'wwa'):
            word_val = get_val(tokens[1])
            address_val = get_val(tokens[2])
            send_config(out_word_enable, out_address_enable, True, True, word=word_val, address=address_val)
        elif tokens_count == 2 and (tokens[0] == 'setmiddelay' or tokens[0] == 'smd'):
            set_mid_tick_delay(int(tokens[1]))
        elif tokens_count == 2 and (tokens[0] == 'setafterdelay' or tokens[0] == 'sad'):
            set_after_tick_delay(int(tokens[1]))
        elif tokens_count == 1 and (tokens[0] == 'tick' or tokens[0] == 't'):
            make_ticks(1)
        elif tokens_count == 2 and (tokens[0] == 'tick' or tokens[0] == 't'):
            make_ticks(int(tokens[1]))
        elif tokens_count == 2 and (tokens[0] == 'writeprogram' or tokens[0] == 'wp'):
            write_program_to_memory(tokens[1])

    serial_device.flushInput()
    serial_device.flushOutput()
    serial_device.close()