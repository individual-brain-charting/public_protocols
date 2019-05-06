# -*- coding: utf-8 -*-

import numpy as np

def calc_score(answer_list, pt_fdbk_list):
    """
    Calculate the final score of the participant based on the number of
    correct answers.
    """
    answer = np.array(answer_list)
    pt_fdbk = np.array(pt_fdbk_list)
    score_list = np.where(answer == pt_fdbk, 1, 0)
    score_list = [float(i) for i in score_list]
    score = np.sum(score_list)
    total_score = '{0:.2f}'.format((score / len(answer) * 100))
    return total_score
