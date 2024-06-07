from pathlib import Path

from src.lang import E_FILE_IS_NOT_EXISTS, E_PATH_IS_NOT_A_FILE


def check_path(file_path):
    p = Path(file_path).absolute()
    if not p.exists():
        raise Exception(E_FILE_IS_NOT_EXISTS.format(p.as_posix()).capitalize())
    if not p.is_file():
        raise Exception(E_PATH_IS_NOT_A_FILE.format(p.as_posix()).capitalize())
    return p
