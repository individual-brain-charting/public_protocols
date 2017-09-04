# -*- coding: utf-8 -*-

import numpy as np


def select_probetype(nsentence_cond, cond_names, dataframe, word_present,
                     word_absent):
    """
    Selection of type of probe, i.e., word_present or word_absent
    The probe scattering is the following:
    b = 0, 2, 4: for #nb_sentence_cond = [0;nb_sentence_cond/2 - 1]
    --> probe = 'word_present'
    for #nb_sentence_cond = [nb_sentence_cond/2;nb_sentence_cond - 1]
    --> probe = 'word_absent'

    b = 1, 3, 5: for #nb_sentence_cond = [0;nb_sentence_cond/2 - 1]
    --> probe = 'word_absent'
    for #nb_sentence_cond = [nb_sentence_cond/2;nb_sentence_cond - 1]
    --> probe = 'word_present'
    """
    ids_subsets = np.split(np.arange(nsentence_cond * len(cond_names)),
                           len(cond_names) * 2)
    pname_allblocks = []
    pword_allblocks = []
    # For all blocks in the block list...
    for bl in np.arange(len(dataframe)):
        pname_block = []
        pword_block = []
        for ldx in np.arange(len(dataframe[bl])):
            # Block with even index
            if bl % 2 == 0:
                # Generate probe stimulus
                if np.any(np.equal([ldx], ids_subsets[::2])):
                    pname = dataframe[bl].columns[word_present]
                    pword = dataframe[bl].values[ldx][word_present]
                else:
                    pname = dataframe[bl].columns[word_absent]
                    pword = dataframe[bl].values[ldx][word_absent]
            # Block with odd index
            else:
                if np.any(np.equal([ldx], ids_subsets[::2])):
                    pname = dataframe[bl].columns[word_absent]
                    pword = dataframe[bl].values[ldx][word_absent]
                else:
                    pname = dataframe[bl].columns[word_present]
                    pword = dataframe[bl].values[ldx][word_present]
            pname_block.append(pname)
            pword_block.append(pword)
        pname_allblocks.append(pname_block)
        pword_allblocks.append(pword_block)
    return pname_allblocks, pword_allblocks
