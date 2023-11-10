"""
Protocol code for training session of color perception task.
Imports from protocol.py

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
November 2021
"""

from psychopy import visual
from protocol import (make_stim_sequence_random, load_stim_sequence,
                      show_init_screen, show_end_window,
                      present_stimulus_blocks)


if __name__ == "__main__":

    while True:
        try:
            sub_num = int(input("Enter subject number: "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        else:
            break

    # s = make_stim_sequence_random(num_blocks=4, stim_per_block=12, probe_proportion=0.2,
    #                             seq_fname=f'stim_seq/stim_sequence_pract.csv',
    #                             random_state=5)
    all_stimuli, stim_names = load_stim_sequence(stim_sequence_file=f'stim_seq/stim_sequence_pract.csv')
    all_stimuli = all_stimuli / 256.

    gray = all_stimuli[0, 0, 0, 0] * 2 - 1.

    window = visual.Window(fullscr=True, color=gray, size=(1920, 1080))

    show_init_screen(window, text=("Appuyez sur Y lorsqu'une image apparait deux fois"
                                "\nAppuyez sur << espace >> pour commencer."),
                    wait_key='space', color='white')

    present_stimulus_blocks(window, all_stimuli, stim_names, sub_num, 1, task='pract')

    show_end_window(window, text='FINI', expected_key='space')

    window.close()