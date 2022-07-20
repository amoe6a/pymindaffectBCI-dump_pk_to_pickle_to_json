import pickle
import sys
import json
import os
import numpy as np

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)

# path to a directory where your .pk log files are saved
LOGS_GLOBAL_PATH: str = "C:\pymindaffectBCI\logs"
DUMPS_DIR_NAME: str = "dumps"

def pk_load_to_dict(filename: str) -> dict:
    try:
        with open(filename,'rb') as fp:
            d = pickle.load(fp)
            return d
    except:
        print("Error opening the file '%s'. It does not exist, or it is not a .pk/.pkl/.pickle/ file. Returning empty dict" % filename)
        return {}

def get_filenames(argv: list[str]) -> list[str]:
    for each in argv:
        delim = '\\' if 'win' in sys.platform else '/'
        name: str = each.split(delim)[-1]
        if name.split('.')[-1] != 'pk': name +='.pk'
        # filenames.append(name)
        yield name

def dump_dict_json_and_pickle(argv: list[str]) -> None:
    # filenames: list = []
    filenames = get_filenames(argv)

    # note that we zip filenames with loads from argv files, because argv files may not be from LOGS_GLOBAL_PATH
    d = dict(zip(filenames, [pk_load_to_dict(each) for each in argv]))
    for file, pkdump in d.items():
        # note that for json.dump we open with 'w' option, reading the file as a textfile
        # for the pickle.dump, we need to open with 'wb' option, as pickle reads file as a bytefile.
        with open(DUMPS_DIR_NAME + '\\' + '.'.join(file.split('.')[:-1] + ["json"]), 'w') as fj:
            json.dump(pkdump, fj, cls=NumpyArrayEncoder)
        with open(DUMPS_DIR_NAME + '\\' + '.'.join(file.split('.')[:-1] + ["pickle"]), 'wb') as fp:
            pickle.dump(pkdump, fp)
    return

# get n most recent modified files we need to convert
def get_n_recent_log_files(n: int) -> list:
    args = sorted(filter(lambda x: x.endswith(".pk") or x.endswith(".pkl") or x.endswith(".pickle"), os.listdir('.')), key=os.path.getmtime, reverse=True)[0:n]
    return args

def do_dumping(argv: list = None) -> None:
    init_path = os.getcwd()
    os.chdir(LOGS_GLOBAL_PATH)
    try:
        os.mkdir(DUMPS_DIR_NAME)
        print("created the %s directory" % DUMPS_DIR_NAME)
    except OSError as e: print(e) 
    if argv is None:
        # here feel free to change your argument n.
        n = 2
        argv = get_n_recent_log_files(n)
    dump_dict_json_and_pickle(argv)
    os.chdir(init_path)
    return

# takes latest from \logs directory: (uncomment)
do_dumping()

# or from custom input filepaths. You can give a filename from the LOGS_GLOBAL_PATH dir, 
# or a global path to a file from the outside of LOGS_GLOBAL_PATH dir
# uncomment below, to use:
# argv = sys.argv[1:]
# do_dumping(argv)
