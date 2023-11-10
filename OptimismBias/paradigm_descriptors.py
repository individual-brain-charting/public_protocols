"""
Event extraction script for optimism bias task.

Author:
Himanshu Aggarwal
himanshu.aggarwal@inria.fr
March 2022
"""

import pandas as pd
import os


def take_input():
    while True:
        try:
            sub_num = int(input("Enter subject number: "))
            design = int(input("Output 1- just the relevant events\n    or 2- all events?: "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        else:
            break

    return sub_num, design


def setup_io_files(sub_num):
    path = os.getcwd()
    data_dir = os.path.join(path, 'log')
    data_files = sorted(os.listdir(data_dir))

    out_dir = os.path.join(path, 'output_paradigm_descriptors')
    try:
        os.mkdir(out_dir)
    except OSError:
        pass
    out_files = sorted(os.listdir(out_dir))

    practice = []
    main = []
    for file in data_files:
        if file.split('_')[0]=='pract':
            if int(file.split('_')[1].split('-')[1]) == sub_num:
                practice.append(file)
        elif file.split('_')[0]=='par':
            continue
        else:
            if int(file.split('_')[1].split('-')[1]) == sub_num:
                main.append(file)
    return data_dir, main, practice, out_dir, out_files


def check_presence(filename, list_of_files):
    if filename in list_of_files:
        count = 0
        for f in list_of_files:
            if f==filename:
                count+=1
        filename = filename.split('.')[0]+'('+str(count)+').'+filename.split('.')[1]
        return check_presence(filename,list_of_files)
    else:
        return filename


def extract_desc(design, file, data_dir, out_files, out_dir):

    file_path = os.path.join(data_dir, file)
    data = pd.read_csv(file_path)
    if len(data) == 0:
        print('Data file empty - {}'.format(file))
        return 0
    else:
        components = file.split('_')

        task = components[0]
        sub = components[1]
        run = components[2]

        data_ed = data.drop(index=[0,140])
        events = list(data_ed.eve)

        rel_eve = []
        decision = []
        i=0
        while i<len(events):
            toe = events[i].split('_')[1]
            if toe=="Passé":
                toe = "past"
            else:
                toe = "future"

            thinking = events[i+1].split('_')[0]
            if thinking=="thinking":
                thinking = True
            else:
                thinking = False

            arousal = events[i+3]
            valence = events[i+5]

            rel_eve.append(f'{toe}_{arousal}_{valence}')

            if thinking:
                if valence=='negative':
                    if arousal=='very' or arousal=='little':
                        decision.append(f'{toe}_negative')
                    else:
                        decision.append('inconclusive')
                elif valence=='positive':
                    if arousal=='very' or arousal=='little':
                        decision.append(f'{toe}_positive')
                    else:
                        decision.append('inconclusive')
                elif valence=='neutral':
                    if arousal=='little' or arousal=='not':
                        decision.append(f'{toe}_neutral')
                    else:
                        decision.append('inconclusive')
                else:
                    decision.append('inconclusive')
            else:
                decision.append('inconclusive')

            i = i + 7

        cnt = 0
        for i, row in data.iterrows():
            if (i-2)%7==0 or i==2:
                data.at[i,'eve'] = decision[cnt]
                cnt = cnt + 1


        data['duration'] = data['t'].shift(-1)-data['t']
        data = data[:-1]
        data = data.rename(columns={'t': 'onset', 'eve': 'trial_type'})
        data = data[['onset', 'duration', 'trial_type']]
        data = data.round(2)

        if design == 1:
            unique_dec = ['future_negative', 'future_neutral',
                         'future_positive', 'inconclusive',
                         'past_negative', 'past_neutral', 'past_positive']
            others = ['fix']
            data = data.loc[data.trial_type.isin(unique_dec+others)].reset_index(drop=True)

        save_as = f'{task}_{sub}_{run}_events.tsv'

        save_as = check_presence(save_as, out_files)
        save_as = os.path.join(out_dir, save_as)
        data.to_csv(save_as, index=False, sep='\t')

    print('Event file created for {}, {}'.format(sub, run))
    return 1


if __name__ == "__main__":

    sub_num, design = take_input()
    data_dir, main, practice, out_dir, out_files = setup_io_files(sub_num)
    
    if len(main) == 0:
        print("Can't find data for subject {}".format(sub_num))
        quit()
    else:
        for file in main:
            extract_desc(design, file, data_dir, out_files, out_dir)
