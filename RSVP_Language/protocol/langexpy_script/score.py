# -*- coding: utf-8 -*-

import numpy as np


def calc_score(probe_type_list, pt_fdbk_list, key_present, key_absent):
    """
    Calculate the final score of the participant based on the number of
    correct answers.
    """
    probe_type = np.array(probe_type_list)
    pt_fdbk = np.array(pt_fdbk_list)
    correct_answer = np.where(probe_type == 'word_present', key_present,
                              key_absent)
    score_list = np.where(pt_fdbk == correct_answer, 1, 0)
    score_list = [float(i) for i in score_list]
    score = np.sum(score_list)
    total_score = '{0:.2f}'.format((score / len(probe_type) * 100))
    return total_score
