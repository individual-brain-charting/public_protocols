#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 11:50:26 2017

@author: ian
"""
from glob import glob
import numpy as np
import os
import seaborn

def get_blocks(order):
    blocks = []
    previous_stim = None
    block_len = 0
    for i in order:
        if i != previous_stim and previous_stim != None:
            blocks.append(block_len)
            block_len = 1
        else:
            block_len+=1
        previous_stim = i
    return blocks

for task in ['attention_network_task', 'dot_pattern_expectancy', 
             'motor_selective_stop_signal', 'stop_signal', 'stroop',
             'twobytwo', 'ward_and_allport']:
    design_dirs = glob(os.path.join(task,task+'_designs_*'))
    for design_dir in np.sort(design_dirs):
        if os.path.exists(design_dir):
            block_counts = []
            stim_orders = []
            for directory in np.sort(glob(os.path.join(design_dir,'design*'))):
                stim_onsets = []
                stims = []
                stim_i = 0
                for stim_file in np.sort(glob(os.path.join(directory,'stimulus*'))):
                    stim_onset=list(np.loadtxt(stim_file))
                    stim_onsets+=stim_onset
                    stims+= [stim_i]*len(stim_onset)
                    stim_i+=1
                sort_index = np.argsort(stim_onsets)
                stim_order = [str(stims[i]) for i in sort_index]
                stim_orders.append(stim_order)
                # load ITIs
                ITIs = np.loadtxt(os.path.join(directory,'ITIs.txt'))
                # save number of blocks and print  out order statistics
                blocks = get_blocks(stim_order)
                block_counts.append(blocks)
                print('task: %s, length: %s, ITIs mean: %s' % (task,len(stim_onsets),np.mean(ITIs)))
                # rotate stim orders 4 times
                rotations = np.linspace(0, len(stim_order)*3/4, 4)
                for i,rotation in enumerate(rotations):
                    rolled_stim_order = np.roll(stim_order,int(rotation))
                    # write stim_order
                    stim_order_file = open(os.path.join(directory,'set_%s_stim_order.txt' % i), "w")
                    stim_order_file.write(','.join(map(str,rolled_stim_order)))
                    stim_order_file.close()
                    
                    # write ITI in an easier to copy form
                    rolled_ITI = np.roll(ITIs, int(rotation))
                    ITI_file = open(os.path.join(directory,'set_%s_ITIs.txt' % i), "w")
                    ITI_file.write(','.join(map(str,rolled_ITI)))
                    ITI_file.close()
                    
            
            f = seaborn.plt.figure()
            for i,block in enumerate(block_counts):
                seaborn.plt.subplot(3,2,i+1)
                seaborn.plt.hist(block)
            f.suptitle(task + ' Block Histogram', fontsize = 16)
            f.savefig(os.path.join(design_dir,'task_block_histogram.pdf'))

