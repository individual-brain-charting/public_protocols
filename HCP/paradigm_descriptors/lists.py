import numpy as np


def short_list(liste, descript, list_headers):
    """
    Generate a short list of the paradigm descriptors: 
    consecutive active conditions under the same category are merged
    """
    # List previously created, but with no headers
    list_noheaders = liste[1:]
    # Indices with the first onset for the next different condition
    indices = [int(n) for n in np.arange(1, len(list_noheaders))
               if list_noheaders[n][descript.index(list_headers['names'])] !=
               list_noheaders[n - 1][descript.index(list_headers['names'])]]
    # Add first and last indice to the previous list
    indices.insert(0, int(0))
    indices.append(len(list_noheaders))
    # Array containing the names of the conditions for
    # the short-version list
    sh_cond_name = [list_noheaders[k][descript.index(list_headers['names'])]
                    for k in indices[: -1]]
    # Array containing the onsets of the conditions for
    # the short-version list
    sh_cond_onset = [float(list_noheaders[k][descript.index(
                                             list_headers['onsets'])])
                     for k in indices[: -1]]
    # Create the array with the duration for the merged conditions
    # used in the short-version list
    # List of lists containing the duration of each event
    # per type of condition
    e_duration = [[float(list_noheaders[i][descript.index(
                                           list_headers['durations'])])
                  for i in np.arange(indices[j - 1], indices[j])]
                  for j in np.arange(1, len(indices))]
    # Sum of all durations from each sub-list
    sh_cond_duration = [sum(e_duration[k])
                        for k in np.arange(len(e_duration))]
    # Stack the name, onset and duration of the short-version
    # regressors in one single list
    sh_list = np.vstack((descript, np.vstack((sh_cond_onset, sh_cond_duration,
                                              sh_cond_name)).T))
    return sh_list


def four_short_list(liste, descript, list_headers):
    """
    Generate a short list of the paradigm descriptors: 
    four active conditions under the same category are merged into the same 
    block
    """
    # List previously created, but with no headers
    list_noheaders = liste[1:]
    chunk_list = [list_noheaders[i:i+4]
                  for i in np.arange(0, len(list_noheaders), 4)]
    chunk_onset = [float(chunk_list[k][0][descript.index(
                                          list_headers['onsets'])])
                   for k in np.arange(len(chunk_list))]
    chunk_duration = [sum([float(chunk_list[k][j][descript.index(
                                                  list_headers['durations'])])
                      for j in np.arange(len(chunk_list[k]))])
                      for k in np.arange(len(chunk_list))]
    chunk_name = [chunk_list[k][1][descript.index(list_headers['names'])]
                  for k in np.arange(len(chunk_list))]
    four_sh_list = np.vstack((descript, np.vstack((chunk_onset, chunk_duration,
                                                   chunk_name)).T))
    return four_sh_list


def stacker(onset_sec, duration, name, list_headers):
    """
    Stack three arrays in the same list with the headers pre-set
    """
    dict_original = {}
    dict_original['onsets'] = onset_sec
    dict_original['durations'] = duration
    dict_original['names'] = name
    liste = list_headers.keys()
    for ind, (key_original, key_mapped) in enumerate(list_headers.items()):
        if ind == 0:
            liste = np.hstack([key_mapped, dict_original[key_original]])
        else:
            liste = np.vstack([liste, np.hstack([key_mapped,
                                                 dict_original[key_original
                                                               ]])])
    liste = liste.T
    return liste
