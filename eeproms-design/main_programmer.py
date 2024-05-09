import os
import serial
from argparse import ArgumentParser
from pathlib import Path

from eeproms.config import Config
from eeproms.identity_eeprom import IdentityEeprom
from eeproms.alu_eeprom import AluLogicEeprom
from eeproms.control_unit_eeproms import ControlUnitEeproms

parser = ArgumentParser(description='Program the EEPROMs')
parser.add_argument('--config-dir', default=Path(__file__).parent.parent / 'config',
                    help='Path to the directory containing the config JSON files')
parser.add_argument('--device-name', default='/dev/ttyUSB0', help='Device name of the serial port')
parser.add_argument('--baud-rate', default=115200, help='Baud rate of the serial port')
parser.add_argument('--eeprom-label', default='identity', help='EEPROM label to program.')

args = parser.parse_args()

print(f'Config path set to {args.config_dir}')
print(f'Device name set to {args.device_name}')
print(f'Baud rate set to {args.baud_rate}')
print(f'EEPROM label set to {args.eeprom_label}')

config = Config(Path(args.config_dir), instructions_filename='instructions.json', microcodes_filename='microcodes.json',
                signals_filename='signals.json', alu_logic_filename='alu.json')
identity_eeprom = IdentityEeprom()
alu_logic_eeprom = AluLogicEeprom(config)
control_logic_eeproms = ControlUnitEeproms(config)

try:
    os.system(f'sudo chmod a+rw {args.device_name}')
    os.system(f'fuser -k {args.device_name}')
    serial_device = serial.Serial(args.device_name, args.baud_rate, timeout=1)
except serial.SerialException:
    print(f'Error: Could not open the serial port {args.device_name}')
    exit(1)

if args.eeprom_label == 'identity':
    identity_eeprom.send_to_serial(serial_device)
elif args.eeprom_label == 'alu':
    alu_logic_eeprom.send_to_serial(serial_device)
elif args.eeprom_label == 'decoderA':
    control_logic_eeproms.get_eeprom('A').send_to_serial(serial_device)
elif args.eeprom_label == 'decoderB':
    control_logic_eeproms.get_eeprom('B').send_to_serial(serial_device)
elif args.eeprom_label == 'decoderC':
    control_logic_eeproms.get_eeprom('C').send_to_serial(serial_device)
elif args.eeprom_label == 'decoderD':
    control_logic_eeproms.get_eeprom('D').send_to_serial(serial_device)
elif args.eeprom_label == 'decoderE':
    control_logic_eeproms.get_eeprom('E').send_to_serial(serial_device)
elif args.eeprom_label == 'decoderF':
    control_logic_eeproms.get_eeprom('F').send_to_serial(serial_device)
else:
    print("Enter EEPROM name:\n[identity / alu / decoderA / decoderB / decoderC / decoderD / decoderE / decoderF]")

serial_device.flushInput()
serial_device.flushOutput()
serial_device.close()
