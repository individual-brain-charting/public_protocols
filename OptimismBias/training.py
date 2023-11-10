"""
Protocol code for training session of optimism bias.
Imports from protocol.py

Author:
Swetha Shankar, Himanshu Aggarwal
himanshu.aggarwal@inria.fr
March 2022
"""

from os.path import join
from os import sep, getcwd
from psychopy import visual, data
import glob
import pandas as pd
from protocol import (take_input, occurence_seq,
                    show_init_screen, present_stimulus_blocks,
                    show_end_window)

if __name__ == "__main__":

    sub_num, run_num, max_runs = take_input(total_runs=1)
    task = 'pract'

    stim_dir = join(getcwd(), 'stim')
    stim_files = glob.glob("%s/training.txt" % stim_dir)

    for run in range(run_num, 2):
        date = data.getDateStr()
        log_filename = join('log','%s_sub-%02d_run-%02d_log_%s.csv' % (task, sub_num,
                         run_num, date))
        
        stim_seq = pd.read_csv(stim_files[run-1], header=None, sep='\n')
        stim_seq = stim_seq[0]
        occ_seq = occurence_seq(run_num, len(stim_seq), task)
        window = visual.Window(fullscr=True, color=[0.5,0.5,0.5])
        clock, init_time = show_init_screen(window, wait_key='space',
                            color='black', size=0.1,
                            text=("Appuyer sur « y », lorsque le souvenir commence à se former.\n\n"
                                "Appuyer « y » si l'épisode est très stimulant,\n"
                                "« u » si un peu stimulant\net « i » si non stimulant.\n\n"
                                "Appuyer « y » si l'épisode est positif\n"
                                "« u » si neutre\net « i » si négatif."
                                "\n\n"
                                "Appuyer sur « espace » pour commencer."))
        present_stimulus_blocks(window, clock, init_time, stim_seq, occ_seq,
                                 log_filename, task_keys={'y', 'u', 'i', 'escape'})
        show_end_window(window, text='FIN', expected_key='space')

    window.close()
