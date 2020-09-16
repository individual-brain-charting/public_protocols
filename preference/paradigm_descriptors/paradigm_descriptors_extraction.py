"""
Script for paradigm descriptors' extraction on the rewarding protocol

author: Ana Luisa Pinho
e-mail: ana.pinho@inria.fr
"""

import os
import csv
import numpy as np

# %%
# ========================== GENERAL PARAMETERS ===============================
# List of participants id
participant_list = [8]

# Subject or Pilot?
# prefix = "pilot"
prefix = "sub"

# Category of runs (aka blocks)
category = ["food", "painting", "face", "house"]

# Group
group = ['A', 'B']

# List of lists of runs. Each sublist corresponds to one category
# according to the order stated in the list "category".
# For each sublist, the first and second element corresponds
# to the group A and B, respectively.
run_number = [[1, 5], [2, 6], [3, 7], [4, 8]]


# ==============================================================================

# %%
# Header for output files
HEADER = ['onset', 'duration', 'trial_type', 'score']

# For every participant...
for participant in participant_list:
    # For every category:
    for b, block in enumerate(category):
        for k, kind in enumerate(group):
            # Load the log files:
            # (1) define the filenames;

            ttl_fname = 'TTL_sub-' + '%02d' % participant + '_run' + \
                '%01d' % run_number[b][k] + '.mat'

            # ================ for the subjects =========================
            mbb_fname = 'MBB_battery_ratings_onsets_sub-' + \
                '%02d' % participant + '_run' + \
                '%01d' % run_number[b][k] + '_' + \
                block + '_group' + kind + '.mat'

            # ================= for the pilot ===========================
            # mbb_fname = 'MBB_battery_ratings_onsets_sub' + \
            #     '%02d' % participant + '_sess' + \
            #     '%01d' % run_number[b][k] + '_' + \
            #     block.capitalize() + '_group' + kind + '.mat'

            # ================= for the subjects ========================
            ratings_fname = 'ratings_summary_sub-' + '%02d' % participant + \
                            '_run' + '%01d' % run_number[b][k] + '_' + \
                            block + '_group' + kind + '.mat'

            # ================== for the pilot ==========================
            # ratings_fname = 'ratings_summary_sub' + '%02d' % participant + \
            #                 '_run_' + '%01d' % run_number[b][k] + '_' + \
            #                 block.capitalize() + '_group' + kind + '.mat'

            # ================= for the subjects ========================
            perm_fname = 'Perm_Rim_ratings_sub-' + '%02d' % participant + \
                         '_run' + '%01d' % run_number[b][k] + '.mat'

            # ================== for the pilot ==========================
            # perm_fname = 'Perm_Rim_ratings_sub' + '%02d' % participant + \
            #              '_sess' + '%01d' % run_number[b][k] + '.mat'

            # (2) define the pathways;
            ttl_path = os.path.abspath(os.pardir + '/protocol/results/' +
                                       prefix + '-' +
                                       '%02d' % participant + '/' + ttl_fname)
            mbb_path = os.path.abspath(os.pardir + '/protocol/results/' +
                                       prefix + '-' +
                                       '%02d' % participant + '/' + mbb_fname)
            ratings_path = os.path.abspath(os.pardir +
                                           '/protocol/results/' + prefix +
                                           '-' + '%02d' % participant + '/' +
                                           ratings_fname)
            perm_path = os.path.abspath(os.pardir + '/protocol/results/' +
                                        prefix + '-' + '%02d' % participant +
                                        '/' + perm_fname)

            no_log_flag = int()
            if not os.path.exists(ttl_path):
                print 'Warning: No TTL-file for ' + '%s' % block + \
                    ', group ' + '%s' % kind + ' and participant ' + \
                    '%s' % participant
                print ttl_path
                no_log_flag = 1
            if not os.path.exists(mbb_path):
                print 'Warning: No MBB-file for ' + '%s' % block + \
                    ', group ' + '%s' % kind + ' and participant ' + \
                    '%s' % participant
                print mbb_path
                no_log_flag = 1
            if not os.path.exists(ratings_path):
                print 'Warning: No ratings-file for ' + '%s' % block + \
                    ', group ' + '%s' % kind + ' and participant ' + \
                    '%s' % participant
                print ratings_path
                no_log_flag = 1
            if not os.path.exists(perm_path):
                print 'Warning: No perm-file for ' + '%s' % block + \
                    ', group ' + '%s' % kind + ' and participant ' + \
                    '%s' % participant
                print perm_path
                no_log_flag = 1
            if no_log_flag == 1:
                continue

            # and (3) read the log files.
            ttl_mat = [line for line in csv.reader(open(ttl_path),
                                                   delimiter=',')]
            mbb_mat = [line for line in csv.reader(open(mbb_path),
                                                   delimiter=',')]
            ratings_mat = [line for line in csv.reader(open(ratings_path),
                                                       delimiter=',')]
            perm_mat = [line for line in csv.reader(open(perm_path),
                                                    delimiter=',')]
            # Flatten list of lists
            ttl_mat_flatten = np.hstack(ttl_mat).tolist()
            mbb_mat_flatten = np.hstack(mbb_mat).tolist()
            ratings_mat_flatten = np.hstack(ratings_mat).tolist()
            perm_mat_flatten = np.hstack(perm_mat).tolist()

