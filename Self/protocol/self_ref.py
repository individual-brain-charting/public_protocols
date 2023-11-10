#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# Protocol on Self-Representation and Memory for the IBC project
#
# Author: Sarah Genon
# Adapted to Expyriment by: Ana Luísa Pinho
#
# email: ana.pinho@inria.fr
#
# Date: May 2018
# =============================================================================

import sys

from protocol import launch_protocol
from confparser import load_config

from expyriment import design, control, stimuli, io

# %%
# ======================== SET DEVELOPMENT MODE ===============================
# For older versions than 0.9.0 (compatible with 0.9.0)
control.set_develop_mode(False)

# %%
# ========================== SET DEFAULT KEYS =================================
# Prevent 'p' key to pause the experiment
control.defaults.pause_key = None

# %%
# ========== SET COMMAND-LINE ARGUMENTS TO BE PASSED TO THE SCRIPT ============
assert(len(sys.argv) > 1), "No arg was introduced. " + \
                           "You must pass two valid args to the script."
gender_stim = sys.argv[1]
assert(gender_stim in ['male', 'female']), \
    "Not valid arg for gender. Please use either male or female."
assert(len(sys.argv) > 2), "The second arg was not introduced. " + \
                           "You must pass a second valid arg to the script."
exp_version = sys.argv[2]
assert(exp_version in ['1', '2']), \
    "Not valid arg for number of inputs' vs. Please use either 1 or 2."

# %%
# ========================== INITIALIZATION ===================================
#
# (1) Present the startup screen with the countdown;
# (2) Start an experimental clock, create the screen;
# (3) Create an event file;
# (4) Present "Preparing experiment"
#
# =============================================================================
# Define global variable for the experiment
exp = design.Experiment('self_reference_' + gender_stim + '_' + exp_version,
                        foreground_colour=(255, 255, 255))

control.initialize(exp)

# %%
# ============================== MENU =========================================
# Preset the menu

setting_mm = load_config('config_self_main_menu.ini')

menu_options = [setting_mm["train_sess"], setting_mm["main_sess"],
                setting_mm["exit"]]

task_title = setting_mm["protocol_title"]

# Use the next command line if you're running Expyriment vs. O.7.0 on Windows
# menu_options = [s.decode('utf-8').encode('cp1252') for s in menu_options]
# task_title = task_title.decode('utf-8').encode('cp1252')
# Use the next two command lines for the customized vs of Expyriment vs. O.7.0
# in Win laptop of the IBC acquisitions
menu_options = [s.decode('utf-8') for s in menu_options]
task_title = task_title.decode('utf-8')

display_note = stimuli.TextLine(setting_mm["note"].decode('utf-8'),
                                text_size=24, text_colour=(0, 160, 230),
                                position=(0, -300))

menu = io.TextMenu(task_title, menu_options, width=1000, text_size=28, gap=10,
                   background_stimulus=display_note)

# Launch the menu (default_preselected_item = 'Expérience principale')
selected_option = menu.get(1)

# Call the functions according to the options selected in the menu
while True:
    # Launch option: "Session d'entraînement"
    if selected_option == 0:
        launch_protocol("config_self_training_session.ini", exp,
                        gender_stim, exp_version)
    # Launch option: "Expérience principale"
    elif selected_option == 1:
        launch_protocol("config_self_main_session.ini", exp,
                        gender_stim, exp_version)
    # Launch option: "Sortie"
    else:
        break
    # Goes back to the main menu after quitting any option
    # (except for the last one)
    if selected_option < (len(menu_options) - 1):
        exp = design.Experiment('self_reference',
                                foreground_colour=(255, 255, 255))
        control.initialize(exp)
        menu_options = [setting_mm["train_sess"], setting_mm["main_sess"],
                        setting_mm["exit"]]

        task_title = setting_mm["protocol_title"]

        menu_options = [s.decode('utf-8') for s in menu_options]
        task_title = task_title.decode('utf-8')

        menu = io.TextMenu(task_title, menu_options, width=1000,
                           text_size=28, gap=10,
                           background_stimulus=display_note)
        selected_option = menu.get(1)

control.end(fast_quit=1)
