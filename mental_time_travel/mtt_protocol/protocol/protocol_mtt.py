# -*- coding: utf-8 -*-

import os
import csv
import numpy as np

import dirfiles
from confparser import load_config
from score import calc_score

import expyriment
from expyriment import design, control, stimuli, io, misc


def protocol(protocol_ini, exp, island):
    # %%
    # ======================== LOAD CONFIG.INI FILE ===========================
    # Select .ini file for instructions
    setting = load_config(protocol_ini)

    # %%
    # ========================== LOAD INPUT FILES =============================

    # Define the pathway of the inputs directory
    inputs_path = os.path.abspath(setting["inputs_dir"] + island)

    # List input csv files
    inputs_filenames = dirfiles.listdir_csvnohidden(inputs_path)
    inputs_filenames.sort()

    # %%
    # ============= WAITS FOR USER TO ENTER RUN NUMBER TO START ===============

    # Define number of runs
    nb_block = len(inputs_filenames)

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
            warning_message1 = stimuli.TextLine(setting["wm1"].decode('utf-8'),
                                                text_size=24,
                                                text_colour=(204, 0, 0))
            warning_message1.present()
            exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
            continue
        # If run (aka block) number introduced is higher than the number of
        # runs preset in config file
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

    # Define the pathway of the audio files
    refsn_path = os.path.abspath(setting["ref_sn"])
    refwe_path = os.path.abspath(setting["ref_we"])
    cue_path = os.path.abspath(setting["cue"])
    eventsn_path = os.path.abspath(setting["event_sn"])
    eventwe_path = os.path.abspath(setting["event_we"])

    # Stimuli sequence of the protocol
    session_list = [[i for i in csv.reader(open(inputs_filename))]
                    for inputs_filename in inputs_filenames]

    # Define the runs (aka blocks) using expyriment module
    block_list = [expyriment.design.Block(name="block%d" % bs)
                  for bs in np.arange(nb_block)]

    # For all runs (aka blocks) in the run list...
    for bl in np.arange(nb_block):
        # ...add stimuli to the trials and add trials to the blocks
        for line in session_list[bl][1:]:
            # Create a trial
            trial = design.Trial()
            # Retrieve variables from input files at every trial and
            # label them according to what is defined by var_names in the
            # corresponding .ini file
            for tsf in np.arange(len(setting["var_names"])):
                trial.set_factor(setting["var_names"][tsf], line[tsf])
            # Create reference stimulus
            if line[1] == 'we':
                ref = stimuli.Audio(refwe_path + '/' + line[4] + '.' +
                                    setting["ext"])
            elif line[1] == 'sn':
                ref = stimuli.Audio(refsn_path + '/' + line[4] + '.' +
                                    setting["ext"])
            # Add reference stimulus to the trial
            trial.add_stimulus(ref)
            # Create cue stimulus
            cue = stimuli.Audio(cue_path + '/' + line[5] + '.' +
                                setting["ext"])
            # Add cue stimulus to the trial
            trial.add_stimulus(cue)
            # Create event stimulus...
            for e in line[7::2]:
                if line[1] == 'we':
                    event_audio = stimuli.Audio(eventwe_path + '/' + e +
                                                '.' + setting["ext"])
                elif line[1] == 'sn':
                    event_audio = stimuli.Audio(eventsn_path + '/' + e +
                                                '.' + setting["ext"])
                # ...and add it to the trial
                trial.add_stimulus(event_audio)
            # Set factor for participant's reply
            trial.set_factor("feedback", "response")
            # Add trial to run (aka block)
            block_list[bl].add_trial(trial)
    # Add run (aka block) to the experiment
    for ad in np.arange(nb_block):
        exp.add_block(block_list[ad])

    # Print exp. variable names in the log file
    exp.data_variable_names = setting["llog_var_names"]

    # %%
    # ==================== DEFINE AND PRELOAD SOME STIMULI ====================
    # TTL cross
    fixcross1 = stimuli.FixCross(size=(30, 30), line_width=3,
                                 colour=(255, 255, 0))
    fixcross1.preload()

    # Trial cross
    fixcross2 = stimuli.FixCross(size=(30, 30), line_width=3,
                                 colour=map(int, setting["wcolor"]))
    fixcross2.preload()

    # Before-reference cross
    fixcross3 = stimuli.FixCross(size=(30, 30), line_width=3,
                                 colour=map(int, setting["brefcross_color"]))
    fixcross3.preload()

    # Text for end of session
    text_end_run = stimuli.TextLine(setting["text_end_run"], text_size=44,
                                    text_colour=(255, 153, 51))
    text_end_run.preload()

    # Text for end of experiment
    text_end = stimuli.TextBox(str(''.join((setting["text_end_exp_one"],
                                            '\n\n',
                               setting["text_end_exp_two"]))).decode('utf-8'),
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
    control.start(skip_ready_screen=True)
    # Start audio system
    control.start_audiosystem()

    # =========================================================================
    # Run the protocol
    # =========================================================================
    stop = False
    found_key = 0
    # While "h" key is not pressed, ...
    while not stop:
        # Arrays to compute the final scores
        answers_final = []
        feedback_final = []
        # ... and for each run
        for b, block in enumerate(exp.blocks[start_block:]):
            # Arrays to compute the score at the end of each run
            correct_answers_run = []
            answers_run = []
            feedback_run = []
            # Start at any run number
            block_no = b + start_block
            # Display fixation cross that sets the beginning of the experiment
            fixcross1.present()
            # Wait for TTL
            exp.keyboard.wait_char(setting["TTL"])
            exp.screen.clear()
            exp.screen.update()
            # Creates the clock
            t0 = misc.Clock()
            # Display fixation cross
            fixcross2.present()
            # Wait INITIALWAIT seconds before the beginning of the trial
            exp.clock.wait(setting["INITIALWAIT"])
            # Loop over all trials within a run (aka block)
            for t, trial in enumerate(block.trials):
                # ##################### REFERENCE #############################
                # Getter for the time in milliseconds since clock init.
                # Time for the beginning of the trial
                t_start = t0.time
                # Display reference
                trial.stimuli[0].present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=2000)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # Calculate duration of reference condition
                ref_duration = t0.time - t_start
                # Log file registry of reference for the current trial
                exp.data.add([block_no, t,
                              trial.get_factor(setting["var_names"][0]),
                              trial.get_factor(setting["var_names"][1]),
                              trial.get_factor(setting["var_names"][2]),
                              trial.get_factor(setting["var_names"][3]),
                              trial.get_factor(setting["var_names"][6]),
                              trial.get_factor(setting["var_names"][4]),
                              t_start, ref_duration])
                # ################### BLANK PERIOD I ##########################
                # Display fixation cross
                fixcross2.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=4000)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # ######################## CUE ################################
                # Display cue
                t_startcue = t0.time
                trial.stimuli[1].present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=2000)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # Calculate duration of the cue
                cue_duration = t0.time - t_startcue
                # Log file registry of cue for the current trial
                exp.data.add([block_no, t,
                              trial.get_factor(setting["var_names"][0]),
                              trial.get_factor(setting["var_names"][1]),
                              trial.get_factor(setting["var_names"][2]),
                              trial.get_factor(setting["var_names"][3]),
                              trial.get_factor(setting["var_names"][6]),
                              trial.get_factor(setting["var_names"][5]),
                              t_startcue, cue_duration])
                # ################### BLANK PERIOD II #########################
                # Display fixation cross
                fixcross2.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=4000)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # ####################### EVENTS ##############################
                for ev, event in enumerate(trial.stimuli[2:]):
                    # Display event
                    t_startevent = t0.time
                    event.present()
                    early_key, early_rt = exp.keyboard.wait_char([
                        setting["LEFT_BUTTON"], setting["RIGHT_BUTTON"]],
                        duration=2000)
                    # Add extra-time to the cue period if there's an early_rt,
                    # in order to assure constant SOA
                    if 0 <= early_rt <= 2000:
                        found_key, _ = exp.keyboard.wait(
                            keys=[misc.constants.K_h], duration=(2000 -
                                                                 early_rt))
                    # Calculate duration of the event
                    event_duration = t0.time - t_startevent

                    # Log file registry of each event for the current trial
                    exp.data.add([block_no, t,
                                 trial.get_factor(setting["var_names"][0]),
                                 trial.get_factor(setting["var_names"][1]),
                                 trial.get_factor(setting["var_names"][2]),
                                 trial.get_factor(setting["var_names"][3]),
                                 trial.get_factor(setting["var_names"][6]),
                                 trial.get_factor(
                                     setting["var_names"][2 * ev + 7]),
                                 t_startevent, event_duration, early_rt,
                                 early_key])
                    # ################# Feedback ##############################
                    t_startfeedback = t0.time
                    fixcross2.present()
                    late_key, late_rt = exp.keyboard.wait_char([
                        setting["LEFT_BUTTON"], setting["RIGHT_BUTTON"]],
                        duration=3000)
                    # Add extra-time to the response period if < 3s
                    # in order to assure constant SOA
                    if 0 <= late_rt <= 3000:
                        found_key, _ = exp.keyboard.wait(
                            keys=[misc.constants.K_h], duration=(3000 -
                                                                 late_rt))
                    # Calculate duration of the event
                    feedback_duration = t0.time - t_startfeedback
                    # Log file registry of feedback for each event
                    exp.data.add([block_no, t,
                                  trial.get_factor(setting["var_names"][0]),
                                  trial.get_factor(setting["var_names"][1]),
                                  trial.get_factor(setting["var_names"][2]),
                                  trial.get_factor(setting["var_names"][3]),
                                  trial.get_factor(setting["var_names"][6]),
                                  trial.get_factor("feedback"),
                                  t_startfeedback, feedback_duration, late_rt,
                                  late_key,
                                  trial.get_factor(
                                      setting["var_names"][2 * ev + 8])])
                    correct_answers_run.append(trial.get_factor(
                                             setting["var_names"][2 * ev + 8]))
                    if late_key is None:
                        lkey = 'None'
                    else:
                        lkey = late_key
                    feedback_run.append(str(lkey))
                # ######## BLANK PERIOD III - INTER-TRIAL INTERVAL ############
                # Display fixation cross
                fixcross2.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=6500)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
                # ######## BLANK PERIOD IV - SIGNALING NEXT TRIAL #############
                # Display before-reference cross, ...
                if t < (len(block.trials) - 1):
                    fixcross3.present()
                #..., unless this is the last trial. 
                # If true, display trial cross, instead.
                else:
                    fixcross2.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=400)
                # Display trial cross
                fixcross2.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                                 duration=100)
                # If "h" key is pressed, returns to main menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
            # ############## BLANK PERIOD V - INTER-RUN INTERVAL ##############
            # Display fixation cross
            fixcross2.present()
            found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_h],
                                             duration=8000)
            # If "h" key is pressed, returns to main menu
            if found_key == misc.constants.K_h:
                stop = True
                break
            # ####################### End of run ##############################
            # Calculate the score for current run
            answers_run = [setting["LEFT_BUTTON"] if answ in ['before', 'west',
                                                              'south']
                           else setting["RIGHT_BUTTON"]
                           for answ in correct_answers_run]
            sc_run = calc_score(answers_run, feedback_run)
            # Display the message with the score
            sc_msg_run = ''.join((setting["text_sc_run"], sc_run, "%."))
            sc_fdbk_run = stimuli.TextLine(sc_msg_run.decode('utf-8'),
                                           text_size=44,
                                           text_colour=(0, 0, 100))
            sc_fdbk_run.present()
            exp.clock.wait(5000)
            # Append results of current run for final score
            answers_final.append(answers_run)
            feedback_final.append(feedback_run)
            # ######################## Next run ###############################
            if block_no < (nb_block - 1):
                # Wait for "ENTER" or "h" key, while displaying the message,
                # "ENTER" --> go to the next session
                text_end_run.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_RETURN,
                                                       misc.constants.K_h])
                # "h" key --> return to the Main Menu
                if found_key == misc.constants.K_h:
                    stop = True
                    break
            # ##################### End of session ############################
            else:
                # Calculate the final score
                answers_final = np.concatenate(answers_final)
                feedback_final = np.concatenate(feedback_final)
                sc_final = calc_score(answers_final, feedback_final)
                # Display the message with the final score
                sc_msg_final = ''.join((setting["text_sc_final"],
                                        sc_final, "%."))
                sc_fdbk_final = stimuli.TextLine(sc_msg_final.decode('utf-8'),
                                                 text_size=44,
                                                 text_colour=(0, 0, 100))
                sc_fdbk_final.present()
                exp.clock.wait(5000)
                # Wait for "ENTER" or "h" key, while displaying the message,
                # in order to quit the protocol and return to the Main Menu
                text_end.present()
                found_key, _ = exp.keyboard.wait(keys=[misc.constants.K_RETURN,
                                                       misc.constants.K_h],
                                                 duration=5000)
                # Leave while loop
                stop = True
