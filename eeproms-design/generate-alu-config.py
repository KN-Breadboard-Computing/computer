prefixes = [
    "NEGA", "NEGB", "ADD", "SUBAB", "SUBBA", 
    "MULA2", "MULB2", "DIVA2", "DIVB2", 
    "INVA", "INVB", "OR", "AND", "XOR",
    "SHRA", "SHRB", "SHLA", "SHLB"
]

operation = [
    "negation", "negation", "sum", "difference", "difference", 
    "multiplication", "multiplication", "quotient", "quotient",
    "bit inversion", "bit inversion", "alternative", "conjunction", "exclusive disjunction",
    "right shift", "right shift", "left shift", "left shift"
]

args = [
    "\\\\texttt{REG_A}", 
    "\\\\texttt{REG_B}", 
    "\\\\texttt{REG_A} and \\\\texttt{REG_B}",
    "\\\\texttt{REG_A} and \\\\texttt{REG_B}",
    "\\\\texttt{REG_B} and \\\\texttt{REG_A}",
    "\\\\texttt{REG_A} and \\\\texttt{2}",
    "\\\\texttt{REG_B} and \\\\texttt{2}",
    "\\\\texttt{REG_A} and \\\\texttt{2}",
    "\\\\texttt{REG_B} and \\\\texttt{2}",
    "\\\\texttt{REG_A}", 
    "\\\\texttt{REG_B}", 
    "\\\\texttt{REG_A} and \\\\texttt{REG_B}",
    "\\\\texttt{REG_A} and \\\\texttt{REG_B}",
    "\\\\texttt{REG_A} and \\\\texttt{REG_B}",
    "\\\\texttt{REG_A}", 
    "\\\\texttt{REG_B}", 
    "\\\\texttt{REG_A}", 
    "\\\\texttt{REG_B}",
]

sufixes = ["A", "B", "MEM", "MEMZP", "STC"]
targets = ["to \\\\texttt{REG_A}", "to \\\\texttt{REG_B}", "to memory at given address", "to zero page memory at given address", "on stack"]

counter = 41
category = "ALU instructions"


for pre_index, pre in enumerate(prefixes):
    for suf_index, suf in enumerate(sufixes):
        name = f"{pre}{suf}"
        opcode = f"0b{bin(counter + 1)[2:].zfill(8)}"
        description = f"Calculate {operation[pre_index]} of {args[pre_index]} and save it {targets[suf_index]}"
        mc_description = ""
        
        print(f'"{name}":{{"id":{counter}, "name":"{name}", "category":"{category}", "opcode":"{opcode}", "arguments": [], "description":"{description}", "microcodes-description": "{mc_description}"}},')

        counter += 1