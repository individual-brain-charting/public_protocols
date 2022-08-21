"""
Protocol code for motion perception task

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
January 2022
"""

from psychopy import core, visual, event, data
from sklearn.utils import check_random_state
import pandas as pd
from os.path import join, exists
from os import mkdir, sep, name, system
from math import tan, radians
from numpy import repeat


def formula(deg, distance, res, size):
    return (tan((radians(deg)/2))*distance*res*2)/size


def convert_deg_to_pix(screen_params, exp_params_deg):

    exp_params_pix = {}

    for param, value in exp_params_deg.items():
        exp_params_pix[param] = formula(exp_params_deg[param],
                                     screen_params['distance'],
                                     screen_params['res_xy'][0],
                                     screen_params['size_xy'][0])

    exp_params_pix['field_size_y'] = formula(exp_params_deg['field_size_y'],
                                             screen_params['distance'],
                                             screen_params['res_xy'][1],
                                             screen_params['size_xy'][1])

    exp_params_pix['dot_density'] = exp_params_deg['dot_density']/formula(1,
                                     screen_params['distance'],
                                     screen_params['res_xy'][0],
                                     screen_params['size_xy'][0])

    exp_params_pix['n_dots'] = int((exp_params_pix['field_size_x']*
                                exp_params_pix['field_size_y']*
                                exp_params_pix['dot_density'])/60)

    return exp_params_pix


def extend_to_all_fields(exp_param):
    
    exp_params_all_fields = {}

    for field in ['both', 'left', 'right']:
        exp_params_all_fields[field] = exp_param.copy()
        if field == 'left':
            exp_params_all_fields[field]['field_center_x'] = -exp_param['field_size_x']/4
            exp_params_all_fields[field]['field_center_y'] = 0
            exp_params_all_fields[field]['field_size_x'] = exp_param['field_size_x']/2
            exp_params_all_fields[field]['n_dots'] = int(exp_param['n_dots']/2)
        elif field == 'right':
            exp_params_all_fields[field]['field_center_x'] = exp_param['field_size_x']/4
            exp_params_all_fields[field]['field_center_y'] = 0
            exp_params_all_fields[field]['field_size_x'] = exp_param['field_size_x']/2
            exp_params_all_fields[field]['n_dots'] = int(exp_param['n_dots']/2)
        else:
            exp_params_all_fields[field]['field_center_x'] = 0
            exp_params_all_fields[field]['field_center_y'] = 0

    return exp_params_all_fields


