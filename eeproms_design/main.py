import sys
import os
import serial

from alu_logic_eeprom import AluLogicEeprom


if __name__ == '__main__':
    device_name = '/dev/ttyUSB0'
    baud_rate = 115200

    if len(sys.argv) == 2:
        os.system(f'sudo chmod a+rw {device_name}')
        os.system(f'fuser -k {device_name}')
        serial_device = serial.Serial(device_name, baud_rate, timeout=1)
        
        eeprom_id = sys.argv[1].lower()

        if eeprom_id == 'alu':
            eeprom = AluLogicEeprom()
            eeprom.send_to_serial(serial_device)
        else:
            print("Enter EEPROM name:\n[alu / decoderA / decoderB / decoderC / decoderD / decoderE / decoder F]")

        serial_device.flushInput()
        serial_device.flushOutput()
        serial_device.close()
