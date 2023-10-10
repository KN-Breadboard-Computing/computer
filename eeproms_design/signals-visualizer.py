import sys
import json
import webbrowser

index_file_path = 'index.html'

INSTRUCTIONS_FILENAME = 'instructions.json'
MICROCODES_FILENAME = 'microcodes.json'
SIGNALS_IDENTIFIERS_FILENAME = 'signals-identifiers.json'

def process_signals(instruction_names):
    with open(INSTRUCTIONS_FILENAME, 'r') as input_file:
        instructions = json.load(input_file)

    with open(MICROCODES_FILENAME) as input_file:
        microcodes = json.load(input_file)

    with open(SIGNALS_IDENTIFIERS_FILENAME) as input_file:
        signals = json.load(input_file)

    for instruction_name in instruction_names:
        if not instruction_name in instructions:
            print(f"Instruction '{instruction_name} does not exist!")
            sys.exit()

    microcodes_to_process = []
    name = ""
    for instruction_name in instruction_names:
        if name == "":
            name = instruction_name
        else:
            name = name + "-" + instruction_name

        if instruction_name  != 'FETCH' and instruction_name != 'ENTER_PROGRAM':
            microcodes_to_process += instructions['FETCH'] 

        microcodes_to_process += instructions[instruction_name]

    descriptions = []
    ticks_number = len(microcodes_to_process)

    clk_values = ['L']
    not_clk_values = ['H']
    for i in range(ticks_number):
        clk_values += ['H', 'L']
        not_clk_values += ['L', 'H']

    descriptions.append(["CLK"] + clk_values)
    descriptions.append(["~CLK"] + not_clk_values)

    for key in signals.keys():
        values = []
        for index, mc in enumerate(microcodes_to_process):
            if signals[key][1] == "~CLK":
                combined = " (&~CLK)"
                if(microcodes[mc][key] == 0):
                    values += ['L', 'L']
                else:
                    values += ['L', 'H']
            elif signals[key][1] == "CLK":
                combined = " (&CLK)"
                if(microcodes[mc][key] == 0):
                    values += ['L', 'L']
                else:
                    values += ['H', 'L']
            else:
                combined = ""
                if(microcodes[mc][key] == 0):
                    values += ['L', 'L']
                else:
                    values += ['H', 'H']

            if index == 0:
                values = [values[1]] + values

        descriptions.append([key + combined] + values)

    return name, microcodes_to_process, descriptions


def draw_signals(name, microsteps, signals_description):
    microsteps_description = ""
    for index, microstep in enumerate(microsteps):
        microsteps_description += """<tr><td style="background-color:purple; color:white;">{index}</td>  <td style="background-color:orange;">{microstep}</td></tr>""".format(microstep=microstep, index=index)

    signals_table_content = ""
    signals_table_content += """<tr style="background-color:yellow;">"""
    signals_table_content += """<td>signal name</td>    <td>init</td>"""
    for index in range(len(microsteps)):
        signals_table_content += """<td></td>   <td colspan="2">{index}</td>""".format(index = index)
    signals_table_content += """</tr>"""

    for signal in signals_description:
        signals_table_content += """
        <tr>
            <td style="background-color:navy; color:white; padding-right: 10px;">{signal_name}</td>
        """.format(signal_name=signal[0])

        for index, val in enumerate(signal[1:]):
            if index % 2 == 1:
                signals_table_content += """<td style="background-color:black;"></td>"""

            if val == 'L':
                signals_table_content += """<td style="width: 30px; background-color:red;">L</td>"""
            elif val == 'H':
                signals_table_content += """<td style="width: 30px; background-color:green;">H</td>"""
            else:
                print('ERROR')
        
        signals_table_content += """</tr>"""

    html_string = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <style>
            table, th, td {{
                border: 1px solid black;
                border-collapse: collapse;
            }}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <td> 
                    <table>
                        {microsteps_description}
                    </table>
                    <p>LOAD works on LOW to HIGH tick</p>
                    <p>TICK works on LOW to HIGH tick</p>
                    <p>EEPROM->REGS LATCHes are connected to CLK</p>
                </td>
                <td> 
                    <table>
                        {signals_table}
                    </table>
                </td>
            </tr>
        </table>
    </body>
    """.format(microsteps_description=microsteps_description, signals_table=signals_table_content)

    index_file_path = f"instructions_visualisations/{name}.html"

    with open(index_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_string)

    webbrowser.open_new_tab(index_file_path)

if len(sys.argv) > 1:
    instruction_names = sys.argv[1:]

    draw_signals(*process_signals(instruction_names))
