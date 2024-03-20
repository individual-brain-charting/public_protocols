#! /usr/bin/env python
# Time-stamp: <2019-03-12 16:44:46 christophe@pallier.org>

import sys
from expyriment import design, control, stimuli, io, misc

AUDIO = sys.argv[1]

exp = design.Experiment(name="Le_Petit_Prince")

control.set_develop_mode(False)
control.defaults.open_gl = 2
control.defaults.window_mode = True
control.defaults.window_size = (1920, 1080)

##
control.initialize(exp)

stim = stimuli.Audio(AUDIO)
stim.preload()

fixcrossGreen = stimuli.FixCross(size=(45, 45), line_width=5,
                                 colour=(0, 255, 0))
fixcrossGreen.preload()
fixcrossGrey = stimuli.FixCross(size=(45, 45), line_width=3,
                                colour=(192, 192, 192))
fixcrossGrey.preload()

def clear_screen():
    exp.screen.clear()
    exp.screen.update()

def wait_for_MRI_synchro():
    fixcrossGreen.present(clear=True, update=True)
    exp.keyboard.wait_char('t')

control.start(exp, skip_ready_screen=True)

wait_for_MRI_synchro()
clear_screen()
fixcrossGrey.present(clear=True, update=True)
exp.clock.wait(5000)
stim.present()
control.wait_end_audiosystem()
io.Keyboard.process_control_keys()

control.end()
