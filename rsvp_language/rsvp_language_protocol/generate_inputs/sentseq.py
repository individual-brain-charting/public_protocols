# -*- coding: utf-8 -*-

# =============================================================================
# Inputs sequence for the IBC language protocol:
# create a random sequence of sentences per block for all blocks according to
# a pre-specified order of condition and probe type
#
# Author: Ana Luísa Pinho
#
# email: ana.pinho@inria.fr
# =============================================================================

import os
import numpy as np
import pandas as pd

import dirfiles
from confparser import load_config
from sentencesseq import sentences_seq

# %%
# ====================== LOAD THE CONFIG.INI FILE =============================

# .ini file for main session
setting = load_config("configparser_main_session.ini")

# .ini file for training session
# setting = load_config("configparser_ts.ini")

# %%
# =========================== MAIN SCRIPT =====================================

# Define the pathway of the inputs directory
inputs_path = os.path.abspath(setting["stim_dir"])

# Define the pathway of the directory containing the conditions' sequence
conditions_seq_path = os.path.join(inputs_path, setting["condseqin_subdir"])

# List the input files
cond_seq_filenames = dirfiles.listdir_csvnohidden(conditions_seq_path)

# Sort input csv files
cond_seq_filenames.sort()

# Read csv files with the conditions' sequences for each block
df_condseq = [pd.read_csv(cond_seq_filename)
              for cond_seq_filename in cond_seq_filenames]
cond_seq = [df_condseq[dfs].values.tolist()
            for dfs in np.arange(setting["nb_block"])]

# Generates the sequence of sentences for each block according to
# the condition's sequence pre-specified in the .csv files
new_order = sentences_seq(setting["nb_block"], setting["nb_sentence_cond"],
                          setting["condition_names"], cond_seq)

df_norder = [pd.DataFrame(new_order[dfn], columns=['sequence'])
             for dfn in np.arange(len(new_order))]

# Define the pathway of the outputs directory
outputs_path = os.path.abspath(setting["order_dir"])

# Create csv files with the sequences of inputs to be introduced in Expyriment
dirfiles.dflist_csvwrite(outputs_path, setting["condseqout_fname"], df_norder,
                         setting["idx_title"])

# Print in the terminal
print "Files 'norder*' created."
