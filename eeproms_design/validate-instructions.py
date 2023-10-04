import json
import jsonschema

MICROCODES_FILENAME = 'microcodes.json'
INSTRUCTIONS_FILENAME = 'instructions.json'

with open(MICROCODES_FILENAME, 'r') as input_file:
    microcodes = json.load(input_file)

with open(INSTRUCTIONS_FILENAME, 'r') as input_file:
    instructions = json.load(input_file)

for key, value in instructions.items():
    error = False
    for microcode in value:
        if not microcode in microcodes:
            error = True   
            print(f'{key:30}Validation failed. Not found microcode: {microcode}') 
            break
    if not error:
        print(f'{key:30}Validation successful')

