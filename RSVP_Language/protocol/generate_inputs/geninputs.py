#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# Script to parse the condition files for the Language protocol of
# the IBC project
#
# Author: Ana Luísa Pinho
# Contributors: Elvis Dohmatob, Mehdi Rahim
#
# email: ana.pinho@inria.fr
# =============================================================================

import os
import glob
import random
import numpy as np
import pandas as pd

import dirfiles
from confparser import load_config
from inputparser import offset_parser
from probeselect import select_probetype

# %%
# ====================== LOAD THE CONFIG.INI FILE =============================

# .ini file for main session
setting = load_config("configparser_main_session.ini")

# .ini file for training session
# setting = load_config("configparser_ts.ini")

# %%
# ========= Read csv files containing the inputs for each condition ===========

# Define the pathway of the inputs directory
inputs_path = os.path.abspath(setting["stim_dir"])

# Define the pathway of the directory containing the conditions
conditions_path = os.path.join(inputs_path, setting["condin_subdir"])

# List input csv files
cond_filenames = dirfiles.listdir_csvnohidden(conditions_path)

# Sort input csv files
cond_filenames_dict = dirfiles.abspath_dict(cond_filenames)
cond_filenames_sorted = [cond_filenames_dict[k]
                         for k in setting["condition_names"]]

# Generate a list of dataframes containing the inputs per condition
df_list = [pd.read_csv(cond_filename)
           for cond_filename in cond_filenames_sorted]

# List of the headers' names
headers_list = df_list[0].columns.values.tolist()

# %%
# ================== Parse of the conditions per block ========================

# List of lists containing the inputs sorted by type of condition
cond_list_original = [df_list[dfl].values.tolist()
                      for dfl in np.arange(len(setting["condition_names"]))]

# Shuffles the entries of each list; the shuffling is performed using the
# same order for all lists in order to keep the match of sentences' pairs
# between lists (this is done in order to avoid having mostly the same
# syntactic subtype per session)
indices = random.sample(range(len(cond_list_original[0])),
                        len(cond_list_original[0]))
cond_list = [map(cond_list_original[itm].__getitem__, indices)
             for itm in np.arange(len(cond_list_original))]

# Parse the input files
session_list = offset_parser(setting["offset"], setting["condition_names"],
                             setting["nb_block"], setting["nb_sentence_cond"],
                             cond_list)

# Generate a list of dataframes containing the inputs per session
df_sessionlist = [pd.DataFrame(session_list[dfs], columns=headers_list)
                  for dfs in np.arange(setting["nb_block"])]


# %%
# ====== Create blocks, trials and stimuli within trials for the blocks =======

# Probe assignment to the trial
probe_type, probe_word = select_probetype(setting["nb_sentence_cond"],
                                          setting["condition_names"],
                                          df_sessionlist,
                                          setting["word_present"],
                                          setting["word_absent"])

# Delete the two last columns containing both types of probe
df_new_sessionlist = [df_sessionlist[dlt].drop(["word_present", "word_absent"],
                                               axis=1)
                      for dlt in np.arange(setting["nb_block"])]

# Introduce probe_type and probe_word column
for ins in np.arange(setting["nb_block"]):
    df_new_sessionlist[ins].insert(len(setting["var_names"]),
                                   'probe_type', probe_type[ins])
    df_new_sessionlist[ins].insert(len(setting["var_names"]) + 1 +
                                   setting["sentence_len"],
                                   'probe_word', probe_word[ins])

# Shuffle the rows of the data frame
df_shuffled = [df_new_sessionlist[sh].reindex(np.random.permutation(
                                              df_new_sessionlist[sh].index))
               for sh in np.arange(setting["nb_block"])]

# Creates directory of the files containing the sentences ordered by category
if not os.path.exists(setting['grouped_inputs_dir']):
    os.makedirs(setting['grouped_inputs_dir'])
else:
    filelist = glob.glob(setting['grouped_inputs_dir'] + "/" + "*.csv")
    for f in filelist:
        os.remove(f)

# Create csv files with the sentences ordered by category (condition)
dirfiles.dflist_csvwrite(setting["grouped_inputs_dir"],
                         setting["cond_file"], df_new_sessionlist,
                         setting["idx_title"])

# Print in the terminal the generation of the condition files
print "Files 'conditions*' created."

# Creates directory of the input files for the protocol
if not os.path.exists(setting['inputs_dir']):
    os.makedirs(setting['inputs_dir'])
else:
    filelist = glob.glob(setting['inputs_dir'] + "/" + "*.csv")
    for f in filelist:
        os.remove(f)

# Create csv files with the inputs for Expyriment
dirfiles.dflist_csvwrite(setting["inputs_dir"],
                         setting["inputs_file"], df_shuffled,
                         setting["idx_title"])

# Print in the terminal the generation of the input files
print "Files 'inputs*' created."
