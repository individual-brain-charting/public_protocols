# -*- coding: utf-8 -*-

import os
import csv
import dirfiles


def trial_order(order_directory):
    """
    Reads a specific trial order for n blocks from n csv files and
    returns n lists to be used by the object block_list.order_trials()
    of Expyriment library
    """
    # Define the pathway of the inputs directory
    order_path = os.path.abspath(order_directory)
    # List csv files with sequence order of the inputs
    order_filenames = dirfiles.listdir_csvnohidden(order_path)
    order_filenames.sort()
    # Read csv files
    order_list = [[i for i in csv.reader(open(order_filename))]
                  for order_filename in order_filenames]
    # Remove headers of each block lists
    for i in range(len(order_list)):
        order_list[i].pop(0)
    # Extract the sequence from the second column of the block lists
    norder_list = [[order_list[i][j][1] for j in range(len(order_list[i]))]
                   for i in range(len(order_list))]
    # Convert "string" into "int" elements
    norder_list = [map(int, norder_list[k]) for k in range(len(norder_list))]
    # Return final sequence of trials for every block
    return norder_list
