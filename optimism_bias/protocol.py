"""
Protocol code for optimism bias

Author:
Swetha Shankar, Himanshu Aggarwal
himanshu.aggarwal@inria.fr
March 2022
"""

from sklearn.utils import check_random_state
from numpy import repeat
import glob
import pandas as pd
from os.path import join, exists
from os import mkdir, sep, getcwd
from psychopy import core, visual, event, data


def take_input(total_runs):
    while True:
        try:
            sub_num = int(input("Enter subject number: "))
            run_num = int(input(f"Enter initial run number (1-{total_runs}): "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        else:
            break

    return sub_num, run_num, total_runs

def occurence_seq(run_num, n_trials, task):
    if not exists('stim'):
        mkdir('stim')

    rng = check_random_state(run_num)

    types = ['Passé', 'Futur']
    occ_sequence = repeat(types, n_trials//len(types))
    rng.shuffle(occ_sequence)

    filename = join('stim', f'{task}_occ_seq_{run_num}.csv')
    if not exists(filename):
        df = {"Occurence Sequence": occ_sequence}
        df = pd.DataFrame(data=df)
        df.to_csv(filename, index=False)

    df = pd.read_csv(filename)
    occ_sequence = df[df.columns[0]]

    return occ_sequence

# Function that shows the initial fixation cross and waits for the TTL pulse
def show_init_screen(window, text, wait_key, color='red', size=0.15):
    fixation = visual.TextStim(window,
                               text=text,
                               pos=[0, 0],
                               height=size,
                               color=color,
                               wrapWidth=1.8)
    fixation.draw()
    window.flip()

    event.clearEvents()
    if wait_key is None:
        return True

    # wait for TTL
    while True:
        keys = event.getKeys(keyList=[wait_key, 'escape'])
        if 'escape' in keys:
            window.close()
            exit()
        if wait_key in keys:
            global_t = core.Clock()
            init_time = global_t.getTime()
            return global_t, init_time

# Function that presents a run
def present_stimulus_blocks(window, global_t, init_time, stim_seq, occ_seq,
                             log_filename, task_keys):
    n_trials = len(stim_seq)

    end_run = False
    log_dict = {'t' : [], 'eve' : []}
    resp_tracker = []

    log_dict['t'].append(init_time)
    log_dict['eve'].append(f'start')
    cnt = 0
    for occ, stim in zip(occ_seq, stim_seq):
        if not end_run:
            cnt = cnt + 1
            print(f'\nTrial{cnt}:')

            t = global_t.getTime()

            log_dict['t'].append(t)
            log_dict['eve'].append(f'scenario_{occ}')

            scenario = visual.TextStim(window,
                                       text=f"{occ}\n{stim}",
                                       pos=[0, 0],
                                       height=0.10,
                                       color='black',
                                       wrapWidth=1.5)
            scenario.draw()
            window.flip()
            event.clearEvents()
            resp_tracker = []
            while global_t.getTime() < t+14:
                response = event.getKeys(keyList=task_keys, timeStamped=global_t)
                if response:
                    if response[0][0] == 'escape':
                        log_dict['t'].append(response[0][1])
                        log_dict['eve'].append('aborted')
                        end_run = True
                        break
                    else:
                        resp_tracker.append(response)
                        print('\tthinking',resp_tracker[0][0][0])

            if not resp_tracker:
                log_dict['t'].append(global_t.getTime())
                log_dict['eve'].append('nr')
                print('\tno response')
            else:
                log_dict['t'].append(resp_tracker[0][0][1])
                if resp_tracker[0][0][0] == 'y':
                    log_dict['eve'].append('thinking')
                else:
                    log_dict['eve'].append(f'nr_{resp_tracker[0][0][0]}')

            if end_run:
                continue

            log_dict['t'].append(global_t.getTime())
            log_dict['eve'].append(f'arousal_feedback')

            arousal = visual.ImageStim(window, image='stim/arousal.jpg', pos=[0, 0])
            arousal.draw()
            window.flip()
            event.clearEvents()
            resp_tracker = []
            t = global_t.getTime()
            while global_t.getTime() < t+2:
                response = event.getKeys(keyList=task_keys, timeStamped=global_t)
                if response:
                    if response[0][0] == 'escape':
                        log_dict['t'].append(response[0][1])
                        log_dict['eve'].append('aborted')
                        end_run = True
                        break
                    else:
                        resp_tracker.append(response)
            
            if not resp_tracker:
                log_dict['t'].append(global_t.getTime())
                log_dict['eve'].append('nr')
                print('\tno response')
            else:
                log_dict['t'].append(resp_tracker[0][0][1])
                if resp_tracker[0][0][0] == 'y':
                    log_dict['eve'].append('very')
                    print('\tvery', 'y')
                elif resp_tracker[0][0][0] == 'g':
                    log_dict['eve'].append('little')
                    print('\tlittle', 'g')
                elif resp_tracker[0][0][0] == 'r':
                    log_dict['eve'].append('not')
                    print('\tnot', 'r')
                else:
                    log_dict['eve'].append(f'nr_{resp_tracker[0][0][0]}')
                

            if end_run:
                continue

            log_dict['t'].append(global_t.getTime())
            log_dict['eve'].append(f'valence_feedback')

            valence = visual.ImageStim(window, image='stim/valence.jpg', pos=[0, 0])
            valence.draw()
            window.flip()
            event.clearEvents()
            resp_tracker = []
            t = global_t.getTime()
            while global_t.getTime() < t+2:
                response = event.getKeys(keyList=task_keys, timeStamped=global_t)
                if response:
                    if response[0][0] == 'escape':
                        log_dict['t'].append(response[0][1])
                        log_dict['eve'].append('aborted')
                        end_run = True
                        break
                    else:
                        resp_tracker.append(response)

            if not resp_tracker:
                log_dict['t'].append(global_t.getTime())
                log_dict['eve'].append('nr')
                print('\tno response')
            else:
                log_dict['t'].append(resp_tracker[0][0][1])
                if resp_tracker[0][0][0] == 'y':
                    log_dict['eve'].append('positive')
                    print('\tpositive', 'y')
                elif resp_tracker[0][0][0] == 'g':
                    log_dict['eve'].append('neutral')
                    print('\tneutral', 'g')
                elif resp_tracker[0][0][0] == 'r':
                    log_dict['eve'].append('negative')
                    print('\tnegative', 'r')
                else:
                    log_dict['eve'].append(f'nr_{resp_tracker[0][0][0]}')

            if end_run:
                continue

            if cnt < n_trials:
                log_dict['t'].append(global_t.getTime())
                log_dict['eve'].append(f'fix')
                print('fix')

                fixation = visual.TextStim(window,
                                        text='+',
                                        pos=[0, 0],
                                        height=0.15,
                                        color='black',
                                        wrapWidth=1.8)
                fixation.draw()
                window.flip()
                event.clearEvents()
                resp_tracker = []
                t = global_t.getTime()
                while global_t.getTime() < t+12:
                    response = event.getKeys(keyList=['escape'], timeStamped=global_t)
                    if response:
                        if response[0][0] == 'escape':
                            log_dict['t'].append(response[0][1])
                            log_dict['eve'].append('aborted')
                            end_run = True
                            break


    log_dict['t'].append(global_t.getTime())
    log_dict['eve'].append('end')
    log_df = pd.DataFrame(data=log_dict)
    log_df = log_df.sort_values(by=['t'])
    log_df.to_csv(f'{log_filename}', index=False)
    # window.close()
    # exit()

# Function that displays the final screen, after run end
def show_end_window(window, text, expected_key):
    textbox = visual.TextStim(window, text, color='white')
    textbox.draw()
    window.flip()

    event.clearEvents()
    while True:
        keys = event.getKeys([expected_key])
        if expected_key in keys:
            return True

if __name__ == "__main__":

    sub_num, run_num, total_runs = take_input(total_runs=5)
    task = 'optimism-bias'

    stim_dir = join(getcwd(), 'stim')
    stim_files = glob.glob("%s/run*txt" % stim_dir)

    for run in range(run_num, total_runs+1):
        date = data.getDateStr()
        log_filename = join('log','%s_sub-%02d_run-%02d_log_%s.csv' % (task, sub_num, run,
                         date))
        
        stim_seq = pd.read_csv(stim_files[run-1], header=None, sep='\n')
        stim_seq = stim_seq[0]
        occ_seq = occurence_seq(run, len(stim_seq), task)
        window = visual.Window(fullscr=True, size=(1920, 1080), color=[0.5, 0.5, 0.5], screen=1)
        clock, init_time = show_init_screen(window, text='+', wait_key='t')
        present_stimulus_blocks(window, clock, init_time, stim_seq, occ_seq, log_filename,
                                 task_keys={'y', 'g', 'r', ',','escape'})
        show_end_window(window, text='FIN', expected_key='space')

        window.close()
