import json
import jsonschema

ALU_SCHEME_FILENAME = '../config/alu_scheme.json'
MICROCODES_SCHEME_FILENAME = '../config/microcodes_scheme.json'
INSTRUCTIONS_SCHEME_FILENAME = '../config/instructions_scheme.json'

ALU_DESCRIPTION_FILENAME = '../config/alu.json'
MICROCODES_DESCRIPTION_FILENAME = '../config/microcodes.json'
INSTRUCTIONS_DESCRIPTION_FILENAME = '../config/instructions.json'


def validate_alu():
    print('Alu validation:')
    with open(ALU_SCHEME_FILENAME, 'r') as input_file:
        schema = json.load(input_file)

    with open(ALU_DESCRIPTION_FILENAME, 'r') as input_file:
        alu_desc = json.load(input_file)
        alu_config = alu_desc['config']
        alu_codes = alu_desc['codes']

    for key, value in alu_codes.items():
        try:
            jsonschema.validate(instance=value, schema=schema)
            if value['MULTIPLEXER_OUTPUT'] not in alu_config['multiplexer-output']:
                print(f'{key:30}Validation failed. Not found specified multiplexer output type.')
            else:
                print(f'{key:30}Validation successful.')
        except jsonschema.exceptions.ValidationError as e:
            print(f'{key:30}Validation failed. Incorrect schema.')
    print()


def validate_microcodes():
    print('Microcodes validation:')
    with open(MICROCODES_SCHEME_FILENAME, "r") as input_file:
        schema = json.load(input_file)

    with open(MICROCODES_DESCRIPTION_FILENAME, "r") as input_file:
        microcodes = json.load(input_file)

    for key, value in microcodes.items():
        try:
            jsonschema.validate(instance=value, schema=schema)
            print(f"{key:40}Validation successful.")
        except jsonschema.exceptions.ValidationError as e:
            print(f"{key:40}Validation failed. Incorrect schema.")
    print()


def validate_instructions():
    print('Instructions validation:')
    with open(INSTRUCTIONS_SCHEME_FILENAME, "r") as input_file:
        schema = json.load(input_file)

    with open(MICROCODES_DESCRIPTION_FILENAME, 'r') as input_file:
        microcodes = json.load(input_file)

    with open(INSTRUCTIONS_DESCRIPTION_FILENAME, 'r') as input_file:
        instructions = json.load(input_file)

    for key, value in instructions.items():
        try:
            jsonschema.validate(instance=value, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            print(f"{key:20}Validation failed. Incorrect schema.")
            continue

        error = False
        for microcode in value["microcodes"]:
            if not microcode in microcodes:
                error = True   
                print(f'{key:20}Validation failed. Not found microcode: {microcode}.') 
                break
        if not error:
            print(f'{key:20}Validation successful.')
    print()


validate_alu()
validate_microcodes()
validate_instructions()
