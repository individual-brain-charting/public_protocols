#! /usr/bin/env python
# updated: <2016-02-04 Esther LIN>
# -*- coding: utf-8 -*-

import pandas as pd
import os.path as op
import sys
import expyriment
from expyriment import design, control, stimuli, io, misc
import pygame

pygame.init()


'''
sent1 = stimuli.Audio("fr_localizer_03_22050.wav")
sent1.preload()
sent1.present()
'''

if len(sys.argv) < 2:
    print(sys.argv[0] + " csvfile")
    print("The csvfile must contained the list of stimuli and onset times")
    sys.exit()
else:
    stimuli_table = sys.argv[1]

exp = design.Experiment(name="bilingue_localizer")

# comment out the following two lines if running the real experiment:
control.set_develop_mode(True)
control.defaults.open_gl = 2

'''
FIXATION_DURATION = 1000
WORD_DURATION = 300
BLOC_DURATION = 6000
RESPONSE_KEYS = [misc.constants.K_b, misc.constants.K_y]
MAX_RESPONSE_DURATION = 1000  # need to be less than (900 + min ITI) 
'''

##
control.initialize(exp)

## load the stimuli table into a block of trials
stim_tbl = pd.read_csv(stimuli_table)

block = design.Block(name="block1")

trial_items = []

for (i, stim_info) in stim_tbl.iterrows():
    trial = design.Trial()
    trial.set_factor("subj", stim_info.subj)
    trial.set_factor("nbloc", stim_info.nbloc)
    trial.set_factor("langue", stim_info.langue)
    trial.set_factor("sent_onset", stim_info.sent_onset)
    trial.set_factor("sent_dur", stim_info.sent_dur)
    trial.set_factor("stims", stim_info.fname)    
    


    sound_fnames = [str("./sound_files/"+stim_info['fname'])]
    trial_items.append(sound_fnames)
    # transform the strings into surfaces to be blit on the screen
    for w in sound_fnames:
        stim = stimuli.Audio(w)
        trial.add_stimulus(stim)
    block.add_trial(trial)

exp.add_block(block)  # note that there is only one block in this experiment

exp.data_variable_names = ["subj", "nbloc", "langue", "sent_onset", 
                           "real_sentence_onset_before","real_sentence_onset_after","sent_dur","filename"]

### A few useful objects and functions 

## define fixation crosses
fixcrossGreen = stimuli.FixCross(size=(45, 45), line_width=5,
                                 colour=(0, 255, 0))
fixcrossGreen.preload()

fixcrossGrey = stimuli.FixCross(size=(45, 45), line_width=3,
                                colour=(192, 192, 192))
fixcrossGrey.preload()

'''
http://www.rapidtables.com/web/color/silver-color.htm
lightgray	rgb(211,211,211)
silver	rgb(192,192,192)
darkgray	rgb(169,169,169)
gray       rgb(128,128,128)
'''


def clear_screen():
    exp.screen.clear()
    exp.screen.update()


def wait_for_MRI_synchro():
    fixcrossGreen.present(clear=True, update=True)
    exp.keyboard.wait_char('t')


def wait_until(clock, time):
    # busy loop wait
    while (clock.time < time):
        pass

############ MAIN LOOP

control.start(exp)


for block in exp.blocks:
    wait_for_MRI_synchro()
    clear_screen()

    # present the fixation cross
    fixcrossGrey.present()    
    
    clock = expyriment.misc.Clock()

    for itrial, trial in enumerate(block.trials):
        #print "Trial: #"+itrial
        for stim in trial.stimuli:
            stim.preload()

        # present the sentence
        wait_until(clock, trial.get_factor("sent_onset"))
        real_sentence_onset_before = clock.time
        stim.present()        
        real_sentence_onset_after = clock.time
        
        io.Keyboard.process_control_keys()

        exp.data.add([trial.get_factor("subj"), trial.get_factor('nbloc'),
                      trial.get_factor('langue'), trial.get_factor('sent_onset'), 
                      real_sentence_onset_before,real_sentence_onset_after,trial.get_factor('sent_dur')," ".join(trial_items[itrial])])

control.end()
