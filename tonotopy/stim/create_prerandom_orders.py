# -*- coding: utf-8 -*-
"""
Script for randomly create three different pre-randomized order for each set
of stimuli

author: Juan Jesus Torre Tresols
e-mail: juan-jesus.torre-tresols@inria.fr
"""

import os
import numpy as np
import glob
import csv
import random
from copy import deepcopy

# %% PARAMETERS


# The six categories of sounds
cat_names = {0: 'animal', 1: 'music', 2: 'nature',
             3: 'speech', 4: 'tools', 5: 'voice'}

# Two extra categories: trials with no sound, and trials that will be the
# same sound as the one previously displayed
extra_names = {6: 'silence', 7: 'catch'}

cat_number = len(cat_names.keys())
extra_trial_num = 5

# In each acquisition, we will use two set, three times each
prerandoms_per_set = np.arange(3)

set_list = ['set1', 'set2', 'set3', 'set4']

my_path = os.getcwd()

total_stim = len(glob.glob1(os.path.join(my_path, 'all'), '*.wav'))

# Number of stim per category in each set
stim_cat_set = int(total_stim / (cat_number * len(set_list)))


# %% FUNCTIONS

def random_map(label_array):
    """Create array of range(len(label_array)) where numbers are randomized according to their label_array value,
    and also randomized withing each value.

    Parameters
    ----------
    label_array: np.array
                 array of numbers corresponding to different categories

    Returns
    -------
    output_list: list
                 a list containing a random permutation of numbers corresponding to each value of label_array.
                 For example, if label_array were to have 10 elements of value 0 and 10 elements of value 1,
                 a random permutation of numbers from 0 to 10 would be assigned where label_array == 0, and a
                 random permutation of numbers from 11 to 20 where label_array == 1
    """

    # Initialize the output list.
    output_list = np.zeros(len(label_array))

    # Find out the number of categories...
    cat_num = len(np.unique(label_array))

    # ...and the number of elements for each category.
    stim_per_cat = int(len(label_array) / cat_num)

    for category in range(cat_num):

        output_list[label_array == category] = np.random.permutation(range(category * stim_per_cat, (category + 1) * stim_per_cat))

    output_list = output_list.astype(int)

    return output_list


def random_label_mapper(labels, elements):
    """Array of len(labels) * elements length, randomly mapped so two consecutive elements are never of the same
    category, and so elements within the same category are mapped randomly to their categories indexes.

    Parameters
    ----------
    labels: int
            desired number of categories

    elements: int
              number of stimuli per category

    Returns
    -------
    label_array: list
                 randomized list of len(range(labels)) * elements) of numbers where
    """

    for blocks in range(0, elements):

        nums = np.arange(labels)
        np.random.shuffle(nums)

        try:
            if nums[0] == label_list[-1]:
                nums[0], nums[-1] = nums[-1], nums[0]
        except NameError:
            label_list = []

        label_list.extend(nums)

    label_array = np.array(label_list)

    return label_array


def file_indexer(cat_dict, file_list):
    """Create a dictionary with keys ranging from 0 to len(file_list), which contains the name
    of the files together with their corresponding category.

    Parameters
    ----------
    cat_dict: dict
              contains keys corresponding to an integer for each category, and values
              with the name of said category

    file_list: list
               names of the files in strings

    Returns
    -------
    file_index: dict
                keys are numbers ranging from 0, and values are two-element lists containing the
                filename as first value and its corresponding category as second value
    """

    # Determine the number of elements per category
    num_files = len(file_list)
    num_cat = len(cat_dict)

    stim_per_cat = int(num_files / num_cat)

    # Create the index
    file_index = {key: [file_list[key], cat_dict[cat]] for cat in range(num_cat)
                  for key in range(cat * stim_per_cat, (cat + 1) * stim_per_cat)}

    return file_index


def audio_extra_trials(trials_list, extra_number, silence=False, catch=False):
    """
    Insert extra trials in trial_list at random positions. This extra trials are not attached to a file, but serve special purposes
    in auditory experiments.

    Parameters
    ----------

    trials_list: list
                 each element of the list is a two-element list containing the name of a file as first
                 element and the category of said stimuli as the second element.

    extra_number: int
                  number of extra trials (for each category in *args) that will be inserted.

    silence: bool (default=False)
             silence trials are usually used in auditory experiments as control condition.

    catch: bool (default=False)
           'catch' trials will copy the last non-special trial filename, but using the category 'catch'.
           This results in two consecutive trials that will display the same stimuli, which is used in
           some auditory experiments.

    Returns
    -------

    extra_list: list
                similar to trials_list, but with extra trials added. If both silence and catch are set
                to False, the result will be a copy of trials_list.
    """

    extra_list = deepcopy(trials_list)

    # Set the length of trials_list as the range to pick random numbers from
    number_of_trials = len(extra_list)

    # In case 'catch' is set to True
    if catch:

        # Generate 5 random odd numbers within the length of the list...
        catch_pos = [random.randrange(1, number_of_trials - 1, 2) for _ in range(extra_number)]

        # Check that no two numbers of catch_pos are consecutive

        # ... and insert the catch trials there
        for pos in sorted(catch_pos):
            extra_list.insert(pos, ['catch', 'catch'])

        # Make catch trials to take the name of the previous trial
        for trial in range(number_of_trials):
            if extra_list[trial][0] == 'catch':
                extra_list[trial][0] = extra_list[trial - 1][0]

    if silence:

        # Create positions for silence trials
        extra_pos = [random.randrange(1, number_of_trials - 1) for _ in range(extra_number)]

        # Insert them in the trial list
        for pos in extra_pos:
            extra_list.insert(pos, ['silence', 'silence'])

    return extra_list


# %% MAIN
def main():

    for set_ in set_list:
        set_path = os.path.join(my_path, set_)
        output_path = os.path.join(my_path, 'prerandomizations')

        # Load the files from the folder
        file_list = sorted(os.listdir(set_path))

        for prerandom in prerandoms_per_set:

            label_map = random_label_mapper(cat_number, stim_cat_set)

            number_map = random_map(label_map)

            file_index = file_indexer(cat_names, file_list)

            final_list = [file_index[number] for number in number_map]

            extra_list = audio_extra_trials(final_list, extra_trial_num,
                                            silence=True, catch=True)

            print(extra_list)

            # Save 'final_list' to a csv
            csv_file = os.path.join(output_path, set_ + '_prerand' + str(prerandom + 1))

            with open(csv_file, 'w') as output:
                writer = csv.writer(output, lineterminator='\n')
                for file in extra_list:
                    writer.writerow([file])


if __name__ == '__main__': main()
