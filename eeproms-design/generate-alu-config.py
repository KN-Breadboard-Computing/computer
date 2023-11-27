# math operations generating

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

mnemonic = [
    "NEG", "NEG", "ADD", "SUB", "SUB", "MUL", "MUL", "DIV", "DIV",
    "INV", "INV", "OR", "AND", "XOR", "SHR", "SHR", "SHL", "SHL"
]

mnemonic_args = [ 
    ["A"], ["B"], [], ["A", "B"], ["B", "A"], ["A"], ["B"], ["A"], ["B"],
    ["A"], ["B"], [], [], [], ["A"], ["B"], ["A"], ["B"]  
]

mnemonic_operator = [
    "-", "-", "+", "-", "-", "*", "*", "/", "/",
    "~", "~", "OR", "AND", "XOR", ">>", ">>", "<<", "<<"  
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

regs = ["A", "B", "TH", "TL"]

counter = 41
category = "ALU instructions"

for pre_index, pre in enumerate(prefixes):
    for suf_index, suf in enumerate(sufixes):
        name = f"{pre}{suf}"
        opcode = f"0b{bin(counter + 1)[2:].zfill(8)}"
        args_list = ""
        for arg in mnemonic_args[pre_index]:
            if args_list != "":
                args_list += ", "
            args_list = f'{args_list}"{arg}"'
        if suf == "A" or suf == "B":
            if args_list != "":
                args_list += ", "
            args_list = f'{args_list}"{suf}"'
        elif suf == "MEM":
            if args_list != "":
                args_list += ", "
            args_list = f'{args_list}"MEM8"'
        elif suf == "MEMZP":
            if args_list != "":
                args_list += ", "
            args_list = f'{args_list}"MEM16"'
        elif suf == "STC":
            if args_list != "":
                args_list += ", "
            args_list = f'{args_list}"STC"'
        description = f"Calculate {operation[pre_index]} of {args[pre_index]} and save it {targets[suf_index]}"
        
        if suf == "A" or suf == "B":
            if len(mnemonic_args[pre_index]) == 1:
                mc_description = f"\\\\( \\\\texttt{{REG_{suf}}} \\\\leftarrow {mnemonic_operator[pre_index]}{args[pre_index]} \\\\quad \\\\& \\\\quad \\\\texttt{{save flags to }} \\\\texttt{{REG_F}} \\\\)"
            else:
                op = args[pre_index].replace("and", mnemonic_operator[pre_index])
                mc_description = f"\\\\( \\\\texttt{{REG_{suf}}} \\\\leftarrow {op} \\\\quad \\\\& \\\\quad \\\\texttt{{save flags to }} \\\\texttt{{REG_F}} \\\\)"
        elif suf == "MEM":
            if len(mnemonic_args[pre_index]) == 1:
                mc_description = f"\\\\( \\\\texttt{{REG_MAR}} \\\\leftarrow \\\\texttt{{PC}} \\\\) <br> \\\\( \\\\texttt{{REG_TMPH}} \\\\leftarrow \\\\texttt{{MEM[REG_MAR]}} \\\\quad \\\\& \\\\quad \\\\texttt{{PC}} \\\\leftarrow \\\\texttt{{PC+1}} \\\\) <br> \\\\( \\\\texttt{{REG_MAR}} \\\\leftarrow \\\\texttt{{PC}} \\\\) <br> \\\\( \\\\texttt{{REG_TMPL}} \\\\leftarrow \\\\texttt{{MEM[REG_MAR]}} \\\\quad \\\\& \\\\quad \\\\texttt{{PC}} \\\\leftarrow \\\\texttt{{PC+1}} \\\\) <br> \\\\( \\\\texttt{{REG_MAR}} \\\\leftarrow \\\\texttt{{REG_TMP}} \\\\) <br> \\\\( \\\\texttt{{REG_MBR}} \\\\leftarrow {mnemonic_operator[pre_index]}{args[pre_index]} \\\\quad \\\\& \\\\quad \\\\texttt{{save flags to }} \\\\texttt{{REG_F}} \\\\) <br> \\\\( \\\\texttt{{MEM[REG_MAR]}} \\\\leftarrow \\\\texttt{{REG_MBR}} \\\\)"
            else:
                op = args[pre_index].replace("and", mnemonic_operator[pre_index])
                mc_description = f"\\\\( \\\\texttt{{REG_MAR}} \\\\leftarrow \\\\texttt{{PC}} \\\\) <br> \\\\( \\\\texttt{{REG_TMPH}} \\\\leftarrow \\\\texttt{{MEM[REG_MAR]}} \\\\quad \\\\& \\\\quad \\\\texttt{{PC}} \\\\leftarrow \\\\texttt{{PC+1}} \\\\) <br> \\\\( \\\\texttt{{REG_MAR}} \\\\leftarrow \\\\texttt{{PC}} \\\\) <br> \\\\( \\\\texttt{{REG_TMPL}} \\\\leftarrow \\\\texttt{{MEM[REG_MAR]}} \\\\quad \\\\& \\\\quad \\\\texttt{{PC}} \\\\leftarrow \\\\texttt{{PC+1}} \\\\) <br> \\\\( \\\\texttt{{REG_MAR}} \\\\leftarrow \\\\texttt{{REG_TMP}} \\\\) <br> \\\\( \\\\texttt{{REG_MBR}} \\\\leftarrow {op} \\\\quad \\\\& \\\\quad \\\\texttt{{save flags to }} \\\\texttt{{REG_F}} \\\\) <br> \\\\( \\\\texttt{{MEM[REG_MAR]}} \\\\leftarrow \\\\texttt{{REG_MBR}} \\\\)"

        else:
            mc_description = ""
        
        #print(f'"{name}":{{"id":{counter}, "name":"{name}", "category":"{category}", "opcode":"{opcode}", "mnemonic":"{mnemonic[pre_index]}", "arguments": [{args_list}], "microcodes": [], "description":"{description}", "microcodes-description": "{mc_description}"}},')

        counter += 1


# comparisions generating
for i in range(len(regs)):
    for j in range(i + 1, len(regs)):
        reg1 = regs[i]
        reg2 = regs[j]
        name = f"CMP{reg1}{reg2}"
        opcode = f"0b{bin(counter + 1)[2:].zfill(8)}"
        description = f"Save flags of operation \\\\texttt{{REG_{reg1}}} - \\\\texttt{{REG_{reg2}}} to \\\\texttt{{REG_F}}"
        mc_description = f"\\\\(\\\\texttt{{calculate}} \\\\quad \\\\texttt{{REG_A}} - \\\\texttt{{REG_B}} \\\\quad \\\\& \\\\quad \\\\texttt{{save flags to}} \\\\texttt{{REG_F}} \\\\)"
        #print(f'"{name}":{{"id":{counter}, "name":"{name}", "category":"{category}", "opcode":"{opcode}", "mnemonic":"CMP", "arguments": ["{reg1}","{reg2}"], "microcodes": [], "description":"{description}", "microcodes-description": "{mc_description}"}},')

        counter += 1

# clear generating
for reg in ["A", "B", "TMP", "TH", "TL"]:
    name = f"CLR{reg}"
    opcode = f"0b{bin(counter + 1)[2:].zfill(8)}"
    description = f"Set value of \\\\texttt{{REG_{reg}}} to \\\\texttt{{0}}"
    mc_description = f"\\\\( \\\\texttt{{REG_{reg}}} \\\\leftarrow \\\\texttt{{0}} \\\\)"
    #print(f'"{name}":{{"id":{counter}, "name":"{name}", "category":"{category}", "opcode":"{opcode}", "mnemonic":"CLR", "arguments": ["{reg}"], "microcodes": [], "description":"{description}", "microcodes-description": "{mc_description}"}},')

    counter += 1

# increment generating
for reg in ["A", "B", "TMP", "TH", "TL"]:
    name = f"INC{reg}"
    opcode = f"0b{bin(counter + 1)[2:].zfill(8)}"
    description = f"Increment value of \\\\texttt{{REG_{reg}}}"
    mc_description = f"\\\\( \\\\texttt{{REG_{reg}}} \\\\leftarrow \\\\texttt{{REG_{reg} + 1}}  \\\\)"
    print(f'"{name}":{{"id":{counter}, "name":"{name}", "category":"{category}", "opcode":"{opcode}", "mnemonic":"INC", "arguments": ["{reg}"], "microcodes": [], "description":"{description}", "microcodes-description": "{mc_description}"}},')

    counter += 1

# decrement generating
for reg in ["A", "B", "TMP", "TH", "TL"]:
    name = f"DEC{reg}"
    opcode = f"0b{bin(counter + 1)[2:].zfill(8)}"
    description = f"Decrement value of \\\\texttt{{REG_{reg}}}"
    mc_description = f"\\\\( \\\\texttt{{REG_{reg}}} \\\\leftarrow \\\\texttt{{REG_{reg} - 1}}  \\\\)"
    print(f'"{name}":{{"id":{counter}, "name":"{name}", "category":"{category}", "opcode":"{opcode}", "mnemonic":"DEC", "arguments": ["{reg}"], "microcodes": [], "description":"{description}", "microcodes-description": "{mc_description}"}},')

    counter += 1
