from contextlib import contextmanager
from tarfile import open as tarfile_open, TarFile
from typing import Generator

from .lib_funcs import file_relative_path_to_abs, file_at_path_exists, get_file_at_path, set_file_at_path, get_file_from_online
from .time_classes.time_instant import time_inst
from .time_classes.lib import TimeStorageType
from .constants import NOMINAL_SECS_PER_DAY

DEFAULT_TZDB_PATH = 'data/tzdata-latest.tar.gz'
DEFAULT_TZDB_DOWNLOADED_TIME_PATH = 'data/tzdb-downloaded-time.txt'
DEFAULT_TZDB_URL = 'https://data.iana.org/time-zones/tzdata-latest.tar.gz'
DEFAULT_TZDB_VERSION_URL = 'https://data.iana.org/time-zones/tzdb/version'
DEFAULT_TZDB_UPDATE_CHECK_TIME = 90 * NOMINAL_SECS_PER_DAY

def tzdb_stored_file_exists(file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH) -> bool:
  return file_at_path_exists(file_path)

def get_tzdb_stored_file_downloaded_time(file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH) -> time_inst.TimeInstant:
  return time_inst.TimeInstant(get_file_at_path(file_path).decode().strip())

@contextmanager
def get_tzdb_stored_file(file_path: str = DEFAULT_TZDB_PATH) -> Generator[TarFile, None, None]:
  with tarfile_open(file_relative_path_to_abs(file_path)) as tgz_file:
    yield tgz_file

def set_tzdb_stored_file_downloaded_time(time: time_inst.TimeInstant, file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH) -> None:
  set_file_at_path(file_path, f'{time.time!s}\n'.encode())

def set_tzdb_stored_file(contents: bytes, file_path: str = DEFAULT_TZDB_PATH) -> None:
  set_file_at_path(file_path, contents)

def get_tzdb_online_file(url: str = DEFAULT_TZDB_URL) -> bytes:
  return get_file_from_online(url)

def get_tzdb_online_version(url: str = DEFAULT_TZDB_VERSION_URL) -> str:
  return get_file_from_online(url).decode().strip()

def parse_tzdb_version(tgz_file: TarFile) -> str:
  with tgz_file.extractfile('version') as f:
    return f.read().decode().strip()

def parse_tzdb(tgz_file: TarFile) -> dict:
  return {}

def get_tzdb_stored_file_version(file_path: str = DEFAULT_TZDB_PATH) -> str:
  with get_tzdb_stored_file(file_path) as tgz_file:
    return parse_tzdb_version(tgz_file)

def get_tzdb_data(
    update_check_time: TimeStorageType = DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = DEFAULT_TZDB_URL,
    version_url: str = DEFAULT_TZDB_VERSION_URL,
    db_file_path: str = DEFAULT_TZDB_PATH,
    downloaded_time_file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH
  ):
  'Gets leap second array from file (if not too old) or from https://data.iana.org/time-zones/tzdata-latest.tar.gz.'
  
  current_instant = time_inst.TimeInstant.now()
  
  create_new_file = False
  
  if not tzdb_stored_file_exists(downloaded_time_file_path):
    # no stored file
    create_new_file = True
  else:
    file_age = current_instant - get_tzdb_stored_file_downloaded_time(downloaded_time_file_path)
    if file_age.time_delta > update_check_time:
      # stored file is old enough to check for update
      file_version = get_tzdb_stored_file_version(db_file_path)
      online_version = get_tzdb_online_version(version_url)
      if online_version != file_version:
        # stored file is old
        create_new_file = True
      else:
        # stored file is new, reset version string
        set_tzdb_stored_file_downloaded_time(current_instant, downloaded_time_file_path)
    else:
      # stored file is recent enough to keep
      pass
  
  if create_new_file:
    set_tzdb_stored_file(get_tzdb_online_file(tzdb_url), db_file_path)
    set_tzdb_stored_file_downloaded_time(current_instant, downloaded_time_file_path)
  
  with get_tzdb_stored_file(db_file_path) as tgz_file:
    return parse_tzdb(tgz_file)
