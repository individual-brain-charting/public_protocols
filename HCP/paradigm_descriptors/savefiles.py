import csv
import os


def write_csv(foldername, sess, prot, fname, liste):
    """
    Define the output pathway and create the corresponding csv files
    """
    path_output = os.path.join(foldername, sess, prot, fname)
    with open(path_output, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(liste)


def write_tsv(foldername, sess, prot, fname, liste):
    """
    Define the output pathway and create the corresponding csv files
    """
    path_output = os.path.join(foldername, sess, prot, fname)
    with open(path_output, 'w') as fp:
        a = csv.writer(fp, delimiter='\t')
        a.writerows(liste)
