# -*- coding: utf-8 -*-

import numpy as np


def offset_parser(offset, condition_names, nb_block, nb_sentence_cond,
                  condition_list):
    """
    Parser of input files with a given offset between first and second input

    Considering,
    b       --> #block
    c       --> #condition
    nb_cond --> total amount of conditions
    offset  --> int > 1
    s(c,b)  --> #set in the condition file of c that will be extracted for b

    For b block with (nb_sentence_cond * nb_cond) inputs, the set s(c,b) of
    nb_cond_sentence inputs from condition_list[c],
    in which c = [0;nb_cond - 1],
    is defined as follows:
    c = 0: s(c,b) = s(1,b) = b
    c = 1: s(c,b) = s(2,b) = (b + offset) mod nb_cond
    c > 1 & (c != nb_cond - 1): s(c,b) = (b + offset + c - 1) mod nb_cond
    c = nb_cond - 1: s(c,b) = (b + offset + c) mod nb_cond
    """
    sess_list = []
    cond_ids = np.arange((offset % len(condition_names)) - 1,
                         len(condition_names) +
                         (offset % len(condition_names)) - 1)

    cond_order = np.remainder(cond_ids, len(condition_names) - 1)
    if nb_block > len(condition_names):
        for j in np.arange(nb_block - len(condition_names)):
            cond_order = np.append(cond_order, cond_order[j % cond_order.size])
    else:
        pass
    for s in np.arange(nb_block):
        # Firstly, create the indices of the first two conditions
        # condition1 : sublist of 10 elements
        condition_1_ids_start = nb_sentence_cond * \
            (s % len(condition_names))
        condition_1_ids_end = condition_1_ids_start + nb_sentence_cond
        # condition2 : sublist of 10 elements with offset
        condition_2_ids_start = (condition_1_ids_start +
                                 (offset %
                                  len(condition_names)) *
                                 nb_sentence_cond) % \
            (nb_sentence_cond * len(condition_names))
        condition_2_ids_end = condition_2_ids_start + nb_sentence_cond

        # Fill the session with the two sublists of cond1 and cond2
        session = condition_list[0][condition_1_ids_start:condition_1_ids_end] + \
            condition_list[1][condition_2_ids_start:condition_2_ids_end]

        # Then, fill with the sublists of the remaining conditions...
        sequences = np.arange(len(condition_names))
        # ... and remove the already added indices
        added_ids = [s % len(condition_names),
                     (s + offset) % len(condition_names)]
        remaining_seqs = np.delete(sequences, added_ids)

        # Reorder remaining sequences
        remaining_seq_reordered = np.roll(remaining_seqs, -cond_order[s])

        # For each indices of the remaining conditions,
        for k, seq in enumerate(remaining_seq_reordered):
            # add their sublists (10 sentences)
            condition_start = nb_sentence_cond * seq
            condition_end = condition_start + nb_sentence_cond
            session = session + \
                condition_list[k + 2][condition_start:condition_end]

        # Session list contains nb_block lists for the blocks.
        # Each list contains (nb_sentences_cond * number_of_conditions) trials
        # from the available condition files.
        sess_list.append(session)
    return sess_list
