# -*- coding: utf-8 -*-
"""
Script for randomly separate all the auditory stim of this protocol into
4 sets of 72 stimuli, with 12 of each category per set

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import os
from random import shuffle
import shutil

# %% PARAMETERS
                
categories = {'animal': [], 'music': [], 'nature': [],
              'speech': [], 'tools': [], 'voice': []}

output_sets = {'set1': [], 'set2': [], 'set3': [], 'set4': []}

files_per_category = 48

number_of_categories = len(categories.keys())
number_of_sets = len(output_sets.keys())

cat_files_per_set = int(files_per_category / number_of_sets)

# %% PATHS

my_path = os.getcwd()

input_path = os.path.join(my_path, 'all')


# %% SCRIPT

# Fill the dict of lists with the files filenames
for cat in categories.keys():
    
    for i in range(files_per_category):
        
        title = "s2_" + cat + "_" + str(i + 1) + ".wav"
        
        categories[cat].append(title)
        
# Divide files into the sets
for cat in categories.keys():
    
    shuffle(categories[cat])
    
    chunks = [categories[cat][x: x + cat_files_per_set] \
              for x in range(0, len(categories[cat]), cat_files_per_set)]
    
    chunk_index = 0
    
    for set_ in output_sets.keys():
        
        for item in chunks[chunk_index]:
        
            output_sets[set_].append(item)
            
        chunk_index += 1
        
# Copy the files to their folders
for set_ in output_sets.keys():
    
    output_path = os.path.join(my_path, set_)
    
    old_files = os.listdir(output_path)
    
    # Remove old files from set folders
    for file_name in old_files:
    
        os.remove(output_path + '/' + file_name)
        
    # Copy from 'all' dir to each directory
    for item in range(len(output_sets[set_])):
        
        item_in_path = os.path.join(input_path, output_sets[set_][item])
        item_out_path = os.path.join(output_path, output_sets[set_][item])
    
        shutil.copyfile(item_in_path, item_out_path)
        
        
