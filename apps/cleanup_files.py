# https://stackoverflow.com/questions/28379664/iife-in-python-common-convention/76936985#76936985
@lambda func: func()
def fix_import_path():
  from pathlib import Path
  from os.path import realpath
  from sys import path as sys_path

  # https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
  # https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
  parent_dir = Path(realpath(__file__)).parent.parent
  sys_path.append(str(parent_dir))

from os import walk
from os.path import isdir
from sys import argv as sys_argv
from py_time_lib import file_relative_path_to_abs
from shutil import rmtree

mode = int(sys_argv[1])

if mode & 1:
  # remove __pycache__
  for root, dirs, files in walk(file_relative_path_to_abs('..')):
    if '.git' in dirs:
      dirs.remove('.git')
    if '__pycache__' in dirs:
      remove_path = root + '/__pycache__'
      print(f'Removing {remove_path}')
      rmtree(remove_path)

if mode & 2:
  # remove py_time_lib/data files
  data_dir = file_relative_path_to_abs('data')
  if isdir(data_dir):
    print(f'Removing {data_dir}')
    rmtree(data_dir)
