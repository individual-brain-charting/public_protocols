import numpy as np
import pandas as pd
import os

while True:
    try:
        sub_num = int(input("Enter subject number: "))
    except ValueError:
        print("Invalid subject number. Expecting an integer.")
        #better try again... Return to the start of the loop
        continue
    else:
        #age was successfully parsed!
        #we're ready to exit the loop.
        break

path = os.getcwd()
data_dir = os.path.join(path, 'Outputs')
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
    if file == 'ancillary':
        continue
    elif file.split('_')[0]=='pract':
        if file.split('_')[1].split('-')[1] == str(sub_num):
            practice.append(file)
    else:
        if file.split('_')[0].split('-')[1] == str(sub_num):
            main.append(file)

def check_presence(filename,list_of_files):
    if filename in list_of_files:
        count = 0
        for f in list_of_files:
            if f==filename:
                count+=1
        filename = filename.split('.')[0]+'('+str(count)+').'+filename.split('.')[1]
        return check_presence(filename,list_of_files)
    else:
        return filename


def extract_desc(files):
    if len(files) == 0:
        print("Can't find data for subject {}".format(sub_num))
        quit()
    for file in files:
        file_path = os.path.join(data_dir, file)
        data = pd.read_csv(file_path,sep='\t')
        if len(data.index) == 0:
            print('Data file empty - {}'.format(file))
        else:
            components = file.split('.')[0].split('_')
            task = 'narps'
            subj = '%02d' %int(components[0].split('-')[-1])
            run = '%02d' %int(components[2].split('-')[-1])

            cross_on = np.array(data.TrialStart) + 4.

            stim_on = np.array(data.TrialStart)

            blank_on = np.array(data.TrialStart) + np.array(data.RT)

            df = pd.DataFrame({'stim':stim_on,'blank':blank_on,'fix':cross_on})
            df = df.stack().reset_index()
            df = df.drop(columns=['level_0'])
            df.columns = ['trial_type','onset']
            df['duration'] = df['onset'].shift(-1,fill_value=list(df['onset'])[-2]+4)-df['onset']

            ids = list(df.loc[df['duration'].eq(0)].index+1)
            df = df.drop(index=ids, errors='ignore')
            # for id in ids:
            #     try:
            #         df.iloc[id] = [np.NaN,np.NaN,np.NaN]
            #     except:
            #         df.append({'trial_type':np.NaN,
            #                 'onset':np.NaN,
            #                 'duration':np.NaN}, ignore_index=True)

            df.drop(df.tail(1).index,inplace=True)
            df.loc[(df['duration'].eq(0) & df['trial_type'].eq('stim')), 'duration'] = 4.
            df = df.round(3)

            gambles = 'stim_+'+ data['WinSum'].astype(str) + '_-' + data['LoseSum'].abs().astype(str)
            responses = data['Response'].astype(str)
            cnt_stim = 0; cnt_resp = 0
            for event in df.index:
                if df.at[event, 'trial_type'] == 'stim':
                    df.at[event, 'trial_type'] = gambles[cnt_stim]
                    cnt_stim+=1
                elif df.at[event, 'trial_type'] == 'blank':
                    df.at[event, 'trial_type'] = responses[cnt_resp]
                    cnt_resp+=1
                else:
                    continue

            df = df[['onset', 'duration', 'trial_type']]
            if file.split('_')[0]=='pract':
                save_as = 'pract_task-{}_sub-{}_run-{}_events.tsv'.format(task,subj,run)
            else:
                save_as = 'task-{}_sub-{}_run-{}_events.tsv'.format(task,subj,run)
            save_as = check_presence(save_as, out_files)
            save_as = os.path.join(out_dir, save_as)
            df.to_csv(save_as,index=False,sep='\t')
        print('Event file created for subject {}, run {}'.format(subj, run))

extract_desc(main)
