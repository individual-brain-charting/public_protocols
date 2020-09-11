# -*- coding: utf-8 -*-
"""
Short version of 'formisano_protocol.py' used for participant training
before the real experiment.

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import os
import numpy as np
import random
import copy

from expyriment import design, control, stimuli, misc, io
from ast import literal_eval as make_tuple

my_path = os.getcwd()

stim_path = os.path.join(my_path, '../stim/prerandomizations')

files_path = os.path.join(my_path, '../stim/all')

colors = {'black': (0, 0, 0), 'purple': (166, 166, 237),
          'yellow': (237, 237, 166), 'gray': (70, 70, 70),
          'red': (204, 0, 0), 'white': (255, 255, 255)}


def get_stim(path, number, catch=True, silence=True):
    """
    Generates a short list containing filenames to load into the experiment

    Parameters
    ----------

    path: str
          path to the stim. In this case, we are going to randomly grab one
          of the prerandomizations each time we run the function

    number: int
            number of stim desired in the list

    silence: bool
             if True, it will insert a silence trial in the list and lower
             the number of files selected in 1 (default = True)

    catch: bool
           same behavior as silence, will insert a catch trial at the end
           (default = True)

    Returns
    -------

    file_list: list
               list containing filenames to load on the experiment
    """

    # Make a list of all files in path
    all_files = sorted(os.listdir(path))

    # Pick a random prerandomization
    prerand_path = os.path.join(path, random.choice(all_files))

    # Open it
    trial_list = [make_tuple(make_tuple(line)) for line in open(prerand_path).readlines()]

    # Remove 'catch' and 'silences'
    clean_list = list(filter(lambda x: x[1] != 'silence' and x[1] != 'catch', trial_list))

    # Determine the length of file_list and pick a slice of clean_list

    number -= silence + catch

    start_slice = random.randint(1, (len(clean_list) - number))

    file_list = clean_list[start_slice: start_slice + number]

    # Insert a catch and silence if specified in parameters

    if catch:

        idx = random.randint(1, len(file_list))
        file_list.insert(idx, copy.copy(file_list[idx - 1]))
        #file_list[idx][1] = 'catch'

    if silence:

        idx = random.randint(1, len(file_list) - 1)
        file_list.insert(idx, ['silence', 'silence'])

    return file_list

def design_training(name, path_to_stim, stim_names):
    """
    Returns an expyriment block object that will be used for the experiment

    Paramenters
    -----------

    name: str
          desired name for the block

    path_to_stim: str
                  folder containing the files

    stim_names: list
                contains the necessary information

    Returns
    -------

    training_block: expyriment design.Block object
                    contains all the stim and trials to be used by the
                    experiment
    """

    test_block = design.Block(name=name)

    for line in stim_names:

        trial = design.Trial()

        if line[1] == 'catch':
            trial.set_factor('condition', line[1])

        else:
            trial.set_factor('condition', line[0].replace('.wav', ''))

        if trial.get_factor('condition') == 'silence':
            stim = stimuli.TextLine("")

        else:
            stim = stimuli.Audio(os.path.join(path_to_stim, line[0]))

        trial.add_stimulus(stim)

        test_block.add_trial(trial)

    return test_block


# Dev mode
control.set_develop_mode(False)

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

# %% DESIGN

stim_list = get_stim(stim_path, 10)

test_block = design_training('training', files_path, stim_list)

# %% EXPERIMENT

control.start(exp, skip_ready_screen=True)

# We used a fixed set of ISI for this experiment, which will be 28 repetitions
# of 3, 2 and 2 TRs for all runs. 1TR = 2s

tr_time = 2000
chunk = np.array((2, 2, 3))

isi_list = np.tile(chunk, len(stim_list)) * tr_time

# Wait for TTL
fix_TTL.present()
exp.keyboard.wait_char('t')

t0 = misc.Clock()

# 2s fix cross before starting
final_fix.present()
exp.clock.wait(2000)

for t, trial in enumerate(test_block.trials):

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
    exp.data.add([test_block.name, trial.id, sound_onset, sound_dur, condition, key, rt])

    exp.clock.wait(10)

    # ################## ACQUISITION TIME ####################

    # Get the onset
    acq_onset = t0.time

    # Wait certain number of TRs
    exp.clock.wait(isi_list[t])

    # Get duration
    acq_dur = t0.time - acq_onset

    # Add data to the data file
    condition = trial.get_factor('condition').replace('s2', '')
    exp.data.add([test_block.name, trial.id, acq_onset, acq_dur, condition])

exp.clock.wait(tr_time)
io.Screen.clear(exp.screen)
end_block.present()
exp.keyboard.wait(keys=[misc.constants.K_SPACE])
io.Screen.clear(exp.screen)

control.end()