def take_input(total_runs=4):
    while True:
        try:
            sub_num = int(input("Enter subject number: "))
            run_num = int(input(f"Enter initial run number (1-{total_runs}): "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        # finally:
        #     if run_num > total_runs or run_num < total_runs:
        #         print(f"Run number should be between 1 or {total_runs}")
        #         continue
        else:
            break

    return sub_num, run_num, total_runs


def show_init_screen(window, text, wait_key, color='red'):
    fixation = visual.TextStim(window,
                               text=text,
                               pos=[0, 0],
                               height=0.15,
                               color=color,
                               wrapWidth=1.8)
    fixation.draw()
    window.flip()

    event.clearEvents()
    if wait_key is None:
        return True

    # wait for TTL
    while True:
        keys = event.getKeys([wait_key, 'escape'])
        if 'escape' in keys:
            window.close()
            exit()
        if wait_key in keys:
            return True


def show_end_screen(window, text, expected_key):
    textbox = visual.TextStim(window, text, color='white')
    textbox.draw()
    window.flip()

    event.clearEvents()
    while True:
        keys = event.getKeys([expected_key])
        if expected_key in keys:
            window.close()
            return True


def save_log(log_df, task, sub_num, run_num, date):
    if not exists('log'):
        mkdir('log')

    df = pd.DataFrame(log_df)
    df = df.sort_values(by=['time_points'])
    log_filename = join('log', '%s_sub-%02d_run-%02d_log_%s.csv' % (task,
                         sub_num, run_num, date))
    df.to_csv(f'{log_filename}', index=False)

    return log_filename


def fix_color_sequence(random_state, cycles, task, trials_per_cycle,
                     trial_duration, att_fix_dur, blue_prob, rep_thres=5):

    rng = check_random_state(random_state)
    fixation_colors = ['red', 'yellow', 'green', 'magenta', 'white', 'blue']
    n_trials = int(((cycles * trials_per_cycle) + 1) *
                 ((trial_duration / att_fix_dur) + 1) + 1)

    other_prob = (1-blue_prob)/(len(fixation_colors)-1)
    all_probs = [other_prob for i in range(len(fixation_colors)-1)]
    all_probs.append(blue_prob)

    color_sequence = rng.choice(fixation_colors, n_trials,
                                 p=all_probs, replace=True).tolist()

    no_rep = []
    for idx in range(0, len(color_sequence) - 1):
        fixation_colors_copy = fixation_colors[:]
        # getting Consecutive elements 
        if color_sequence[idx] == color_sequence[idx + 1]:
            if idx != 0:
                fixation_colors_copy.remove(color_sequence[idx])
                fixation_colors_copy.remove(no_rep[idx-1])
            else:
                fixation_colors_copy.remove(color_sequence[idx])
            replacement = rng.choice(fixation_colors_copy, 1, replace=True).tolist()[0]
            no_rep.append(replacement)
        else:
            no_rep.append(color_sequence[idx])

    color_sequence = no_rep[:]

    filename = join('seq', f'{task}_att_fix_seq_{random_state}.csv')
    if not exists(filename):
        df = {"Fixation Color Sequence": color_sequence}
        df = pd.DataFrame(data=df)
        df.to_csv(filename, index=False)

    return filename


def coherent_type_sequence(random_state, cycles, task):

    rng = check_random_state(random_state)

    types = ['coherent_anti', 'coherent_clock']
    type_sequence = rng.choice(types, cycles, replace=True)

    filename = join('seq', f'{task}_coherent_type_seq_{random_state}.csv')
    if not exists(filename):
        df = {"Coherent Stim Type Sequence": type_sequence}
        df = pd.DataFrame(data=df)
        df.to_csv(filename, index=False)

    return filename


def init_angle_sequence(random_state, cycles, task, n_angles):

    rng = check_random_state(random_state)
    
    increment = int(360/n_angles)
    all_angles = [*range(0, 360, increment)]
    angle_sequence = rng.choice(all_angles, cycles, replace=True)

    filename = join('seq', f'{task}_init_angle_seq_{random_state}.csv')
    if not exists(filename):
        df = {"Initial Angle Sequence": angle_sequence}
        df = pd.DataFrame(data=df)
        df.to_csv(filename, index=False)

    return filename


def display_field_sequence(random_state, cycles, task):

    rng = check_random_state(random_state)

    fields = ['left', 'right', 'both']
    n_fields = len(fields)
    assert cycles % n_fields == 0

    field_sequence = repeat(fields, cycles//n_fields)
    rng.shuffle(field_sequence)

    filename = join('seq', f'{task}_display_field_seq_{random_state}.csv')
    if not exists(filename):
        df = {"Display Field Sequence": field_sequence}
        df = pd.DataFrame(data=df)
        df.to_csv(filename, index=False)

    return filename


def trial_type_sequence(random_state, cycles, task, trial_seq):

    rng = check_random_state(random_state)

    trial_type_seq = []
    for cycle in range(cycles):
        rng.shuffle(trial_seq)
        for trial in trial_seq:
            trial_type_seq.append(trial)

    filename = join('seq', f'{task}_trial_type_seq_{random_state}.csv')
    if not exists(filename):
        df = {"Trial type Sequence": trial_type_seq}
        df = pd.DataFrame(data=df)
        df.to_csv(filename, index=False)

    return filename


def create_load_sequences(run_num, cycles, task, trial_seq, trial_duration,
                         att_fix_dur, blue_prob=0.05):
    if not exists('seq'):
        mkdir('seq')

    att_fix_seq = fix_color_sequence(run_num, cycles, task, len(trial_seq),
                                     trial_duration, att_fix_dur, blue_prob)
    coherent_type_seq = coherent_type_sequence(run_num, cycles, task)
    display_field_seq = display_field_sequence(run_num, cycles, task)
    trial_type_seq = trial_type_sequence(run_num, cycles, task, trial_seq)

    seq_files = [att_fix_seq, coherent_type_seq, display_field_seq, trial_type_seq]
    sequences = []
    for file in seq_files:
        df = pd.read_csv(file)
        sequences.append(df[df.columns[0]])

    return sequences[0], sequences[1], sequences[2], sequences[3]


def present_trial(window, task, att_fix_seq, init_angle, exp_param, color_cnt,
                 sub_num, run_num, date, clock, log_df,
                 trial_type, duration, att_fix_dur):

    if trial_type == 'coherent_anti' or trial_type == 'coherent_clock':
        speed = exp_param['dot_speed']
        coherence = 1
        angles = 6
    elif trial_type == 'incoherent':
        speed = exp_param['dot_speed']
        coherence = 0
        angles = 6
    elif trial_type == 'stationary':
        speed = 0
        coherence = 1
        angles = 1

    fixation_frames = int(att_fix_dur//window.monitorFramePeriod)
    attention_fixation = visual.Polygon(window, edges=100,
                                 radius=exp_param['dot_size'], pos=[0, 0],
                                 fillColor=att_fix_seq[color_cnt], units='pix')
    attention_bg = visual.Rect(window, size=exp_param['inner_border'], pos=[0, 0],
                                fillColor='black', units='pix')
    response = []

    duration_per_angle = duration / angles
    motion_frames = int(duration_per_angle//window.monitorFramePeriod)
    dot_life_sec = 1
    dot_life_frames = int(dot_life_sec//window.monitorFramePeriod)
    angle = init_angle
    count_angle = 0

    while count_angle<angles:
        if 'escape' in event.getKeys(['escape']):
            log_df['time_points'].append(clock.getTime())
            log_df['events'].append('escaped')
            task = f'par_{task}'
            log_filename = save_log(log_df, task, sub_num, run_num, date)
            window.close()
            exit()

        angle = angle%360
        log_df['time_points'].append(clock.getTime())
        log_df['events'].append(f'{trial_type}')
        dot_stim = visual.DotStim(window, fieldShape='sqr', fieldPos=(exp_param['field_center_x'],0),
                     fieldSize=(exp_param['field_size_x'], exp_param['field_size_y']),
                     dir=angle, dotSize=exp_param['dot_size'], signalDots='same', units='pix',
                     noiseDots='direction', speed=speed, dotLife=dot_life_frames,
                     nDots=int(exp_param['n_dots']), coherence=coherence)

        for current_frame in range(1, motion_frames+1):
            if current_frame == 1 and count_angle == 0:
                log_df['time_points'].append(clock.getTime())
                log_df['events'].append(f'att_fix_{att_fix_seq[color_cnt]}')
                color_cnt += 1

            if current_frame % fixation_frames == 0:
                attention_fixation.fillColor = att_fix_seq[color_cnt]
                log_df['time_points'].append(clock.getTime())
                log_df['events'].append(f'att_fix_{att_fix_seq[color_cnt]}')
                color_cnt += 1

            if 'escape' in event.getKeys(['escape']):
                log_df['time_points'].append(clock.getTime())
                log_df['events'].append('escaped')
                task = f'par_{task}'
                log_filename = save_log(log_df, task, sub_num, run_num, date)
                window.close()
                exit()

            if response:
                log_df['time_points'].append(response[0][1])
                log_df['events'].append(response[0][0])

            dot_stim.draw()
            attention_bg.draw()
            attention_fixation.draw()
            response = event.getKeys(['y'], timeStamped=clock)
            window.flip()

        if trial_type == 'coherent_clock':
            angle = angle - 60
        else:
            angle = angle + 60

        count_angle += 1


    log_df['time_points'].append(clock.getTime())
    log_df['events'].append('iti_fix')
    fixation = visual.TextStim(window, text="+", pos=[0, 0], height=0.15,
                                color='white', wrapWidth=1.8)
    fixation.draw()
    window.flip()
    core.wait(2)

    return log_df, color_cnt


def calculate_accuracy(log_filename):
    data = pd.read_csv(log_filename)
    data['events_clean'] = data.events.str.split('_').str[0]

    stimuli_resp = data.loc[data.events_clean.isin(['att', 'y'])]
    stimuli = data.loc[data.events_clean.isin(['att'])]
    n_trials = len(stimuli)

    probes = stimuli_resp['events']=='att_fix_blue'
    resp = stimuli_resp['events']=='y'

    probes_resp = stimuli_resp[probes | resp]
    events = list(probes_resp.events)
    times = list(probes_resp.time_points)

    if 'y' not in events:
        accuracy = 'No responses registered'
    else:
        verdict = []
        counter = 0
        while counter < len(events):
            if events[counter] == 'att_fix_blue' and counter == len(events)-1:
                verdict.append('fn')
                break
            elif events[counter] == 'y':
                verdict.append('fp')
                counter = counter + 1
            elif events[counter] == 'att_fix_blue' and events[counter+1] == 'y':
                if times[counter+1] - times[counter] <= 1:
                    verdict.append('tp')
                else:
                    verdict.append('fn')
                counter = counter + 2
            else:
                verdict.append('fn')
                counter = counter + 1

        # calculations
        sum_tp_fp_fn =  len(verdict)
        counts = pd.Series(verdict).value_counts()

        for verdict in ['tp','fn','fp']:
            if verdict not in list(counts.index):
                counts[verdict] = 0

        tp = counts.tp; fn = counts.fn; fp = counts.fp
        tn = n_trials - sum_tp_fp_fn
        assert tp + fp + fn + tn == n_trials
        accuracy = ((tp + tn)/n_trials)*100
        accuracy = round(accuracy, 2)
    
    return accuracy


def present_run(window, task, sub_num, run_num, exp_param_all_fields,
                 cycles=9, trial_duration=12, att_fix_dur=0.5):

    date = data.getDateStr()
    clock = core.Clock()
    log_df = {'time_points': [], 'events': []}

    trial_seq = ['incoherent', 'stationary', 'coherent']
    if task == 'pract':
        blue_prob = 0.3
    else:
        blue_prob = 0.05
    att_fix_seq, coherent_type_seq, display_field_seq, trial_type_seq = create_load_sequences(
                                         run_num, cycles, task, trial_seq,
                                         trial_duration, att_fix_dur, blue_prob)
    color_cnt = 0
    trial_cnt = 0
    for cycle in range(1, cycles+1):
        exp_param = exp_param_all_fields[display_field_seq[cycle-1]]
        for i in range(3):
            trial_type = trial_type_seq[trial_cnt]
            if trial_type=='coherent':
                trial_type = coherent_type_seq[cycle-1]
            init_angle = 0
            log_df, color_cnt = present_trial(window, task, att_fix_seq,
                                            init_angle, exp_param,
                                            color_cnt, sub_num, run_num, date,
                                            clock, log_df, trial_type,
                                            trial_duration, att_fix_dur)
            trial_cnt += 1

    log_df, color_cnt = present_trial(window, task, att_fix_seq,
                                    init_angle, exp_param,
                                    color_cnt, sub_num, run_num, date,
                                    clock, log_df, 'stationary',
                                    trial_duration, att_fix_dur)
    log_df['time_points'].append(clock.getTime())
    log_df['events'].append('End')
    log_filename = save_log(log_df, task, sub_num, run_num, date)

    return log_filename



if __name__ == "__main__":

    sub_num, run_num, max_runs = take_input()
    task = 'task-motion'

    # Parameters defining screen setup
    # laptop_screen_param = {'distance':0.30, 'res_xy':(1920, 1080), 'size_xy':(0.30, 0.18)}
    BOLD_screen_param = {'distance':0.89, 'res_xy':(1920, 1080), 'size_xy':(0.60, 0.45)}

    # Stimulus parameters, in degrees, from the study
    exp_param_deg = {'field_size_x': 40, 'field_size_y': 20, 'inner_border': 3,
                     'dot_size': 0.143, 'dot_speed': 0.1, 'dot_density': 6}
    # Convert to pixels
    exp_param_pix = convert_deg_to_pix(BOLD_screen_param, exp_param_deg)
    exp_param_all_fields = extend_to_all_fields(exp_param_pix)

    window = visual.Window(fullscr=True, size=(1920, 1080), color=(-1, -1, -1), screen=1)
    show_init_screen(window, color='white', wait_key="space",
     text=("Le protocole de mouvement sera présenté maintenant"
     "\nAppuyez sur << espace >> pour commencer."))
    window.close()

    for run in range(run_num, max_runs+1):
        window = visual.Window(fullscr=True, size=(1920, 1080), color=(-1, -1, -1), screen=1)
        show_init_screen(window, text='+', wait_key="t")
        log_file = present_run(window, task, sub_num, run, exp_param_all_fields)

        if log_file.split('_')[0] == 'par':
            continue
        else:
            accuracy = calculate_accuracy(log_file)

        show_end_screen(window, text=f'Accuracy = {accuracy}%\nFINI',
                         expected_key='space')

        window.close()
