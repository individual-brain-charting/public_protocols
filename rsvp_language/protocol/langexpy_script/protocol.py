# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

import dirfiles
from confparser import load_config
from score import calc_score
# from order import trial_order

import expyriment
from expyriment import design, control, stimuli, io, misc


def launch_protocol(protocol_ini, exp):
    # %%
    # ======================== LOAD CONFIG.INI FILE ===========================

    # Select .ini file for instructions
    setting = load_config(protocol_ini)

    # %%
    # ========================== LOAD INPUT FILES =============================

    # Define the pathway of the inputs directory
    inputs_path = os.path.abspath(setting["inputs_dir"])
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
                      background_colour=(0, 0, 0),
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

    # Generate a list of dataframes containing the inputs per block
    df_list = [pd.read_csv(inputs_filename)
               for inputs_filename in inputs_filenames]

    # Convert the list of dataframes in a list of lists
    session_list = [df_list[sl].values.tolist()
                    for sl in np.arange(nb_block)]

    # List of lists containing type of probe for every session
    probe_list_sess = [df_list[pls]['probe_type'].values.tolist()
                       for pls in np.arange(nb_block)]

    # Unique list containing type of probe for the trials within the blocks
    # selected by the user. To be used for score's calculation.
    probe_list = []
    for j in np.arange(start_block, nb_block):
        probe_list.extend(df_list[j]['probe_type'].values.tolist())

    # Define the blocks using expyriment module
    block_list = [expyriment.design.Block(name="block%d" % bs)
                  for bs in np.arange(nb_block)]

    # Path of font type file
    font_path = os.path.abspath(setting["font_file"])

    # For all blocks in the block list...
    MaxWidth, MaxHeight = 0, 0
    for bl in np.arange(nb_block):
        # ...add stimuli to the trials and add trials to the blocks
        for line in session_list[bl]:
            # Create a trial
            trial = design.Trial()
            # Define variables within the trial
            for tsf in np.arange(len(setting["var_names"])):
                trial.set_factor(setting["var_names"][tsf], line[tsf])
            # Generate sentence stimulus and add it to the trial
            # Bitmaps of the words displayed
            for w in line[setting["sentence_ini"]:setting["sentence_ini"] +
                          setting["sentence_len"]]:
                sentence = stimuli.TextLine(w.decode('utf-8'),
                                            text_font=font_path,
                                            text_size=setting["txtsize"],
                                            text_colour=map(int,
                                                            setting["wcolor"]))
                # Length of the frame lines
                x, y = sentence.surface_size
                if x > MaxWidth:
                    MaxWidth = x
                elif y > MaxHeight:
                    MaxHeight = y
                # Add bitmap of sentence to the trial
                trial.add_stimulus(sentence)
            # Define type of probe
            trial.set_factor("probe", line[setting["probe_type"]])
            # Create bitmap of the probe displayed and add it to the trial
            probe = stimuli.TextLine(line[setting[
                "probe_word"]].decode('utf-8'), text_font=font_path,
                text_size=setting["txtsize"],
                text_colour=map(int, setting["wcolor"]))
            # Add bitmap of probe to the trial
            trial.add_stimulus(probe)
            # Set factor for participant's reply
            trial.set_factor("feedback", "feedback")
            # Add trial to block
            block_list[bl].add_trial(trial)

    # =========================================================================
    #  Reorder trials within each block according to a pre-specified sequence
    #  (uncomment three next lines and preamble, too)
    # =========================================================================
    #  trials_seq = trial_order(setting["order_dir"])
    #  for nbb in np.arange(nb_block):
    #  	  block_list[nbb].order_trials(trials_seq[nbb])

    # Add block to the experiment
    for ad in np.arange(nb_block):
        exp.add_block(block_list[ad])

    # Print exp. variable names in the log file
    exp.data_variable_names = setting["llog_var_names"]

    # %%
    # ================ DEFINE AND PRELOAD SOME STIMULI ========================

    # TTL cross
    fixcross1 = stimuli.FixCross(size=(30, 30),
                                 line_width=3, colour=(255, 255, 0))
    fixcross1.preload()

    # Trial cross
    fixcross2 = stimuli.FixCross(size=(30, 30), line_width=3,
                                 colour=map(int, setting["wcolor"]))
    fixcross2.preload()

    # Blank screen before sentence display
    blank1 = stimuli.BlankScreen(colour=None)
    blank1.preload()

    # Frame lines during text display
    MaxWidth = MaxWidth + setting["txtsurface_broadness"]
    MaxHeight = MaxHeight + setting["txtsurface_broadness"]
    line1 = stimuli.Line((- MaxWidth / 2, MaxHeight / 2),
                         (MaxWidth / 2, MaxHeight / 2), 2,
                         map(int, setting["wcolor"]))
    line1.preload()
    line2 = stimuli.Line((- MaxWidth / 2, - MaxHeight / 2),
                         (MaxWidth / 2, - MaxHeight / 2), 2,
                         map(int, setting["wcolor"]))
    line2.preload()

    # Jittered blank screen before probe
    blank2 = stimuli.BlankScreen(colour=None)
    blank2.preload()

    # Blank screen - participant's feedback
    blank3 = stimuli.BlankScreen(colour=None)
    blank3.preload()

    # Message at the end of each session
    blockend_message = stimuli.TextLine(setting["text_end_session"],
                                        text_size=44,
                                        text_colour=(255, 153, 51))
    blockend_message.preload()

    # Final message before quitting the experiment
    text_end = stimuli.TextBox(str(''.join((setting["text_end_exp_one"],
                                            '\n\n',
                                            setting["text_end_exp_two"]))),
                               (1000, 1000), position=(0, -400),
                               text_size=44, text_colour=(255, 153, 51))
    text_end.preload()

    # %%
    # ================================ RUN ====================================
    # =========================================================================
    # Starts running the experiment:
    # (1) Present a screen asking for the subject no. (exp.subject) and
    #     wait for the RETURN key
    # (2) Create a data file (exp.data)
    # (3) Present the "Ready" screen
    # =========================================================================
    control.start(exp, skip_ready_screen=True)

    # =========================================================================
    # Run the protocol
    # =========================================================================
    stop = False
    found_key = 0
    key_totalexp = []
    # While "h" key is not pressed, ...
    while not stop:
        # Loop over all blocks
        for b, block in enumerate(exp.blocks[start_block:]):
            block_no = b + start_block
            key_session = []
            # Display fixation cross that sets the beginning of the experiment
            fixcross1.present()
            # Wait for TTL
            exp.keyboard.wait_char(setting["TTL"])
            exp.screen.clear()
            exp.screen.update()
            # Creates the clock
            t0 = misc.Clock()
            # Wait INITIALWAIT seconds before the beginning of the trial
            exp.clock.wait(setting["INITIALWAIT"])
            # Loop over all trials within a block
            for t, trial in enumerate(block.trials):
                # Getter for the time in milliseconds since clock init.
                # Time for the beginning of the trial
                t_start = t0.time
                # Display fixation cross that sets the beginning of the trial
                line1.present(clear=True, update=False)
                line2.present(clear=False, update=False)
                fixcross2.present(clear=False)
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=2000)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # First blank screen
                blank1.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=500)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # Presentation of the language stimuli within
                # the pre-specified frame lines
                onset_sentence = t0.time
                for word_stim in trial.stimuli[0:setting["sentence_len"]]:
                    # Display: Word-on
                    line1.present(clear=True, update=False)
                    line2.present(clear=False, update=False)
                    word_stim.present(clear=False)
                    found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                     duration=400)
                    # Display: Word-off
                    # line1.present(clear=True, update=False)
                    # line2.present(clear=False, update=True)
                    # found_key, _ = exp.keyboard.wait(
                    #                 keys=[misc.constants.K_h], duration=100)

                    # If "h" key is pressed, returns to main menu
                    if found_key == misc.constants.K_h:
                        stop = True
                        break
                if stop:
                    break
                # Log file registry of word display for the current trial
                duration_sentence = t0.time - onset_sentence
                log_reg_sentence = [trial.get_factor(setting["var_names"][tgf])
                                    for tgf in
                                    np.arange(len(setting["var_names"]))]
                log_reg_sentence.insert(0, block_no)
                log_reg_sentence.insert(1, t)
                log_reg_sentence.extend([onset_sentence, duration_sentence])
                exp.data.add(log_reg_sentence)
                # Second jittered blank screen
                blank2.present()
                found_key, _ = exp.keyboard.wait(
                    keys=[misc.constants.K_h],
                    duration=design.randomize.rand_int(1000, 1500))
                # Display fixation cross before probe
                line1.present(clear=True, update=False)
                line2.present(clear=False, update=False)
                fixcross2.present(clear=False)
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=500)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # Probe display
                onset_probe = t0.time
                line1.present(clear=True, update=False)
                line2.present(clear=False, update=False)
                trial.stimuli[setting["sentence_len"]].present(clear=False)
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=500)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # Log file registry of probe display for the current trial
                duration_probe = t0.time - onset_probe
                exp.data.add([block_no, t, trial.get_factor("probe"),
                              onset_probe, duration_probe])
                # Pt's feedback
                onset_reply = t0.time
                blank3.present()
                key, rt = exp.keyboard.wait_char([setting["YES"],
                                                  setting["NO"]],
                                                 duration=1000)
                # Log file registry of pt's feedback for the current trial
                exp.data.add([block_no, t, trial.get_factor("feedback"),
                              key, onset_reply, rt])
                # Add pt's response to the list in order to evaluate the score
                key_session.append(key)
                key_totalexp.append(key)
                # Add extra-time to the response period
                # in order to assure SOA = 10s
                t_end = t0.time
                t_diff = t_end - t_start
                if t_diff < setting["SOA"]:
                    found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                     duration=(setting["SOA"] -
                                                               t_diff))
            if stop:
                break
            # In the end of each session:
            if block_no < (nb_block - 1):
                # Calculate the score for current session
                sc_sess = calc_score(probe_list_sess[block_no], key_session,
                                     setting["YES"], setting["NO"])
                sc_msg_sess = ''.join((setting["text_sc_sess"], sc_sess, "%."))
                # Display the message with the score
                sc_fdbk_sess = stimuli.TextLine(sc_msg_sess.decode('utf-8'),
                                                text_size=44,
                                                text_colour=(0, 0, 100))
                sc_fdbk_sess.present()
                exp.clock.wait(5000)
                # Display message: "End of Session"
                blockend_message.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_RETURN,
                                                       misc.constants.K_h])
                if found_key == misc.constants.K_h:
                    stop = True
                    break
            # In the end of the experiment:
            elif block_no == (nb_block - 1):
                # Calculate the score for current session
                sc_sess = calc_score(probe_list_sess[block_no], key_session,
                                     setting["YES"], setting["NO"])
                sc_msg_sess = ''.join((setting["text_sc_sess"], sc_sess, "%."))
                # Display the message with the score
                sc_fdbk_sess = stimuli.TextLine(sc_msg_sess.decode('utf-8'),
                                                text_size=44,
                                                text_colour=(0, 0, 100))
                sc_fdbk_sess.present()
                exp.clock.wait(5000)
                # Calculate the final score
                sc_final = calc_score(probe_list, key_totalexp, setting["YES"],
                                      setting["NO"])
                sc_msg_final = ''.join((setting["text_sc"], sc_final, "%."))
                # Display the message with the score
                sc_fdbk_final = stimuli.TextLine(sc_msg_final.decode('utf-8'),
                                                 text_size=44,
                                                 text_colour=(0, 60, 0))
                sc_fdbk_final.present()
                exp.clock.wait(5000)
                # Display message: "End of the Experiment"
                text_end.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_RETURN,
                                                       misc.constants.K_h],
                                                 duration=5000)
                # Leave while loop
                stop = True
