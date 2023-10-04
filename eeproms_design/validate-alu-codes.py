import json
import jsonschema

SCHEME_FILENAME = 'alu-logic-scheme.json'
ALU_LOGIC_DESCRIPTION_FILENAME = 'alu-logic.json'

with open(SCHEME_FILENAME, 'r') as input_file:
    schema = json.load(input_file)

with open(ALU_LOGIC_DESCRIPTION_FILENAME, 'r') as input_file:
    alu_desc = json.load(input_file)
    alu_config = alu_desc['config']
    alu_codes = alu_desc['codes']

for key, value in alu_codes.items():
    try:
        jsonschema.validate(instance=value, schema=schema)
        if value['MULTIPLEXER_OUTPUT'] not in alu_config['multiplexer-output']:
            print(f'{key:30}Validation failed. Not found specified multiplexer output type')
        else:
            print(f'{key:30}Validation successful')
    except jsonschema.exceptions.ValidationError as e:
        print(f'{key:30}Validation failed')
