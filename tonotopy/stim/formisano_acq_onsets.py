#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script used on our version of the experiment used by Santoro et al. (2017) to 
generate the list of onsets for the interrupter fMRI acquisitions

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import os
import numpy as np
import pandas as pd

my_path = os.getcwd()
output_path = os.path.join(my_path, 'interrupted_acq_onsets')

# Number of runs (blocks)
nb_block = 6

# Duration of the TR
tr_dur = 2000

# Initial fixcross duration
fix_dur = 2000

# Same code that there is in the original protocol for generating the ISI
random_isi = []
stack = np.hstack((np.repeat(3, 40), np.repeat(2, 22), np.repeat(4, 20)))

for run in range(nb_block):
    np.random.seed(run * 10 + run)
    random_stack = np.random.permutation(stack)
    random_isi.append(random_stack)
    
for run in range(len(random_isi)):
    
    onset_list = [fix_dur]
    
    for index in range(len(random_isi[run])):
        
        next_onset = onset_list[index] + (random_isi[run][index] * tr_dur) + tr_dur
        
        onset_list.append(next_onset)
        
    onset_df = pd.DataFrame(onset_list, columns = ['onset'])
    
    onset_df.to_csv(os.path.join(output_path,
                                 'onsets_run' + str(run + 1)), index = False)
    