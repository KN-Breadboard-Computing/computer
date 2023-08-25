import json
import jsonschema

SCHEME_FILENAME = "signals-scheme.json"
MICROCODES_FILENAME = "microcodes.json"

if __name__ == '__main__':
    with open(SCHEME_FILENAME, "r") as input_file:
        schema = json.load(input_file)

    with open(MICROCODES_FILENAME, "r") as input_file:
        microcodes = json.load(input_file)

    for key, value in microcodes.items():
        try:
            jsonschema.validate(instance=value, schema=schema)
            print(f"{key:40}Validation successful")
        except jsonschema.exceptions.ValidationError as e:
            print(f"{key:40}Validation failed")
