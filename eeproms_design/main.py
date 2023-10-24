import sys
import os
import serial

from alu_logic_eeprom import AluLogicEeprom
from control_unit_eeproms import ControlUnitEeproms


device_name = '/dev/ttyUSB1'
baud_rate = 115200

alu_logic_eeprom = AluLogicEeprom()
control_logic_eeproms = ControlUnitEeproms()

if len(sys.argv) == 2:
    os.system(f'sudo chmod a+rw {device_name}')
    os.system(f'fuser -k {device_name}')
    serial_device = serial.Serial(device_name, baud_rate, timeout=1)
    
    eeprom_id = sys.argv[1]

    if eeprom_id == 'alu':
        alu_logic_eeprom.send_to_serial(serial_device)
    elif eeprom_id == 'decoderA':
        control_logic_eeproms.get_eeeprom('A').send_to_serial(serial_device)
    elif eeprom_id == 'decoderB':
        control_logic_eeproms.get_eeeprom('B').send_to_serial(serial_device)
    elif eeprom_id == 'decoderC':
        control_logic_eeproms.get_eeeprom('C').send_to_serial(serial_device)
    elif eeprom_id == 'decoderD':
        control_logic_eeproms.get_eeeprom('D').send_to_serial(serial_device)
    elif eeprom_id == 'decoderE':
        control_logic_eeproms.get_eeeprom('E').send_to_serial(serial_device)
    elif eeprom_id == 'decoderF':
        control_logic_eeproms.get_eeeprom('F').send_to_serial(serial_device)
    else:
        print("Enter EEPROM name:\n[alu / decoderA / decoderB / decoderC / decoderD / decoderE / decoderF]")

    serial_device.flushInput()
    serial_device.flushOutput()
    serial_device.close()
