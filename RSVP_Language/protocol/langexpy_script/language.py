#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# Protocol on Language Processing for the IBC project
#
# Authors: Ana Luísa Pinho, Christophe Pallier
# Contributors: Elvis Dohmatob, Mehdi Rahim
#
# email: ana.pinho@inria.fr
# =============================================================================

from instdisplay import launch_instructions
from protocol import launch_protocol
from confparser import load_config

from expyriment import design, control, stimuli, io

# %%
# ======================== SET DEVELOPMENT MODE ===============================
control.set_develop_mode(False)

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
exp = design.Experiment('language_processing', foreground_colour=(0, 0, 0),
                        background_colour=(127, 127, 127))
control.initialize(exp)

# %%
# ============================== MENU =========================================
# Preset the menu

setting_mm = load_config('config_language_main_menu.ini')

menu_options = [setting_mm["instruct"], setting_mm["demo_sess"],
                setting_mm["train_sess"], setting_mm["main_sess"],
                setting_mm["exit"]]

task_title = setting_mm["protocol_title"]

# Use the next command line if you're running Expyriment vs. O.7.0 on Windows
# menu_options = [s.decode('utf-8').encode('cp1252') for s in menu_options]
# task_title = task_title.decode('utf-8').encode('cp1252')

display_note = stimuli.TextLine(setting_mm["note"].decode('utf-8'),
                                text_size=24, text_colour=(0, 0, 150),
                                position=(0, -300))

menu = io.TextMenu(task_title, menu_options,
                   width=1000, text_size=28, gap=10,
                   background_colour=(127, 127, 127),
                   background_stimulus=display_note)

# Launch the menu (default_preselected_item = 'Expérience principale')
selected_option = menu.get(3)

# Call the functions according to the options selected in the menu
while True:
    # Launch option: "Instructions"
    if selected_option == 0:
        launch_instructions("config_language_instructions.ini", exp)
    # Launch option: "Session de démontration"
    elif selected_option == 1:
        launch_protocol("config_language_demo.ini", exp)
    # Launch option: "Session d'entraînement"
    elif selected_option == 2:
        launch_protocol("config_language_training_session.ini", exp)
    # Launch option: "Expérience principale"
    elif selected_option == 3:
        launch_protocol("config_language_main_session.ini", exp)
    # Launch option: "Sortie"
    else:
        break
    # Goes back to the main menu after quitting any option
    # (except for the last one)
    if selected_option < (len(menu_options) - 1):
        exp = design.Experiment('language_processing',
                                foreground_colour=(0, 0, 0),
                                background_colour=(127, 127, 127))
        control.initialize(exp)
        menu_options = [setting_mm["instruct"], setting_mm["demo_sess"],
                        setting_mm["train_sess"], setting_mm["main_sess"],
                        setting_mm["exit"]]

        menu = io.TextMenu(setting_mm["protocol_title"], menu_options,
                           width=1000, text_size=28, gap=10,
                           background_colour=(127, 127, 127),
                           background_stimulus=display_note)
        selected_option = menu.get(3)

control.end(fast_quit=1)
