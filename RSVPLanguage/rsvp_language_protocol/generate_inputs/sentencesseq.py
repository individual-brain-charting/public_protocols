# -*- coding: utf-8 -*-

import numpy as np


def sentences_seq(nblock, nsentence_cond, cnames, condseq):
    """
    Generates the sequence of sentences per block for all blocks

    Note: Although the sequence of the conditions per block is fixed
          the selection of the sentences with
          probe = ('word_present' | 'word_absent') within condition is
          randomized with no repetition
    """
    sseq = []
    for nbl in np.arange(nblock):
        # Generate list of indices
        cond_probe = []
        # Each sublist corresponds to a specific condition
        # with probe = ('word_present' | 'word_absent')
        cond_probe_idx = np.split(np.arange(nsentence_cond *
                                            len(cnames)),
                                  len(cnames) * 2)
        # Regroup sublists in pairs by type of condition
        for cp in np.arange(0, len(cnames) * 2 - 1, 2):
            cond_probe_together = np.vstack((cond_probe_idx[cp],
                                            cond_probe_idx[cp + 1]))
            cond_probe_together = cond_probe_together.tolist()
            cond_probe.append(cond_probe_together)
        sentences = []
        # For each pre-specified block sequence,
        for cs in condseq[nbl]:
            # for a blocks with even index,
            if nbl % 2 == 0:
                # Random selection of sentences indices for condition cs[0]
                # with probe = 'word_present', i.e. cs[1] = 1
                if cs[1] == 1:
                    new_sentence_idx = np.random.choice(cond_probe[cs[0]][0])
                    sentences.append(new_sentence_idx)
                    cond_probe = [[[entry for entry in subarr
                                   if entry != new_sentence_idx]
                                  for subarr in arr] for arr in cond_probe]
                # Random selection of sentences indices for condition cs[0]
                # with probe = 'word_absent', i.e. cs[1] = 0
                else:
                    new_sentence_idx = np.random.choice(cond_probe[cs[0]][1])
                    sentences.append(new_sentence_idx)
                    cond_probe = [[[entry for entry in subarr
                                   if entry != new_sentence_idx]
                                  for subarr in arr] for arr in cond_probe]
            # for a block with odd index,
            else:
                # Random selection of sentences indices for condition cs[0]
                # with probe = 'word_absent', i.e. cs[1] = 0
                if cs[1] == 0:
                    new_sentence_idx = np.random.choice(cond_probe[cs[0]][0])
                    sentences.append(new_sentence_idx)
                    cond_probe = [[[entry for entry in subarr
                                   if entry != new_sentence_idx]
                                  for subarr in arr] for arr in cond_probe]
                # Random selection of sentences indices for condition cs[0]
                # with probe = 'word_present', i.e. cs[1] = 1
                else:
                    new_sentence_idx = np.random.choice(cond_probe[cs[0]][1])
                    sentences.append(new_sentence_idx)
                    cond_probe = [[[entry for entry in subarr
                                   if entry != new_sentence_idx]
                                  for subarr in arr] for arr in cond_probe]
        sseq.append(sentences)
    return sseq