# %%
            # Extract TTL, onsets and durations
            TTL = int()
            flag = int()
            counter_onset = int()
            counter_duration = int()
            counter_tooslow_onset = int()
            counter_tooslow_duration = int()
            absolute_onset = []
            duration = []
            absolute_tooslow_onset = []
            tooslow_duration = []
            for t, t0 in enumerate(ttl_mat_flatten):
                if ttl_mat_flatten[t - 2] == '# name: T0':
                    TTL = round(float(t0), 3)
            for r, row in enumerate(mbb_mat_flatten):
                # Start extracting the onsets
                if row == '# name: onset':
                    flag = 1
                # Start extracting the durations
                elif row == '# name: duration':
                    flag = 2
                # Extract onsets
                elif flag == 1:
                    if mbb_mat_flatten[r - 4 - counter_onset] == \
                          '# name: display_ratingscaleRim':
                        if row[0] == '#':
                            continue
                        else:
                            counter_onset = counter_onset + 1
                            absolute_onset.append(round(float(row), 3))
                    elif mbb_mat_flatten[r - 4 - counter_tooslow_onset] == \
                            '# name: tooslowtrial_display_ratingscaleRim':
                        if row[0] == '#':
                            continue
                        else:
                            counter_tooslow_onset = counter_tooslow_onset + 1
                            absolute_tooslow_onset.append(round(float(row), 3))
                # Extract durations
                elif flag == 2:
                    if mbb_mat_flatten[r - 4 - counter_duration] == \
                          '# name: display_ratingscaleRim':
                        if row[0] == '#':
                            continue
                        else:
                            counter_duration = counter_duration + 1
                            duration.append(round(float(row), 3))
                    elif mbb_mat_flatten[r - 4 - counter_tooslow_duration] == \
                            '# name: tooslowtrial_display_ratingscaleRim':
                        if row[0] == '#':
                            continue
                        else:
                            counter_tooslow_duration = \
                                counter_tooslow_duration + 1
                            tooslow_duration.append(round(float(row), 3))

            # Remove the last onset
            # if the protocol is interrupted abruptely
            if len(absolute_onset) != len(duration):
                absolute_onset = np.delete(absolute_onset, -1).tolist()

            # Re-calculate onsets using the TTL
            onset = [round(trial_onset - TTL, 3)
                     for trial_onset in absolute_onset]
            tooslow_onset = [round(ts_onset - TTL, 3)
                             for ts_onset in absolute_tooslow_onset]

            # Extract order of images's display
            for arr in perm_mat_flatten:
                if arr[0] != '#':
                    perm = arr

            perm_comma = perm.split(' ')
            perm_string = np.delete(perm_comma, 0).tolist()
            perm_int = [int(p) for p in perm_string]

            # Extract ratings
            for line in ratings_mat_flatten:
                if line[0] != '#':
                    ratings = line

            rating_comma = ratings.split(' ')
            rating_string = np.delete(rating_comma, 0).tolist()
            rating_int = [int(x) for x in rating_string]

            rating_reordered = []
            for element in perm_int:
                rating_reordered.append(rating_int[element - 1])

            # If the protocol is interrupted abruptely...
            rating_resized = rating_reordered[:len(onset)]

            # Create array for trial type
            name = [block] * len(onset)

# %%
            # Creating final array with too_slow elements for...
            # ... onsets,
            ct_onset = int()
            all_onsets = []
            tooslow_onset_odd_idx = tooslow_onset[1::2]
            for n, onset_value in enumerate(onset):
                all_onsets.append(onset_value)
                if duration[n] == 10:
                    all_onsets.append(tooslow_onset_odd_idx[ct_onset])
                    ct_onset = ct_onset + 1

            # ... durations,
            ct_duration = int()
            all_durations = []
            tooslow_duration_odd_idx = tooslow_duration[1::2]
            for duration_value in duration:
                all_durations.append(duration_value)
                if duration_value == 10:
                    all_durations.append(tooslow_duration_odd_idx[ct_duration])
                    ct_duration = ct_duration + 1

            # ... trial type,
            ct_names = int()
            all_names = []
            for lb, label in enumerate(name):
                if duration[lb] == 10:
                    all_names.extend([label + '_too-slow', label])
                else:
                    all_names.append(label)

            # ... and ratings.
            ct_ratings = int()
            all_ratings = []
            for sc, score in enumerate(rating_resized):
                if duration[sc] == 10:
                    all_ratings.extend([np.nan, score])
                else:
                    all_ratings.append(score)

# %%
            # Stack onset, duration, trial_type and rating arrays
            liste = np.vstack((HEADER, np.vstack((all_onsets, all_durations,
                                                  all_names, all_ratings)).T))

# %%
            # Create directory for output files
            if not os.path.exists(prefix + '-' + '%02d' % participant):
                os.makedirs(prefix + '-' + '%02d' % participant)

            # Set pathway of output file
            output_path = prefix + '-' + '%02d' % participant + '/' + \
                'paradigm_descriptors_piv_' + \
                prefix + '-' + '%02d' % participant + '_run' + \
                '%01d' % run_number[b][k] + '.tsv'

            # Save liste in the output file
            with open(output_path, 'w') as fp:
                a = csv.writer(fp, delimiter='\t')
                a.writerows(liste)
