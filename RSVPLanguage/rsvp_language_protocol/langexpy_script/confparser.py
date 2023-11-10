import os
import re
from configobj import ConfigObj


def _sanitize(section, key, **replacements):
    val = section[key]
    if isinstance(val, basestring):
        for k, v in replacements.items():
            val = val.replace("%" + k + "%", v)
    if isinstance(val, basestring):
        if val.lower() in ["true", "yes"]:
            # positive answers
            val = True
        elif val.lower() in ["false", "no"]:
            # negative answers
            val = False
        elif key == "slice_order":
            val = val.lower()
        elif val.lower() in ["none", "auto", "unspecified", "unknown",
                             "default"]:
            # user wants the default value to be used
            val = None
        elif re.match("^ *?$", val):
            # empty value specified
            val = None

    section[key] = val


def load_config(config_file, **replacements):
    """Load configuration from .ini python configuration file
    Parameters
    ----------
    config_file: string (existing filename)
        .ini file containing the configuration to be loaded.

    Returns
    -------
    config: dict
        Key-value pairs of loaded stuff.

    Notes
    -----
    Code borrowed from pypreprocess's conf_parse module.
    """
    if not os.path.isfile(config_file):
        raise OSError("Configuration file '%s' doesn't exist!" % config_file)
    cobj = ConfigObj(config_file)
    cobj.walk(_sanitize, call_on_sections=True, **replacements)
    config = cobj['config']

    # convert numerals
    for k, v in config.iteritems():
        try:
            config[k] = eval(v)
        except:
            pass
    return config
