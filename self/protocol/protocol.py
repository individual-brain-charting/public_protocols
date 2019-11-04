# -*- coding: utf-8 -*-

import os
import csv
import numpy as np

import dirfiles
from confparser import load_config

import expyriment
from expyriment import design, control, stimuli, io, misc


def launch_protocol(protocol_ini, exp, gender, vs):
    # %%
    # ======================== LOAD CONFIG.INI FILE ===========================

    # Select .ini file for instructions
    setting = load_config(protocol_ini)

    # %%
    # ========================== LOAD INPUT FILES =============================

    # Define the pathway of the inputs directory
    inputs_path = os.path.abspath(setting["inputs_dir"] + gender +
                                  '/version_' + vs)
    print inputs_path
    # List input csv files
    inputs_filenames = dirfiles.listdir_csvnohidden(inputs_path)
    inputs_filenames.sort()

    # %%
    # ======== WAITS FOR USER TO ENTER BLOCK (AKA RUN) NUMBER TO START ========

    # Define number of runs
    nb_block = len(inputs_filenames)

    # Wait 5 seconds in order to launch input text screen
    exp.keyboard.wait(duration=5000)

    # Create text input box
    ti = io.TextInput(message='Block number:', message_text_size=24,
                      message_colour=map(int, setting["bcolor"]),
                      user_text_colour=map(int, setting["ucolor"]),
                      ascii_filter=misc.constants.K_ALL_DIGITS,
                      frame_colour=(70, 70, 70))

    # Load user's input
    while True:
        sb = ti.get('0')
        # If string is empty
        if not sb:
            warning_message1 = stimuli.TextLine(setting["wm1"].decode('utf-8'),
                                                text_size=24,
                                                text_colour=(204, 0, 0))
            warning_message1.present()
            exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
            continue
        # If block number introduced is higher than the number of blocks
        # preset in config file
        elif int(sb) >= nb_block:
            warning_message2 = stimuli.TextLine(setting["wm2"].decode('utf-8'),
                                                text_size=24,
                                                text_colour=(204, 0, 0))
            warning_message2.present()
            exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
            continue
        else:
            start_block = int(sb)
            break

    # %%
    # ============================== DESIGN ===================================

    # Stimuli sequence of the protocol
    session_list = [[i for i in csv.reader(open(inputs_filename))]
                   for inputs_filename in inputs_filenames]

    # Define the blocks using expyriment module
    block_list = [expyriment.design.Block(name="block%d" % bs)
                  for bs in np.arange(nb_block)]

    # For all blocks in the block list...
    for bl in np.arange(nb_block):
        # ...add stimuli to the trials and add trials to the blocks
        for l,line in enumerate(session_list[bl]):
            # Create a trial
            trial = design.Trial()
            # Retrieve variables from input files at every trial and
            # label them according to what is defined by var_names
            for tsf in np.arange(len(setting["var_names"]) - 1):
                trial.set_factor(setting["var_names"][tsf],
                                 line[tsf].decode('utf-8'))
            trial.set_factor(setting["var_names"][-1],
                             line[-2].decode('utf-8'))
            # Create stimuli...
            if line[1] == '0':
                # ... (1) for Rest trial,
                # (i.e. between encoding and recognition), ...
                if line[0] == '+':
                    fixcross_isi = stimuli.FixCross(size=(30, 30),
                                                    line_width=3,
                                                    colour=(255, 255, 255))
                    # Add fixation cross to the trial
                    trial.add_stimulus(fixcross_isi)
                # (2) for Instructions trial, ...
                else:
                    instruction = stimuli.TextLine(line[4].decode('utf-8'),
                                                   position=(0, 250),
                                                   text_size=56,
                                                   text_colour=(255, 153, 51))
                    question = stimuli.TextLine(line[0].decode('utf-8'),
                                                position=(0, 0),
                                                text_size=58,)
                    question_reminder = stimuli.TextLine(
                        line[0].decode('utf-8'), position=(0, 250),
                        text_size=56, text_colour=(255, 153, 51))
                    # Add instructions to the trial
                    trial.add_stimulus(instruction)
                    trial.add_stimulus(question)
            # ... and (3) for active trial.
            else:
                # Add adjectives to the trial
                adjective = stimuli.TextLine(line[0].decode('utf-8'),
                                             text_size=58,
                                             position=(0, 0))
                yes_answer = stimuli.TextLine(setting["yes_key_indication"],
                                              position=(-350, -250),
                                              text_size=60)
                no_answer = stimuli.TextLine(setting["no_key_indication"],
                                             position=(300, -250),
                                             text_size=60)
                trial.add_stimulus(question_reminder)
                trial.add_stimulus(adjective)
                trial.add_stimulus(yes_answer)
                trial.add_stimulus(no_answer)
            # Add trial to run
            block_list[bl].add_trial(trial)

    # Add block to the experiment
    for ad in np.arange(nb_block):
        exp.add_block(block_list[ad])

    # Print exp. variable names in the log file
    exp.data_variable_names = setting["llog_var_names"]

    # # %%
    # # ================ DEFINE AND PRELOAD SOME STIMULI ======================

    # TTL cross
    fixcross_ttl = stimuli.FixCross(size=(40, 40), line_width=3,
                                    colour=(255, 255, 0))
    fixcross_ttl.preload()

    # # Message at the end of each session
    blockend_message = stimuli.TextLine(setting["text_end_session"],
                                        text_size=44,
                                        text_colour=(255, 153, 51))
    blockend_message.preload()

    # # Final message before quitting the experiment
    text_end = stimuli.TextBox(str(''.join((setting["text_end_exp_one"],
                                            '\n\n',
                               setting["text_end_exp_two"]))).decode('utf-8'),
                               (1000, 1000), position=(0, -400),
                               text_size=44, text_colour=(255, 153, 51))
    text_end.preload()

    # # %%
    # # ================================ RUN ==================================
    # # =======================================================================
    # # Starts running the experiment:
    # # (1) Present a screen asking for the subject no. (exp.subject) and
    # #     wait for the RETURN key
    # # (2) Create a data file (exp.data)
    # # (3) Present the "Ready" screen
    # # =======================================================================
    control.start(exp, skip_ready_screen=True)

    # # =======================================================================
    # # Run the protocol
    # # =======================================================================
    stop = False
    found_key = 0
    key_totalexp = []
    # While "h" key is not pressed, ...
    while not stop:
        # Loop over all runs
        for b, block in enumerate(exp.blocks[start_block:]):
            block_no = b + start_block
            t_jit = 0
            # Display fixation cross that sets the beginning of the experiment
            fixcross_ttl.present()
            # Wait for TTL
            exp.keyboard.wait_char(setting["TTL"])
            exp.screen.clear()
            exp.screen.update()
            # Creates the clock
            t0 = misc.Clock()
            # Wait INITIALWAIT seconds before the beginning of the trial
            fixcross_isi.present()
            exp.clock.wait(setting["INITIALWAIT"])
            # Loop over all trials within a block
            for t, trial in enumerate(block.trials):
                # Getter for the time in milliseconds since clock init.
                # Time for the beginning of the trial
                t_start = t0.time
                # Present stimulus
                for s, stimulus in enumerate(trial.stimuli):
                    if len(trial.stimuli) > 1:
                        if s == 0:
                            stimulus.present(update=False)
                        elif s == len(trial.stimuli) - 1:
                            stimulus.present(clear=False)
                        else:
                            stimulus.present(clear=False, update=False)
                    else:
                        stimulus.present()
                # Jittered duration during rest,
                # i.e. between encoding and recognition
                if len(trial.stimuli) == 1:
                    jit_rest = design.randomize.rand_int(10000, 14000)
                    found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                     duration=jit_rest)
                    # If "h" key is pressed, returns to main menu
                    if found_key == misc.constants.K_h:
                        stop = True
                        break
                    diff_mean_rest = 1000 - jit_rest
                    t_jit = t_jit + diff_mean_rest
                    # Calculate total duration of the rest period
                    duration_rest = t0.time - t_start
                    # Log file registry for rest
                    exp.data.add([block_no, t,
                                  trial.get_factor(setting["var_names"][0]),
                                  trial.get_factor(setting["var_names"][2]),
                                  t_start, duration_rest])
                else:
                    # Duration of active trials
                    if len(trial.stimuli) == 4:
                        key, rt = exp.keyboard.wait_char([setting["YES"],
                                                          setting["NO"]],
                                                         duration=5000)
                        t_end = t0.time
                        t_diff = t_end - t_start
                        if t_diff < 5000:
                            exp.clock.wait(5000-t_diff)
                        # Calculate total duration of the active condition
                        duration_active = t0.time - t_start
                        # Log file registry for the active condition
                        exp.data.add([block_no, t,
                                      trial.get_factor(setting["var_names"][0]),
                                      trial.get_factor(setting["var_names"][1]),
                                      trial.get_factor(setting["var_names"][2]),
                                      trial.get_factor(setting["var_names"][3]),
                                      trial.get_factor(setting["var_names"][4]),
                                      t_start, duration_active, key, rt])
                    # Duration of instruction trial
                    else:
                        found_key, _ = exp.keyboard.wait(
                            keys=[misc.constants.K_h], duration=5000)
                        # If "h" key is pressed, returns to main menu
                        if found_key == misc.constants.K_h:
                            stop = True
                            break
                        # Calculate total duration of the instruction
                        duration_inst = t0.time - t_start
                        # Log file registry for the instruction trials
                        exp.data.add([block_no, t,
                                      trial.get_factor(setting["var_names"][0]),
                                      trial.get_factor(setting["var_names"][2]),
                                      t_start, duration_inst])
                    # Jittered ISI fixation cross
                    fixcross_isi.present()
                    jit_isi = design.randomize.rand_int(300, 700)
                    found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                     duration=jit_isi)
                    # If "h" key is pressed, returns to main menu
                    if found_key == misc.constants.K_h:
                        stop = True
                        break
                    diff_mean_isi = 500 - jit_isi
                    t_jit = t_jit + diff_mean_isi
            if stop:
                break
            # Display fixation cross in the end of the session
            fixcross_isi.present()
            found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                             duration=15000 + t_jit)
            # If "h" key is pressed, returns to main menu
            if found_key == misc.constants.K_h:
                stop = True
                break
            # In the end of each session:
            if block_no < (nb_block - 1):
                fixcross_isi.present()
                # Display message: "End of Session"
                blockend_message.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_RETURN,
                                                       misc.constants.K_h])
                if found_key == misc.constants.K_h:
                    stop = True
                    break
            # In the end of the experiment:
            elif block_no == (nb_block - 1):
                fixcross_isi.present()
                # Display message: "End of the Experiment"
                text_end.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_RETURN,
                                                       misc.constants.K_h],
                                                 duration=5000)
                # Leave while loop
                stop = True
