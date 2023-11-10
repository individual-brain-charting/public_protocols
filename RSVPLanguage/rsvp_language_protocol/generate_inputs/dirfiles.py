import os
import glob


def listdir_csvnohidden(path):
    """
    List only non-hidden csv files
    """
    return glob.glob(os.path.join(path, "*.csv"))


def abspath_dict(cond_filenames):
    """
    Dictionary of filename's absolute path
    """
    cond_filenames_dict = {}
    for f in cond_filenames:
        _, fname = os.path.split(f)
        fname, _ = os.path.splitext(fname)
        cond_filenames_dict[fname] = f
    return cond_filenames_dict


def dflist_csvwrite(directory, filename, dataframe_list, idx_name):
    """
    Print dataframes in csv files
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    for df, dataframe in enumerate(dataframe_list):
        dataframe.to_csv(
            os.path.join(directory, str(''.join((filename, "%s.csv")) % df)),
            index_label=idx_name)
