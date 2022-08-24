import pandas as pd
import numpy as np
import os


def take_input():
    while True:
        try:
            sub_num = int(input("Enter subject number: "))
        except ValueError:
            print("Invalid input. Expecting integers.")
            continue
        else:
            break

    return sub_num


def setup_io_files(sub_num):
    path = os.getcwd()
    data_dir = os.path.join(path, 'Log')
    data_files = sorted(os.listdir(data_dir))
    out_dir = os.path.join(path, 'output_paradigm_descriptors')
    try:
        os.mkdir(out_dir)
    except OSError:
        pass
    out_files = sorted(os.listdir(out_dir))
    main = []
    infos = []
    for file in data_files:
        if file.split('.')[1] == 'log':
            file_info = file.split('-')
            file_sub = int(file_info[0])
            file_task = file_info[1].split('_')
            
            if file_task[-1] == 'post':
                file_task = file_task[1]
                file_run = int(file_info[2][-1])
            else:
                file_run = int(file_task[1][-1])
                file_task = file_task[0]

            if file_sub == sub_num:
                main.append(file)
                infos.append((sub_num, file_task, file_run))

    return data_dir, main, infos, out_dir, out_files
    

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


def extract_desc(info, file, data_dir, out_files, out_dir):

    file_path = os.path.join(data_dir, file)
    data = pd.read_csv(file_path, sep='\t', skiprows=3)
    data['Time'] = data['Time']/10
    if len(data) == 0:
        print('Data file empty - {}'.format(file))
        return 0
    else:

        sub = info[0]
        task = info[1]
        run = info[2]

        if task == 'piopfaces':
            data = data[['Event Type', 'Code', 'Time']]
            stim = data.loc[data['Event Type'].isin(['Video'])]
            iti = data.loc[data['Code'].isin(['ITI'])]

            video_info = data.drop(index=list(iti.index) + list(stim.index))
            video_info = video_info.loc[video_info['Event Type'].isin(['Manual'])]
            video_info['Code'] =  video_info.Code.str.split('.').str[0]
            video_info['emo'] = video_info.Code.str.split(pat=r'\d+').str[0]
            video_info['demo'] = video_info.Code.str.split(pat=r'\D+').str[1].astype(int)

            video_info['emo'] = np.select([video_info.emo == 'P', video_info.emo == 'C',video_info.emo == 'A', video_info.emo == 'J'], ['pride','contempt','anger','joy'], default='neutral')

            video_info['sex'] = np.where(video_info.demo>8, 'male', 'female')

            video_info['eth'] = np.where(video_info.demo.isin([1,2,3,4,9,10,11,12]), 'european', 'mediterranean')
            video_info['event'] = video_info['emo']+'_'+video_info['sex']+'_'+video_info['eth']

            stim['Code'] = list(video_info.event)

            rel_data = pd.concat([stim, iti])
            rel_data = rel_data.sort_index()
            rel_data = rel_data.reset_index().drop(columns=['index'])
            rel_data['Time'] = rel_data['Time']/1000
            end_time = data['Time'][122]/1000 - rel_data['Time'][0]
            rel_data['Time'] = rel_data['Time'] - rel_data['Time'][0]
            
            rel_data['duration'] = rel_data['Time'].shift(-1, fill_value=end_time)-rel_data['Time']
            rel_data = rel_data.round(2)

            rel_data = rel_data.drop(columns=['Event Type'])
            rel_data = rel_data.rename(columns={'Time': 'onset', 'Code': 'trial_type'})
            rel_data = rel_data[['onset', 'duration', 'trial_type']]
            data = rel_data

        elif task == 'piopgstroop':
            data = data[['Event Type', 'Code', 'Time']]
            ttl_index = data.loc[data['Event Type'].isin(['Pulse'])].head(1).index[0]
            data = data.drop(index=[* range(0,ttl_index)])
            data['Event Type'][ttl_index] = 'ttl'

            iti = data.loc[data['Code'].isin([99])]
            response = data.loc[data['Code'].isin([2,3])]
            ttl = data.loc[data['Event Type'].isin(['ttl'])]
            stim = data.loc[~data['Code'].isin([255,99,2,3])]

            iti['trial_type'] = 'iti'
            ttl['trial_type'] = 'ttl'
            response['trial_type'] = np.where(response.Code==2, 'index_response', 'middle_response')
            stim['face'] = np.where(stim.Code%100<13, 'face_female', 'face_male')
            stim['word'] = np.where(round(stim.Code/100)<5, 'word_female', 'word_male')
            stim['cong'] = np.where(((round(stim.Code/100)<5) & (stim.Code%100<13)) | ((round(stim.Code/100)>4) & (stim.Code%100>12)), 'congruent', 'incongruent')
            
            response_check = pd.concat([stim, response])
            response_check = response_check[['Time', 'face', 'trial_type']]
            response_check.sort_values(by='Time', inplace=True)
            response_check['check'] = response_check['face'].combine_first(response_check['trial_type'])
            check = []
            seq = list(response_check['check'])
            for i in range(len(seq)):
                if seq[i] not in ['face_female', 'face_male']:
                    continue
                elif i == len(seq)-1:
                    check.append('incorrect')
                elif seq[i] == 'face_female' and seq[i+1] == 'middle_response':
                    check.append('correct')
                elif seq[i] == 'face_male' and seq[i+1] == 'index_response':
                    check.append('correct')
                else:
                    check.append('incorrect')
            stim['check'] = check

            stim['trial_type'] = stim.check + '_' + stim.cong + '_' + stim.word + '_' + stim.face
            stim = stim.drop(columns=['face', 'word', 'cong', 'check'])

            rel_data = pd.concat([ttl,iti,response,stim])
            rel_data = rel_data.sort_index()
            rel_data = rel_data.reset_index().drop(columns=['index'])
            rel_data['Time'] = rel_data['Time']/1000
            rel_data['Time'] = rel_data['Time'] - rel_data['Time'][0]
            rel_data['duration'] = rel_data['Time'].shift(-1, fill_value=int(rel_data['Time'].tail(1))+4)-rel_data['Time']
            rel_data = rel_data.round(2)
            rel_data = rel_data.drop(columns=['Event Type', 'Code'])
            rel_data = rel_data.rename(columns={'Time': 'onset'})
            rel_data = rel_data[['onset', 'duration', 'trial_type']]
            data = rel_data

        elif task == 'piopharriri':
            data = data[['Event Type', 'Code', 'Time']]
            ttl_index = data.loc[data['Event Type'].isin(['Pulse'])].head(1).index[0]
            data = data.drop(index=[* range(0,ttl_index)])
            data['Event Type'][ttl_index] = 'ttl'
            data = data.loc[~data['Event Type'].isin(['Pulse'])]
            data = data.reset_index().drop(columns=['index'])

            data['trial_type'] = np.select([data.Code == 255, data.Code > 50, (data.Code < 50) & (data.Code > 10), data.Code == 3], ['ttl','shape','emotion','middle_response'], default='index_response')

            data = data.drop(columns=['Event Type', 'Code'])

            data['Time'] = data['Time']/1000
            data['Time'] = data['Time'] - data['Time'][0]
            data['duration'] = data['Time'].shift(-1, fill_value=int(data['Time'].tail(1))+4)-data['Time']
            
            data = data.rename(columns={'Time': 'onset'})
            data = data.round(2)
            data = data[['onset', 'duration', 'trial_type']]

        elif task == 'piopworkingmemory':
            if sub == 64:
                aux_file = str(sub)+'piop_workingmemory_run'+str(run)+'_log.txt'
                aux_file_path = os.path.join(data_dir, aux_file)
                aux_data = pd.read_csv(aux_file_path, sep='\t', names=['trial', 'trial_type', 'duration', 'response'])
                aux_data = aux_data.drop(columns=['trial'])
                aux_data['response'] = np.select([aux_data['response'] == 2, aux_data['response'] == 3, aux_data['response'] == 0], ['index_response','middle_response', np.nan])
                aux_data.duration = aux_data.duration.astype(int)
                aux_data['duration'] = np.where(aux_data.trial_type>0, 6, aux_data.duration)

                data = data[['Event Type', 'Code', 'Time']]
                ttl_index = data.loc[data['Event Type'].isin(['Pulse'])].head(1).index[0]
                data = data.drop(index=[* range(0,ttl_index)])
                data['Event Type'][ttl_index] = 'ttl'
                data = data.loc[~data['Event Type'].isin(['Pulse', 'Picture'])]
                data = data.reset_index().drop(columns=['index'])
                init_time = data['Time'][0]

                aux_data['onset'] = (aux_data['duration']*1000).shift(1, fill_value=init_time)
                aux_data['onset'] = aux_data['onset'].cumsum()
                aux_data['onset_corr'] = aux_data['onset'] + 22 + 25
                aux_data['trial_type'] = np.select([aux_data.trial_type == 1, aux_data.trial_type == 2,aux_data.trial_type == 3], ['active_no_change','active_change','passive'], default='null')

                resp = data.loc[data['Event Type'].isin(['Response'])]
                resp = resp.drop(columns=['Event Type'])
                resp = resp.rename(columns={'Time': 'onset', 'Code':'trial_type'})
                resp['onset_corr'] = resp['onset']
                resp['trial_type'] = np.where(resp['trial_type']==2, 'index_response', 'middle_response')

                rel_data = pd.concat([aux_data, resp])
                rel_data = rel_data.sort_values('onset')
                rel_data['onset'] = rel_data['onset_corr']
                rel_data = rel_data.drop(columns=['response','onset_corr'])
                rel_data = rel_data[['onset', 'duration', 'trial_type']]
                init_time = rel_data['onset'][0]
                rel_data.onset = rel_data.onset - init_time
                rel_data.onset = rel_data.onset/1000
                rel_data = rel_data.round(2)
                
                data = rel_data
            
            else:
                aux_file = str(sub)+'piop_workingmemory_run'+str(run)+'_log.txt'
                aux_file_path = os.path.join(data_dir, aux_file)
                aux_data = pd.read_csv(aux_file_path, sep='\t', names=['trial', 'trial_type', 'duration', 'response'])
                aux_data = aux_data.drop(columns=['trial'])
                aux_data.duration = aux_data.duration.astype(int)
                aux_data['duration'] = np.where(aux_data.trial_type>0, 6, aux_data.duration)

                data = data[['Event Type', 'Code', 'Time']]
                stim = data.loc[data['Code'].isin([0, 10])]
                stim = stim.iloc[1:]
                resp = data.loc[data['Code'].isin([2, 3])]
                resp = resp.iloc[1:]

                aux_data['temp_ind'] = stim.index
                aux_data.set_index('temp_ind', inplace=True)
                stim['Code'] = aux_data['trial_type']
                stim['Code'] = np.select([stim.Code == 1, stim.Code == 2,stim.Code == 3], ['active_no_change','active_change','passive'], default='null')
                resp['Code'] = np.where(resp.Code==2, 'index_response', 'middle_response')

                rel_data = pd.concat([resp, stim])
                rel_data.drop(columns=['Event Type'], inplace=True)
                rel_data.rename(columns={'Time': 'onset', 'Code':'trial_type'}, inplace=True)
                rel_data = rel_data.sort_values('onset')
                rel_data['duration'] = rel_data['onset'].shift(-1,fill_value=float(rel_data['onset'].tail(1)+8000))-rel_data['onset']
                init_time = float(rel_data.head(1)['onset'])
                rel_data.onset = rel_data.onset - init_time
                # rel_data.drop(index=rel_data.tail(1).index, inplace=True)

                rel_data.onset = rel_data.onset/1000
                rel_data.duration = rel_data.duration/1000
                rel_data = rel_data[['onset', 'duration', 'trial_type']]

                rel_data = rel_data.round(2)

                data = rel_data

        save_as = f'task-{task}_sub-{sub:02d}_run-{run:02d}_events.tsv'

        save_as = check_presence(save_as, out_files)
        save_as = os.path.join(out_dir, save_as)
        data.to_csv(save_as, index=False, sep='\t')

    print('Event file created for {}, {}, run {}'.format(sub, task, run))
    return 1


if __name__ == "__main__":

    sub_num = take_input()
    data_dir, main, infos, out_dir, out_files = setup_io_files(sub_num)
    
    if len(main) == 0:
        print("Can't find data for subject {}".format(sub_num))
        quit()
    else:
        for file, info in zip(main, infos):
            extract_desc(info, file, data_dir, out_files, out_dir)
