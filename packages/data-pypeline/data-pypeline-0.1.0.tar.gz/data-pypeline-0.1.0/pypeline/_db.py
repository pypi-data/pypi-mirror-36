"""
A utility module for dealing with the backing database for serialized objects (LevelDB).
"""

import os
from contextlib import contextmanager

import plyvel


@contextmanager
def open_db(loc: str) -> plyvel.DB:
    """
    Creates a managed LevelDB handle (use the 'with' statement!).
    :param loc: The directory of the database.
    :return: The database.
    """
    from filelock import FileLock

    if not os.path.exists(loc):
        os.mkdir(loc)

    lock = FileLock(os.path.join(loc, "LOCK.lock"))
    with lock:
        db = plyvel.DB(loc, create_if_missing=True)
        yield db
        db.close()


@contextmanager
def open_prefixed_db(loc: str, prefix: bytes) -> plyvel.DB:
    """
    Creates a managed LevelDB handle (use the 'with' statement!).
    :param loc: The directory of the database.
    :param prefix: The prefix for objects inserted.
    :return: The database.
    """
    with open_db(loc) as db:
        yield db.prefixed_db(prefix)
