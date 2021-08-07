from os import path, getcwd
from shutil import rmtree


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def flatten(ml):
    return [item for sublist in ml for item in sublist]


def cleanup():
    tmp = path.join(getcwd(), "/tmp")
    if path.isdir(tmp):
        rmtree(tmp)
