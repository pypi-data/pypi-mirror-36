import os
import re
import sys
import pathlib
import itertools
import contextlib

from .api import Distribution
from configparser import ConfigParser


class MetadataPathFinder:
    """
    A degenerate finder, supplying only a find_distribution
    method for versions of Python that do not have a
    PathFinder find_distribution.
    """
    @staticmethod
    def find_spec(*args, **kwargs):
        return None

    @classmethod
    def find_distribution(cls, name):
        paths = cls._search_paths(name)
        dists = map(PathDistribution, paths)
        return next(dists, None)

    @classmethod
    def _search_paths(cls, name):
        """
        Find metadata directories in sys.path heuristically.
        """
        return itertools.chain.from_iterable(
            cls._search_path(path, name)
            for path in map(pathlib.Path, sys.path)
            )

    @classmethod
    def _search_path(cls, root, name):
        if not root.is_dir():
            return ()
        return (
            item
            for item in root.iterdir()
            if item.is_dir()
            and str(item.name).startswith(name)
            and re.match(rf'{name}(-.*)?\.(dist|egg)-info', str(item.name))
            )


class PathDistribution(Distribution):
    def __init__(self, path):
        """
        Construct a distribution from a path to the metadata dir.
        """
        self.path = path

    def load_metadata(self, name):
        """
        Attempt to load metadata given by the name. Return None if not found.
        """
        filename = os.path.join(self.path, name)
        with contextlib.suppress(FileNotFoundError):
            with open(filename, encoding='utf-8') as fp:
                return fp.read()


def entry_points(name):
    # Avoid circular imports.
    from importlib_metadata import distribution
    as_string = distribution(name).load_metadata('entry_points.txt')
    # 2018-09-10(barry): Should we provide any options here, or let the caller
    # send options to the underlying ConfigParser?   For now, YAGNI.
    config = ConfigParser()
    config.read_string(as_string)
    return config
