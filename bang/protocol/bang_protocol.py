# -*- coding: utf-8 -*-
# =============================================================================
# Created on May 2018
#
# ######################### Movie protocol ####################################
#
# Author: Ana Luísa Pinho
# email: ana.pinho@inria.fr
# =============================================================================

import os
import csv
import numpy as np

from confparser import load_config

import expyriment
from expyriment import design, control, stimuli, io, misc

# %%
# ======================== LOAD CONFIG.INI FILE ===========================
# Select .ini file for instructions
setting = load_config('config.ini')

# %%
# ========================== SET DEFAULT KEYS =================================
# Prevent 'p' key to pause the experiment
control.defaults.pause_key = None

# %%
# ========================== INITIALIZATION ===================================
#
# (1) Present the startup screen with the countdown;
# (2) Start an experimental clock, create the screen;
# (3) Create an event file;
# (4) Present "Preparing experiment"
#
# =============================================================================
exp = design.Experiment(setting["exp_name"], background_colour=(127, 127, 127))

control.initialize(exp)

# %%
# ============================== INPUTS =======================================
# Define the pathway of the video files
input_path = os.path.abspath(setting["video_path"])

# Define list of inputs filenames
film_list = [input_path + '/' + i[0] + '.' + setting["ext"] for i in
             csv.reader(open(setting["inputs_filenames"] + '.csv'))]

film_name_list = [j[0] for j in
                  csv.reader(open(setting["inputs_filenames"] + '.csv'))]

# Define number of runs
nb_block = len(film_list)

# %%
# ============= WAITS FOR USER TO ENTER RUN NUMBER TO START ===================

# Wait 5 seconds in order to launch input text screen
exp.keyboard.wait(duration=5000)

# Create text input box
ti = io.TextInput(message='Number of the Run:', message_text_size=24,
                  message_colour=map(int, setting["bcolor"]),
                  user_text_colour=map(int, setting["ucolor"]),
                  ascii_filter=misc.constants.K_ALL_DIGITS,
                  background_colour=(0, 0, 0),
                  frame_colour=(70, 70, 70))

# Load user's input
while True:
    sb = ti.get('0')
    # If string is empty
    if not sb:
        warning_message1 = stimuli.TextLine(setting["wm1"], text_size=24,
                                            text_colour=(204, 0, 0))
        warning_message1.present()
        exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
        continue
    # If run (aka block) number introduced is higher than the number of
    # runs preset in config file
    elif int(sb) >= nb_block:
        warning_message2 = stimuli.TextLine(setting["wm2"], text_size=24,
                                            text_colour=(204, 0, 0))
        warning_message2.present()
        exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
        continue
    else:
        start_block = int(sb)
        break

# %%
# ============================== DESIGN =======================================
# Define the pathway of the video files
input_path = os.path.abspath(setting["video_path"])

# Define list of inputs filenames
film_list = [input_path + '/' + i[0] + '.' + setting["ext"] for i in
             csv.reader(open(setting["inputs_filenames"] + '.csv'))]

film_name_list = [j[0] for j in
                  csv.reader(open(setting["inputs_filenames"] + '.csv'))]


# Define the blocks using expyriment module
block_list = [expyriment.design.Block(name="block%d" % bs)
              for bs in np.arange(nb_block)]

# For all runs, add video to the trial and add trial to the run
for bl, film in enumerate(film_list):
    # Create a trial
    trial = design.Trial()
    # Retrieve variables from input files at every trial and
    # label them according to what is defined by var_names
    trial.set_factor(setting["var_names"], film_name_list[bl])
    # Create stimulus
    # stim = stimuli.TextLine(line)
    stim = stimuli.Video(film)
    # Add stimulus to the trial
    trial.add_stimulus(stim)
    # Add trial to block
    block_list[bl].add_trial(trial)

# Add block to the experiment
for ad in np.arange(nb_block):
    exp.add_block(block_list[ad])

# Print exp. variable names in the log file
exp.data_variable_names = setting["llog_var_names"]

# %%
# ==================== DEFINE AND PRELOAD SOME STIMULI ========================
# TTL cross
fixcross_TTL = stimuli.FixCross(size=(30, 30), line_width=5,
                                colour=(255, 255, 0))
fixcross_TTL.preload()

# Trial cross
fixcross = stimuli.FixCross(size=(30, 30), line_width=5, colour=(0, 0, 0))
fixcross.preload()

# Blank screen before sentence display
blank1 = stimuli.BlankScreen(colour=None)
blank1.preload()

# Text for end of Run
text_end_run = stimuli.TextLine(setting["text_end_run"], text_size=44,
                                text_colour=(255, 153, 51))
text_end_run.preload()

# Text for end of Session
text_end = stimuli.TextBox(str(''.join((setting["text_end_exp_one"],
                            '\n\n',
                            setting["text_end_exp_two"]))).decode('utf-8'),
                           (1000, 1000), position=(0, -400),
                           text_size=44, text_colour=(255, 153, 51))
text_end.preload()

# %%
# ================================ RUN ========================================
# =============================================================================
# Starts running the experiment:
# (1) Present a screen asking for the subject no. (exp.subject) and
#     wait for the RETURN key
# (2) Create a data file (exp.data)
# (3) Present the "Ready" screen
# =============================================================================
control.start(exp, skip_ready_screen=True)
# Stop audio system
control.stop_audiosystem()

# =============================================================================
# Run the protocol
# =============================================================================
for b, block in enumerate(exp.blocks[start_block:]):
    # Start at any run number
    block_no = b + start_block
    # Display fixation cross that sets the beginning of the experiment
    fixcross_TTL.present()
    # Wait for TTL
    exp.keyboard.wait_char('t')
    exp.screen.clear()
    exp.screen.update()
    # Creates the clock
    t0 = misc.Clock()
    # Set video as stimulus for the single trial pertaining every block
    for trial in block.trials:
        for stimulus in trial.stimuli:
            # Getter for the time in milliseconds since clock init.
            # Time for the beginning of the trial
            t_start = t0.time
            # Preload video
            stimulus.preload()
            # Present video
            stimulus.play()
            stimulus.present()
            stimulus.wait_end()
            stimulus.stop()
            # Calculate duration of the video display
            duration = t0.time - t_start
            # Log file registry for the current trial
            exp.data.add([block_no,
                          trial.get_factor(
                                setting["var_names"]), t_start, duration])
    # Display fixation cross for 10 seconds before the end of the trial
    exp.screen.clear()
    exp.screen.update()
    fixcross.present()
    exp.clock.wait(setting["WAIT"])
    exp.screen.clear()
    exp.screen.update()
    # End of session
    if block_no < (nb_block - 1):
        # Wait for "ENTER", while displaying the message, in order to pass
        # to the next session
        text_end_run.present()
        exp.keyboard.wait(keys=[misc.constants.K_RETURN])
    else:
        # Wait for "ENTER", while displaying the message, in order to quit
        # the protocol
        text_end.present()
        exp.keyboard.wait(keys=[misc.constants.K_RETURN])
# End of the experiment
control.end()
