from __future__ import print_function
import sys
import os

import yaml
import hashlib


def _get_config_data(config_path):
    if config_path is None:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.load(f.read())
    return config

def _get_sha1_checksum(filename, blocksize=65536):
    """
    Return the SHA1 checksum for a dataset.
    http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
    """
    hasher = hashlib.sha1()
    f = open(filename, 'rb')
    buf = f.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = f.read(blocksize)
    return hasher.hexdigest()

def get_install_path(args):
    """
    Retrieve the  path for installing datasets from
    the GGD config file.
    """
    op = os.path
    config = _get_config_data(args.config)
    return op.abspath(op.expanduser(op.expandvars(config['path']['root'])))

# from @chapmanb
def check_software_deps(programs):
    """Ensure the provided programs exist somewhere in the current PATH.
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    if not programs:
        return True
    if isinstance(programs, basestring):
        programs = [programs]
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    for p in programs:
        found = False
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, p)
            if is_exe(exe_file):
                found = True
                break
        if not found:
            return False
    return True


def setup(args):
    install_path = get_install_path(args)
    if not os.path.exists(install_path):
        os.makedirs(install_path)

# yaml can be either empty or a list or a single value.
# we just want an empty list or a list of values.
def get_list(d, keys):
    if isinstance(keys, basestring):
        keys = [keys]

    for k in keys[:len(keys)-1]:
        d = d.get(k, {})
        if isinstance(d, list):
            assert len(d) == 1 and isinstance(d[0], dict)
            d = d[0]
    key = keys[-1]
    v = d.get(key, [])
    if not isinstance(v, list):
        v = [v]
    return v

def check_outfiles(files, overwrite=False):
    ok = True
    for f in files:
        if os.path.exists(f):
            print("%s: %s exists." % ("WARNING" if overwrite else "ERROR", f),
                  file=sys.stderr)
            if not overwrite:
                print("use --overwrite to force install.", file=sys.stderr)
            ok = overwrite
    return ok

def msg_unless(b, code=1, msg=None):
    """
    if b is True, all is OK. If it's not,
    print an optional message the return the code.
    """
    if b: return 0
    if msg:
        print(msg, file=sys.stderr)
    return code
