# -*- coding: utf-8 -*-
"""
Parser for e-prime ARCHI localizers log-files

author: Mehdi Rahim
@contributor: Ana Luisa Pinho, ana.pinho@inria.fr

Last update: August 2018

Compatibility: Python 2.7

How to run:
Run this script from the data folder
python <name_of_the_script> <eprime_input.txt> <exp_var_1>
    <exp_var_2> ... <exp_var_n>

python ..\paradigm_descriptors\parser_eprime_logtxt_scene_perception.py scene-perception_sub-53_run1.txt 
Instruction.OffsetTime Fix.OnsetTime Stimulus.OnsetTime Condition Stimulus.ACC Stimulus.RT ITI.OnsetTime ITI 
"""

import os
import sys
import codecs
import chardet
import pandas as pd
import numpy as np


# Quick E-Prime Parser
def parse_data_eprime(filename):
    """ returns a dict of header informations (hdr) and a DataFrame of values
    at the 2rd level (edf)
    """

    edf = pd.DataFrame()  # Dataframe
    lvl = {}    # E-Prime level 2 dict
    hdr = {}  # Header dict
    level_flag = -1  # Flag on the current header/level

    with open(filename, 'rb') as f:
        det = chardet.detect(f.readline())
        # need to unit-test this in scenarios where encoding is 'UTF-16LE"
        if det['encoding'] in ['UTF-16', 'UTF-16LE']:
            encoding = 'utf-16'
        else:
           encoding = 'utf-8'

    print 'File encoding is : ', encoding
    print '________________'

    with codecs.open(filename, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if "header start" in line.lower() or "header end" in line.lower():
                # set the flag on header section
                level_flag = 0
                continue
            if line == "*** LogFrame Start ***":
                # reset the level 2 dict
                lvl = {}
                continue
            if line == "*** LogFrame End ***":
                # append dict according to the dataframe
                if lvl:
                    edf = edf.append(lvl, ignore_index=True)
                level_flag = -1
                continue
            fields = line.split(":")
            fields[0] = fields[0].replace(':', '')
            fields = [field.strip() for field in fields]

            if fields[0] == "Level":
                level_flag = int(fields[1])
                continue
            if level_flag in np.arange(1, 5):
                # if we are at level 2 or 3 : copy data to lvl dict
                lvl[fields[0]] = ''
                if len(fields) == 2:
                    lvl[fields[0]] = fields[1]
                # if we are at upper level : copy data to header
            elif level_flag == 0:
                hdr[fields[0]] = fields[1]
    return edf, hdr


##############################################################################
##############################################################################
# Parsing and saving a session csv for an e-prime file.
##############################################################################
##############################################################################

# General parameters
participant = 51
session = 'screening3'
# session = 'all_ARCHI_loc'
protocol = 'localizer_spatial'
# Subject or pilot?
fname_prefix = 'sub'
# fname_prefix = 'pilot'


# fname must be the path to an eprime txt file (from argv or fixed)
if len(sys.argv) > 1:
    fname = sys.argv[1]
    print '\nInput file : ', fname
    print '________________'

    # Selected columns can be given as input argument
    if len(sys.argv) > 2:
        eprime_selected_cols = sys.argv[2:]
    else:
        # You can provide a list of selected columns
        eprime_selected_cols = None

    print 'Selected columns :  ', eprime_selected_cols
    print '________________'

    # Parse data (df) and header informations (hd)
    df, hd = parse_data_eprime(fname)

    # Checks fields
    print 'Fields read : ', df.keys()

    # Get filename without the extension
    _, output_file = os.path.split(fname)
    output_file, _ = os.path.splitext(output_file)
    # Filename lowercase only
    output_file = output_file.lower()
    # Save file (add extracted_ prefix)
    participant_id = fname_prefix + '-' + '%02d' % participant
    # path_output = os.path.join(participant_id, session, protocol)
    path_output = os.getcwd()
    df.to_csv(path_output + '/extracted_' + output_file + '.csv', sep=',',
              columns=eprime_selected_cols, index=False)

    print '________________'
    print 'Output file : ', 'extracted_' + output_file + '.csv\n'
else:
    print '\nYou must provide at least the eprime filename !'
    print str(''.join(('FORMAT: ipython parse_eprime_file.py',
                       '[FILENAME] {[COL1] [COL2] ...}\n')))
