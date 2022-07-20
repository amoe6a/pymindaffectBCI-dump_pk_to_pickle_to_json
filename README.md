# pymindaffectBCI-dump_pk_to_pickle_to_json
Utility for a pymindaffectBCI open source software.
Converts the .pk files, resulted after the end of a BCI session and by default stored in the *pymindaffectBCI/logs* directory, into .pickle and .json formats.
The converted .pickle and .json files are by default stored in *pymindaffectBCI/logs/dumps* directory (not an original pymindaffectBCI directory).
## Usage
First, copy the *dump_pk.py* to your *pymindaffectBCI/mindaffectBCI* directory.
To convert latest *n* .pk files: (sorts by time modified, recently modified first. By default *n = 2*)
>$ python dump_pk.py  

To convert specific files:
>$ python dump_pk.py filename1 filename2 filename3 ...  

If files you want to convert are not in *pymindaffectBCI/logs* directory, you should write the global path instead of just filenames.
