# -*- coding: utf-8 -*-
"""
Script based on the experiment used by Santoro et al. (2017), for the fMRI
analysis of real-life sound perception
author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import os
import sys
import numpy as np

from expyriment import design, control, stimuli, misc, io
from ast import literal_eval as make_tuple

# %% PARAMETERS

# Dev mode

control.set_develop_mode(False)

# Colors

colors = {'black': (0, 0, 0), 'purple': (166, 166, 237),
          'yellow': (237, 237, 166), 'gray': (70, 70, 70),
          'red': (204, 0, 0), 'white': (255, 255, 255)}

# Participant and number of acquisition

try:

    acq_num = sys.argv[1]

except IndexError as err:

    raise IndexError("Acquisition number not provided. Please input 1 for first session or 2 for the second.") from err

# Sets used for each acquisition: first list of each key indicates the sets
# and second list indicates the prerand number

set_pairs = {1: [[1, 2, 3, 4, 1, 2], [1, 1, 1, 1, 2, 2]],
             2: [[1, 2, 3, 4, 3, 4], [3, 3, 2, 2, 3, 3]]}

# %% PATHS

my_path = os.getcwd()

stim_path = os.path.join(my_path, '../stim')

filenames_path = os.path.join(stim_path, 'prerandomizations')

# Create the paths to open the csv files

path_lambda = lambda x, y: os.path.join(filenames_path,
                                        'set' + str(x) + '_prerand' + str(y))

try:

    set_maps = map(path_lambda,
                   set_pairs[int(acq_num)][0],
                   set_pairs[int(acq_num)][1])

except KeyError as e:

    raise Exception("The acquisition number does not match the existing sessions. Please input 1 or 2.") from e

else:

    all_set_list = list(set_maps)

# Open the files

runs_list = [open(all_set_list[filename])
             for filename in range(len(all_set_list))]

# Inter-stimulus intervals

# In case you are free to use interrupted acquisitions, this code generates
# pseudo-random inter stim intervals of 1, 2 or 3 TRs
# random_isi = []
# stack = np.hstack((np.repeat(3, 40), np.repeat(2, 22), np.repeat(4, 20)))
#
# for run in range(nb_block):
#    np.random.seed(run * 10 + run)
#    random_stack = np.random.permutation(stack)
#    random_isi.append(random_stack)

# In our case, we used a fixed list of intervals

# %% STIM TO PRELOAD

# Set sampling rate
control.defaults.audiosystem_sample_rate = 16000

exp = design.Experiment('formisano_protocol')
control.initialize(exp)

exp.data_variable_names = ["Block", "Trial", "Onset", "Duration", "Condition",
                           "Response", "RT"]

# TTL cross
fix_TTL = stimuli.FixCross(size=(40, 40), line_width=6,
                           colour=colors['red'])
fix_TTL.preload()

# Fix cross at the start of each run
final_fix = stimuli.FixCross(size=(40, 40), line_width=6,
                             colour=colors['white'])
final_fix.preload()

# End of block message
end_block = stimuli.TextBox(str(''.join(('Fin du bloc.',
                            '\n\n', 
                            'Veuillez attendre les instructions.'))),
                            (1000,1000), position=(0, -400),
                             text_size=44)
end_block.preload()

# End of experiment message

end_experiment = stimuli.TextBox(str(''.join(('Fin du bloc.',
                            '\n\n',
                            'Veuillez attendre les instructions.'))),
                            (1000,1000), position=(0, -400),
                             text_size=44)

# %%
# ============= WAITS FOR USER TO ENTER RUN NUMBER TO START ===============

# Define number of runs
nb_block = len(runs_list)

# Wait 5 seconds in order to launch input text screen
exp.keyboard.wait(duration=5000)

# Create text input box
ti = io.TextInput(message='Number of the Run:', message_text_size=24,
                  message_colour=colors["purple"],
                  user_text_colour=colors["white"],
                  ascii_filter=misc.constants.K_ALL_DIGITS,
                  background_colour=(0, 0, 0),
                  frame_colour=(70, 70, 70))

# Load user's input
while True:
    sb = ti.get('0')
    # If string is empty
    if not sb:
        warning_message1 = stimuli.TextLine("Please enter a number between 0 and 5",
                                            text_size=24,
                                            text_colour=colors["red"])
        warning_message1.present()
        exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
        continue
    # If run (aka block) number introduced is higher than the number of
    # runs preset in config file
    elif int(sb) >= nb_block:
        warning_message2 = stimuli.TextLine("The maximum run number is 5",
                                            text_size=24,
                                            text_colour=colors["red"])
        warning_message2.present()
        exp.keyboard.wait(misc.constants.K_RETURN, duration=5000)
        continue
    else:
        start_block = int(sb)
        break

# %% DESIGN

block_list = [design.Block(name='run%d' % block)
              for block in np.arange(nb_block)]

# For each run
for block in np.arange(nb_block):

    # Set the path to the folder containing the files
    path_to_stim = os.path.join(stim_path,
                                'set%s' % set_pairs[int(acq_num)][0][block])

    # For each trial
    for line in runs_list[block].readlines():

        stim_filename = make_tuple(make_tuple(line))

        # Create a trial (unexpected)
        trial = design.Trial()
        trial.set_factor('condition', stim_filename[1].strip())

        if trial.get_factor('condition') != 'catch':
            trial.set_factor('condition', stim_filename[0].replace('.wav', ''))

        # And one stimulus for that trial
        if trial.get_factor('condition') == 'silence':
            stim = stimuli.TextLine("")
        else:
            stim = stimuli.Audio(os.path.join(path_to_stim,
                                              stim_filename[0].strip()))

        trial.add_stimulus(stim)

        block_list[block].add_trial(trial)

    exp.add_block(block_list[block])

# %% EXPERIMENT

control.start(exp, skip_ready_screen=True)

# We used a fixed set of ISI for this experiment, which will be 28 repetitions
# of 3, 2 and 2 TRs for all runs. 1TR = 2s

tr_time = 2000
chunk = np.array((2, 2, 3))

isi_list = np.tile(chunk, 28) * tr_time

for b, block in enumerate(exp.blocks[start_block:]):

    # Set the list that will be used for the ISI of this run
    # 1 TR = 2s in our case -- ONLY FOR RANDOMIZED ISI
    # isi_list = random_isi[b] * 2000

    # Wait for TTL
    fix_TTL.present()
    exp.keyboard.wait_char('t')

    t0 = misc.Clock()

    # 2s fix cross before starting
    final_fix.present()
    exp.clock.wait(2000)

    for t, trial in enumerate(block.trials):

        # ################## SOUND PRESENTATION ###################

        # Get onset
        sound_onset = t0.time
        # Present stim
        trial.stimuli[0].present()

        io.Screen.clear(exp.screen)
        final_fix.present()

        # Wait for "Y" key press and register response type
        key, rt = exp.keyboard.wait(keys=[misc.constants.K_y],
                                    duration=tr_time)

        if rt is None: rt = tr_time

        exp.clock.wait(tr_time - rt)

        if key == 121:
            if trial.get_factor('condition') == 'catch':
                key = 'hit'
            else:
                key = 'false_alarm'
        else:
            if trial.get_factor('condition') == 'catch':
                key = 'miss'
            else:
                key = 'N/A'

        # Get duration
        sound_dur = t0.time - sound_onset

        # Add data to the data file
        condition = 'sound_presentation'
        exp.data.add([block.name, trial.id, sound_onset, sound_dur, condition, key, rt])

        exp.clock.wait(10)

        # ################## ACQUISITION TIME ####################

        # Get the onset
        acq_onset = t0.time

        # Wait certain number of TRs
        #exp.clock.wait(isi_list[t])

        # This block registers up to 3 TTLs during the total duration of isi_list[t].
        # We used it for testing purposes due to technical problems with our scanner,
        # but it can be removed or commented if this is not necessary

        key, rt = exp.keyboard.wait(keys=[misc.constants.K_t], duration=isi_list[t])
        
        if rt is not None:
        
            # Add TTL1 data to the logfile
            TTL1_onset = t0.time
            exp.data.add([block.name, trial.id, TTL1_onset, '-', 'TTL1'])
        
            remaining_isi = isi_list[t] - rt
            print(rt, remaining_isi)
            key, rt2 = exp.keyboard.wait(keys=[misc.constants.K_t], duration=remaining_isi)
        
            if rt2 is not None:
        
                # Add TTL2 data to the logfile
                TTL2_onset = t0.time
                exp.data.add([block.name, trial.id, TTL2_onset, '-', 'TTL2'])
        
                remaining_isi -= rt2
                print(rt2, remaining_isi)
                key, rt3 = exp.keyboard.wait(keys=[misc.constants.K_t], duration=remaining_isi)
        
                if rt3 is not None:
        
                    # Add TTL3 data to the logfile
                    TTL3_onset = t0.time
                    exp.data.add([block.name, trial.id, TTL3_onset, '-', 'TTL3'])
        
                    remaining_isi -= rt3
                    print(rt3, remaining_isi)
                    exp.clock.wait(remaining_isi)

        # Get duration
        acq_dur = t0.time - acq_onset

        # Add data to the data file
        condition = trial.get_factor('condition').replace('s2_', '')
        exp.data.add([block.name, trial.id, acq_onset, acq_dur, condition])

    exp.clock.wait(tr_time)
    io.Screen.clear(exp.screen)
    end_block.present()
    exp.keyboard.wait(keys=[misc.constants.K_SPACE])
    io.Screen.clear(exp.screen)

control.end()
