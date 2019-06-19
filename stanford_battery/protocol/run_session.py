import json
import os
import subprocess
import time

subid = raw_input('Enter subject id (i.e. s999): ')
training = raw_input('Enter 0 for training, 1 for main tasks: ')

if training == '1':
    run_file = 'scanner_tasks_order1'
else:
    run_file = 'practice_tasks'

taskset = raw_input('Enter task group (1, 2 or 3): ')

if taskset == '1':
    tasks = ['stop_signal','attention_network_task','twobytwo']
elif taskset == '2':
    tasks = ['motor_selective_stop_signal', 'stroop', 'discount_fixed']
elif taskset == '3':
    tasks = ['dot_pattern_expectancy', 'columbia_card_task_hot',
             'ward_and_allport']

else:
    raise ValueError('Invalid session number')

print('\n'.join(tasks))
json.dump(tasks, open('temp_tasklist.json','w'))

for task in tasks:
    print('***************************************************************')
    if os.name == 'posix':
        subprocess.call("expfactory --run --folder {0} --battery expfactory-battery/ "
                        "--experiments {1} --subid {2} &".format(run_file, task, subid), shell=True)
    else:
        subprocess.call("start expfactory --run --folder {0} --battery expfactory-battery/ "
                        "--experiments {1} --subid {2}".format(run_file, task, subid), shell=True)
    time.sleep(1)
