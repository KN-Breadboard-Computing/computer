import os

from argparse import ArgumentParser
from pathlib import Path

from eeproms.control_unit_eeproms import ControlUnitEeproms
from eeproms.alu_eeprom import AluLogicEeprom
from eeproms.config import Config
from eeproms.interrupts_eeprom import InterruptsEeprom

EEPROMS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'BRANCH', 'INT']

parser = ArgumentParser(description='Dump the contents of EEPROMs to files')
parser.add_argument('--config-dir', default=os.getcwd(), help='Path to the directory containing the config JSON files')
parser.add_argument('--microcodes-config', default='microcodes.json',
                    help='Path to the microcodes JSON file. It will be resolved against the config directory unless the provided path is absolute')
parser.add_argument('--output-dir', default=os.getcwd(), help='Path to the destination directory')
parser.add_argument('--eeproms', nargs='*', default=EEPROMS, help='EEPROM labels to dump. Dumps all by default')

args = parser.parse_args()

config_path = Path(args.config_dir)
output_path = Path(args.output_dir)

eeproms = set()
for eeprom in args.eeproms:
    eeprom = eeprom.upper()
    if eeprom not in EEPROMS:
        print(f'fatal: Unknown EEPROM {eeprom}')
        exit(1)
    else:
        eeproms.add(eeprom)

print(f'Config path set to {config_path}')
print(f'Output path set to {output_path}')
print(f'EEPROMs do dump: {" ".join(eeproms)}')

config = Config(config_path, microcodes_filename=args.microcodes_config)
control_unit_eeproms = ControlUnitEeproms(config)
int_eeprom = InterruptsEeprom()

for eeprom in eeproms:
    path = output_path / f'{eeprom}.bin'
    if eeprom == 'INT':
        int_eeprom.save_to_file(path)
    else:
        control_unit_eeproms.get_eeprom(eeprom).save_to_file(path)

print('Done')
