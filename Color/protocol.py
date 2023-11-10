"""
Protocol code for color perception task

Himanshu Aggarwal
himanshu.aggarwal@inria.fr
November 2021
"""

from os import times, sep, name, system
import numpy as np
from psychopy import core, visual, event, data
import math

import pandas
from PIL import Image
from os.path import join as opj

from sklearn.utils import check_random_state


def add_probes(block_types, block_sequence, stim_per_block, probe_proportion,
                random_state=0):

    rng = check_random_state(random_state)
    stim_seq = np.repeat(block_sequence, stim_per_block)
    probes = []
    for chrom in block_types:
        ind_chrom = np.where(stim_seq == chrom)[0]
        prob_chrom = rng.choice(ind_chrom, int(probe_proportion*len(ind_chrom)),
                     replace=False)
        probes.extend(prob_chrom.copy())

    probes.sort()

    return probes


def make_stim_sequence_random(num_blocks, stim_per_block, probe_proportion,
    seq_fname='stim_sequence.csv', path='color_stimuli', random_state=0):

    rng = check_random_state(random_state)

    total_stim = int(num_blocks*stim_per_block)

    block_types = np.array(['chromatic', 'achromatic'])
    block_sequence = block_types[rng.permutation(num_blocks) % 2]

    stim_sequence = dict([(bt, rng.choice(
                    [*range(0,total_stim//2+1)], total_stim//2+1, replace=False)) 
                    for bt in block_types])

    counters = dict([(bt, 0) for bt in block_types])

    probes = add_probes(block_types, block_sequence, stim_per_block,
                        probe_proportion=probe_proportion,
                        random_state=random_state)

    all_files = []

    global_count = 0
    for i, b in enumerate(block_sequence):
        curr_count = counters[b]
        for j in range(stim_per_block):
            if global_count in probes:
                if global_count%(stim_per_block)==0:
                    fname = '%s_%03d.png' % (b,
                             stim_sequence[b][curr_count + j + 1])
                else:
                    fname = '%s_%03d.png' % (b,
                             stim_sequence[b][curr_count + j - 1])
            else:
                fname = '%s_%03d.png' % (b, stim_sequence[b][curr_count + j])
            all_files.append(
                dict(fname=opj(path, fname),
                     chrom=b, block=i, id=curr_count + j + 1))
            global_count = global_count + 1
        counters[b] = curr_count + stim_per_block


    df = pandas.DataFrame(all_files)
    df.to_csv(seq_fname, index=False) 

    return df


def load_stim_sequence(stim_sequence_file='stim_sequence.csv'):

    df = pandas.read_csv(stim_sequence_file)
    all_block_files = []
    for b_id, grp in df.groupby('block'):
        # for chrom in np.unique(df['chrom'].values):
        #     all_block_files.append(grp[grp['chrom'] == chrom]['fname'].values)
        all_block_files.append(grp['fname'].values)

    all_blocks = [[np.array(Image.open(fname))
                   for fname in block]
        for block in all_block_files]

    return np.array(all_blocks), list(df.fname)


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


def save_log(time_point, eve, task, sub_num, run_num, date):
    df = pandas.DataFrame({'t': time_point, 'event': eve})
    df = df.sort_values(by=['t'])
    log_filename = opj('log','%s_sub-%02d_run-%02d_log_%s.csv' % (task, sub_num, run_num,
                     date))
    df.to_csv(f'{log_filename}', index=False)
    return log_filename


def visual_angles_to_pixels(ang_ecc=2.58, ang_ele=2, ang_stim=1.72,
							screen_xy=(0.6,0.45), res_xy=(1920,1080),
							distance=0.89):

	pix_ecc = (math.tan((ang_ecc/2)*(math.pi/180))*distance*res_xy[0])/(screen_xy[0]/2)
	pix_ele = (math.tan((ang_ele/2)*(math.pi/180))*distance*res_xy[1])/(screen_xy[1]/2)
	pix_stim_x = (math.tan((ang_stim/2)*(math.pi/180))*distance*res_xy[0])/(screen_xy[0]/2)
	pix_stim_y = (math.tan((ang_stim/2)*(math.pi/180))*distance*res_xy[1])/(screen_xy[1]/2)

	return pix_ecc, pix_ele, pix_stim_x, pix_stim_y


def present_stimulus_blocks(window, stimulus_blocks, stim_names,
                            sub_num, run_num, task='task-color',
                            block_length_seconds=7.2,
                            pause_length_seconds=5,
                            gray_image=None):

    # if gray_image is None:
    #     gray_image = np.zeros_like(stimulus_blocks[0][0])
    #     gray_image[:] = stimulus_blocks.reshape(-1)[0]
    date = data.getDateStr()
    gray = stimulus_blocks[0, 0, 0, 0] * 2 - 1.

    width, height, center_x, center_y = visual_angles_to_pixels(16, 16)
    stim_size = (int(width), int(height))
    stim_container = visual.ImageStim(window, size=stim_size, units="pix")
    fixation = visual.TextStim(window,
                               text="+",
                               pos=[0, 0],
                               height=0.15,
                               color='black',
                               wrapWidth=1.8)
    blank = visual.rect.Rect(window, fillColor=gray)

    time_point = []
    eve = []

    global_t = core.Clock()
    response = []
    stim_count = 0

    start_t = global_t.getTime()
    time_point.append(start_t)
    eve.append('Start')

    for block in stimulus_blocks:

        clock = core.Clock()
        present_stimulus = -1

        while True:
            if 'escape' in event.getKeys(['escape']):
                time_point.append(global_t.getTime())
                eve.append('escaped')
                task = f'par_{task}'
                log_filename = save_log(time_point, eve, task, sub_num, run_num,
                                        date)
                window.close()
                exit()
            t = clock.getTime()
            current_stimulus = int(t // (block_length_seconds / len(block)))
            if current_stimulus >= len(block):
                window.flip()
                break
            
            if present_stimulus < current_stimulus:
                
                present_stimulus = current_stimulus
                
                time_point.append(global_t.getTime())
                eve.append('blank')
                blank.draw()
                window.flip()
                core.wait(.1)

                if response:
                    time_point.append(response[0][1])
                    eve.append(response[0][0])

                response = event.getKeys(['y'], timeStamped=global_t)

                time_point.append(global_t.getTime())
                eve.append(stim_names[stim_count])
                stim_container.setImage(block[current_stimulus])
                stim_container.draw()        
                window.flip()

                stim_count += 1

        # break
        time_point.append(global_t.getTime())
        eve.append('fix')
        fixation.draw()
        window.flip()
        while True:
            if 'escape' in event.getKeys(['escape']):
                time_point.append(global_t.getTime())
                eve.append('escaped')
                task = f'par_{task}'
                log_filename = save_log(time_point, eve, task, sub_num, run_num,
                                        date)
                window.close()
                exit()
            t2 = clock.getTime()
            if t2 - t >= pause_length_seconds:
                break
    
    time_point.append(global_t.getTime())
    eve.append('End')
    log_filename = save_log(time_point, eve, task, sub_num, run_num, date)
    return log_filename


def calculate_accuracy(log_filename):
    data = pandas.read_csv(log_filename)

    stimuli_resp = data.loc[~data.event.isin(['blank', 'fix', 'Start', 'End'])]
    stimuli = data.loc[~data.event.isin(['blank', 'fix', 'Start', 'End', 'y'])]
    n_trials = len(stimuli)

    probes = stimuli_resp['event'].duplicated(keep='first')
    resp = stimuli_resp['event']=='y'

    probes_resp = stimuli_resp[probes | resp]
    events = list(probes_resp.event)
    times = list(probes_resp.t)

    if 'y' not in events:
        accuracy = 'No responses registered'
    else:
        verdict = []
        counter = 0
        while counter < len(events):
            if events[counter].split(sep)[0] == 'color_stimuli' and counter == len(events)-1:
                verdict.append('fn')
                break
            elif events[counter] == 'y':
                verdict.append('fp')
                counter = counter + 1
            elif events[counter].split(sep)[0] == 'color_stimuli' and events[counter+1] == 'y':
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
        counts = pandas.Series(verdict).value_counts()

        for verdict in ['tp','fn','fp']:
            if verdict not in list(counts.index):
                counts[verdict] = 0

        tp = counts.tp; fn = counts.fn; fp = counts.fp
        tn = n_trials - sum_tp_fp_fn
        assert tp + fp + fn + tn == n_trials
        accuracy = ((tp + tn)/n_trials)*100
        accuracy = round(accuracy, 2)

    return accuracy

def show_end_window(window, text, expected_key):
    textbox = visual.TextStim(window, text, color='white')
    textbox.draw()
    window.flip()

    event.clearEvents()
    while True:
        keys = event.getKeys([expected_key])
        if expected_key in keys:
            window.close()
            return True


if __name__ == "__main__":

    while True:
        try:
            sub_num = int(input("Enter subject number: "))
            run_num = int(input("Enter initial run number (1-4): "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        else:
            break

    window = visual.Window(fullscr=True, size=(1920, 1080), color=(-1, -1, -1), screen=1)
    show_init_screen(window, color='white',
     text=("Le protocole de couleur sera présenté maintenant"
     "\nAppuyez sur << espace >> pour commencer."), wait_key="space")
    window.close()

    for run in range(run_num, 5):
        s = make_stim_sequence_random(num_blocks=36, stim_per_block=12,
                            probe_proportion=0.08,
                            seq_fname=opj('stim_seq',f'stim_sequence_run-{run}.csv'),
                            random_state=run-1)
        all_stimuli, stim_names = load_stim_sequence(stim_sequence_file=opj('stim_seq',
                                f'stim_sequence_run-{run}.csv'))
        all_stimuli = all_stimuli / 256.

        gray = all_stimuli[0, 0, 0, 0] * 2 - 1.

        window = visual.Window(fullscr=True, color=gray, size=(1920, 1080), screen=1)

        show_init_screen(window, text='+', wait_key="t")

        log_file = present_stimulus_blocks(window, all_stimuli, stim_names,
                    sub_num, run)
        
        if log_file.split('_')[0] == 'par':
            continue
        else:
            accuracy = calculate_accuracy(log_file)

        show_end_window(window, text=f'Accuracy = {accuracy}%\nFINI',
                        expected_key='space')

        window.close()
