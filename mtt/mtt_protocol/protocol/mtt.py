# -*- coding: utf-8 -*-
# =============================================================================
# Protocol on Mental Time Travel for the IBC project
#
# Authors: Ana Luísa Pinho, Baptiste Gauthier
#
# email: ana.pinho@inria.fr
# =============================================================================

import sys
from instdisplay import launch_instructions
from protocol_mtt import protocol
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
# ========== SET COMMAND-LINE ARGUMENTS TO BE PASSED TO THE SCRIPT ============
assert(len(sys.argv) > 1), "No arg was introduced. " + \
                           "You must pass a valid arg to the script."
coord = sys.argv[1]
assert(coord in ['we', 'sn']), \
    "Not valid arg for type of island. Please use either we or sn."

# %%
# ========================== INITIALIZATION ===================================
#
# (1) Present the startup screen with the countdown;
# (2) Start an experimental clock, create the screen;
# (3) Create an event file;
# (4) Present "Preparing experiment"
#
# =============================================================================
exp = design.Experiment('mental_time_travel', foreground_colour=(0, 0, 0),
                        background_colour=(127, 127, 127))

control.initialize(exp)

# %%
# ============================== MENU =========================================
# Preset the menu

setting_mm = load_config('config_mtt_main_menu.ini')

menu_options = [setting_mm["instruct"], setting_mm["train_sess"],
                setting_mm["main_sess"], setting_mm["exit"]]

task_title = setting_mm["protocol_title"]

# Use the next command line if you're running Expyriment vs. O.7.0 on Windows
# menu_options = [s.decode('utf-8').encode('cp1252') for s in menu_options]
# task_title = task_title.decode('utf-8').encode('cp1252')
# Use the next two command lines for the customized vs of Expyriment vs. O.7.0
# in Win laptop of the IBC acquisitions
menu_options = [s.decode('utf-8') for s in menu_options]
task_title = task_title.decode('utf-8')

display_note = stimuli.TextLine(setting_mm["note"].decode('utf-8'),
                                text_size=24, text_colour=(0, 0, 150),
                                position=(0, -300))

menu = io.TextMenu(task_title, menu_options, width=1000, text_size=28, gap=10,
                   background_colour=(127, 127, 127),
                   background_stimulus=display_note)

# Launch the menu (default_preselected_item = 'Expérience principale')
selected_option = menu.get(2)

# Call the functions according to the options selected in the menu
while True:
    # Launch option: "Instructions"
    if selected_option == 0:
        launch_instructions("config_mtt_instructions.ini", exp)
    # Launch option: "Session d'entraînement"
    elif selected_option == 1:
        protocol("config_mtt_training_session.ini", exp, coord)
    # Launch option: "Expérience principale"
    elif selected_option == 2:
        protocol("config_mtt_main_session.ini", exp, coord)
    # Launch option: "Sortie"
    else:
        break
    print selected_option
    # Goes back to the main menu after quitting any option
    # (except for the last one)
    if selected_option < (len(menu_options) - 1):
        exp = design.Experiment('mental_time_travel',
                                foreground_colour=(0, 0, 0),
                                background_colour=(127, 127, 127))
        control.initialize(exp)
        menu_options = [setting_mm["instruct"], setting_mm["train_sess"],
                        setting_mm["main_sess"], setting_mm["exit"]]

        task_title = setting_mm["protocol_title"]

        menu_options = [s.decode('utf-8') for s in menu_options]
        task_title = task_title.decode('utf-8')

        menu = io.TextMenu(task_title, menu_options, width=1000, text_size=28,
                           gap=10, background_colour=(127, 127, 127),
                           background_stimulus=display_note)
        selected_option = menu.get(2)

control.end(fast_quit=1)
