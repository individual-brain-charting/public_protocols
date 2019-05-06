# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

from confparser import load_config
from expyriment import stimuli, misc


def launch_instructions(instructions_ini, exp):
    # Select .ini file for instructions
    setting = load_config(instructions_ini)
    # Define the pathway of files
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
            # For lines corresponding to an audio file display
            if line[0] in setting["audio_examples"]:
                speaker = stimuli.Picture(instructions_dir + '/' +
                                          setting["speaker_fname"] +
                                          '.png')
                speaker.present()
                audio_example = stimuli.Audio(instructions_dir + '/' +
                                              line[0] + '.' +
                                              setting["ext"])
                audio_example.present()
                exp.clock.wait(2000)
            # For lines corresponding to the feedback period after the
            # event's presentation
            elif line[0] == '?':
                # Presentation of question mark picture
                qmark = stimuli.Picture(instructions_dir + '/' +
                                        setting["qmark_fname"] +
                                        '.png')
                qmark.present()
                # Check whether "LEFT", "RIGHT" or "h" key were pressed
                response_key, _ = exp.keyboard.wait_char([
                    setting["LEFT_BUTTON"], setting["RIGHT_BUTTON"], 'h'])
                # "h" key pressed --> breaks the loop
                if response_key == 'h':
                    break
                # Otherwise, display the result of the reply
                elif ((response_key == setting["LEFT_BUTTON"] and
                       line[-1] == "fdbk_left") or
                      (response_key == setting["RIGHT_BUTTON"] and
                       line[-1] == "fdbk_right")):
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
            # For all remaining lines presenting the instructions
            else:
                text_display = stimuli.TextBox(
                    line[0].decode('utf-8'),
                    map(int, setting["box_size"]),
                    position=map(int, setting["box_position"]),
                    text_size=setting["txtsize"],
                    text_colour=map(int, setting["txtcolour"]))
                text_display.present()
            # After the display of the event audio file,
            # goes straight to the question mark
            if line[-1] == 'event':
                exp.clock.wait(300)
            # Otherwise, checks whether "ENTER", "LEFT" or m" key were pressed.
            # If "ENTER", goes to the next line;
            # if "LEFT", goes to the previous slide;
            # if "h", returns to main menu.
            else:
                found_key, _ = exp.keyboard.wait([misc.constants.K_RETURN,
                                                  misc.constants.K_LEFT,
                                                  misc.constants.K_h])
            if found_key == misc.constants.K_h:
                break
            elif found_key == misc.constants.K_LEFT:
                ldx = ldx - 2
                if ldx < 0:
                    ldx = -1
            ldx = ldx + 1
