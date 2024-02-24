from pathlib import Path

class Config:

    def __init__(self, path=Path(''), instructions=None, microcodes=None, signals=None, alu=None):
        def get_path(file, default):
            if isinstance(file, Path):
                return file if file.is_absolute() else path / file
            else:
                file = Path(file) if file is not None else Path(default)
                return path / file
        
        self._instructions_path = get_path(instructions, 'instructions.json')
        self._microcodes_path = get_path(microcodes, 'microcodes.json')
        self._signals_path = get_path(signals, 'signals.json')
        self._alu_path = get_path(alu, 'alu.json')

    def get_instructions(self):
        return self._instructions_path

    def get_microcodes(self):
        return self._microcodes_path

    def get_signals(self):
        return self._signals_path

    def alu():
        return self._alu_path
