"""
Protocol code for training session of motion perception task.
Imports from protocol.py

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
January 2022
"""

from psychopy import visual
from protocol import (take_input, convert_deg_to_pix,
                     show_init_screen, present_run, extend_to_all_fields,
                     calculate_accuracy, show_end_screen)

if __name__ == "__main__":

    sub_num, run_num, max_runs = take_input(total_runs=1)
    task = 'pract'

    # Parameters defining screen setup
    # laptop_screen_param = {'distance':0.30, 'res_xy':(1920, 1080), 'size_xy':(0.30, 0.18)}
    BOLD_screen_param = {'distance':0.89, 'res_xy':(1920, 1080), 'size_xy':(0.60, 0.45)}

    # Stimulus parameters, in degrees, from the study
    exp_param_deg = {'field_size_x': 40, 'field_size_y': 20, 'inner_border': 3,
                     'dot_size': 0.143, 'dot_speed': 0.1, 'dot_density': 6}
    # Convert to pixels
    exp_param_pix = convert_deg_to_pix(BOLD_screen_param, exp_param_deg)
    exp_param_all_fields = extend_to_all_fields(exp_param_pix)

    for run in range(run_num, max_runs+1):
        window = visual.Window(fullscr=True, size=(1920, 1080), color=(-1, -1, -1))
        show_init_screen(window, wait_key="space",
         text='Appuyer sur << y >> lorsque le point devient bleu\nAppuyer sur espace pour commencer ')        
        
        log_file = present_run(window, task, sub_num, run, exp_param_all_fields, cycles=3)

        if log_file.split('_')[0] == 'par':
            continue
        else:
            accuracy = calculate_accuracy(log_file)

        show_end_screen(window, text=f'Accuracy = {accuracy}\n\nFINI',
                         expected_key='space')

    window.close()