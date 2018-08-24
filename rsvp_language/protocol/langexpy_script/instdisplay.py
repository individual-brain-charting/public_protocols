# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

from confparser import load_config
from expyriment import stimuli, misc


def launch_instructions(instructions_ini, exp):
    # Select .ini file for instructions
    setting = load_config(instructions_ini)
    # Define the pathway of the instructions file
    instructions_fname = ''.join((setting["inst_filename"], ".csv"))
    instructions_dir = os.path.abspath((setting["inputs_dir"]))
    instructions_path = os.path.join(instructions_dir, instructions_fname)
    # Generate a dataframe containing the instructions
    df_inst = pd.read_csv(instructions_path, sep='|')
    # Convert the dataframe into a list
    instructions = df_inst.values.tolist()
    # Convert each element of the dataframe into a string
    instructions = [[''.join(instructions[i][j])
                     for j in np.arange(len(instructions[i]))]
                    for i in np.arange(len(df_inst))]
    # Initialization of variable containing the value of the key pressed
    found_key = 0
    response_key = 0
    # While "h" key to return to main menu is not pressed...
    while not (found_key == misc.constants.K_h or response_key == 'h'):
        # Read the instructions file, line by line
        ldx = 0
        while ldx < len(instructions):
            line = instructions[ldx]
            # ... and item by item
            for word in line:
                # For lines with one item
                if word in ("no_item", "no_probe", "fdbk_yes",
                            "fdbk_no"):
                    pass
                # For lines corresponding to the examples, i.e. containing
                # more than one item
                else:
                    text_display = stimuli.TextBox(
                        word.decode('utf-8'),
                        map(int, setting["box_size"]),
                        position=map(int, setting["box_position"]),
                        text_size=setting["txtsize"],
                        text_colour=map(int, setting["txtcolour"]))
                    text_display.present()
                    exp.clock.wait(300)
                    # Check whether "h" key was pressed
                    found_key = exp.keyboard.check([misc.constants.K_h])
                    # If yes, breaks the loop
                    if found_key == misc.constants.K_h:
                        break
            # If "h" key was pressed during the presentation of the example,
            # it breaks the loop and return to main menu
            if found_key == misc.constants.K_h:
                break
            # After the display of the last word of sentence's example,
            # goes straight to the next line of instructions
            elif line[-1] not in ("no_item", "fdbk_yes", "fdbk_no"):
                exp.clock.wait(300)
            # Waits for the participant's response and gives feedback whether
            # the answer was correct or not
            elif line[-1] in ("fdbk_yes", "fdbk_no"):
                response_key, _ = exp.keyboard.wait_char([setting["YES"],
                                                          setting["NO"], 'h'])
                if response_key == 'h':
                    break
                elif ((response_key == setting["YES"] and
                       line[-1] == "fdbk_yes") or
                      (response_key == setting["NO"] and
                       line[-1] == "fdbk_no")):
                    message_display = stimuli.TextLine(
                        "Correct!", text_size=setting["txtsize"],
                        text_colour=(0, 204, 0))
                    message_display.present()
                    exp.clock.wait(2000)
                else:
                    message_display = stimuli.TextLine(
                        "Incorrect!", text_size=setting["txtsize"],
                        text_colour=(255, 0, 0))
                    message_display.present()
                    exp.clock.wait(2000)
            # Checks whether "ENTER", "LEFT" or m" key were pressed.
            # If "ENTER", goes to the next line;
            # if "LEFT", goes to the previous slide
            # if "h", returns to main menu.
            else:
                found_key, _ = exp.keyboard.wait([misc.constants.K_RETURN,
                                                  misc.constants.K_LEFT,
                                                  misc.constants.K_h])
                if found_key == misc.constants.K_LEFT:
                    ldx = ldx - 2
                    if ldx < 0:
                        ldx = -1
                elif found_key == misc.constants.K_h:
                    break
            ldx = ldx + 1
