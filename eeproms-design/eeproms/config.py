from pathlib import Path


class Config:
    def __init__(self, configs_path=Path(''), instructions_filename='instructions.json',
                 microcodes_filename='microcodes.json', signals_filename='signals.json', alu_logic_filename='alu.json'):
        def get_path(file, default):
            if isinstance(file, Path):
                return file if file.is_absolute() else configs_path / file
            else:
                file = Path(file) if file is not None else Path(default)
                return configs_path / file

        self._instructions_path = get_path(instructions_filename, 'instructions.json')
        self._microcodes_path = get_path(microcodes_filename, 'microcodes.json')
        self._signals_path = get_path(signals_filename, 'signals.json')
        self._alu_path = get_path(alu_logic_filename, 'alu.json')

    def get_instructions(self):
        return self._instructions_path

    def get_microcodes(self):
        return self._microcodes_path

    def get_signals(self):
        return self._signals_path

    def get_alu(self):
        return self._alu_path
