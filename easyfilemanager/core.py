import json
import os
from collections import UserDict
from os import makedirs, walk, listdir
from os.path import join, exists, splitext, isfile
from typing import Iterable, List, Union, Optional

import yaml
from logzero import logger

from .exceptions import NameAlreadyRegisteredError


class FileManager(UserDict):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, log_name="logs.log", override=False, verbose=False,
                 **kwargs):
        """
        :param override: Set this to True to override paths of names that have already been registered
        """
        super().__init__(**kwargs)
        self.file_types = {}
        self.log_file_name = log_name
        self.override = override
        self.verbose = verbose

    def register_file(self, file_name: str, path: str = '.',
                      short_name: str = None):
        if file_name in self:
            if join(path, file_name) == self[file_name]:
                return self[file_name]
            elif not self.override and self[file_name] != join(path,
                                                               file_name):
                raise NameAlreadyRegisteredError(
                        f"Override is set to {self.override} and '{file_name}' has already been registered.",
                        file_name,
                        path)
            else:
                logger.warning(
                        f"'{file_name}' already exists and is pointing to '{self[file_name]}'... Overriding.")
        if not exists(path):
            makedirs(path, exist_ok=True)
        path = join(path, file_name)
        self[file_name] = path
        if short_name:
            self[short_name] = path
        return self[file_name]

    def get_path(self, name: str):
        return self[name]

    def set_log_name(self, log_file_name: str):
        self.log_file_name = log_file_name

    def directory_load(self, path: str, recursive=False):
        """
        Load and register all files within a specified directory
        """
        if not recursive:
            files = [f for f in listdir(path) if isfile(join(path, f))]
            for file in files:
                self.register_file(file, path,
                                   splitext(file)[0] if splitext(file)[
                                                            0] != file else None)
            return files
        else:
            files_list = []
            for root, dirs, files in walk(path, topdown=True):
                for name in files:
                    file_name = name
                    short_name = splitext(name)[0] if splitext(name)[
                                                          0] != file_name else None
                    self.register_file(file_name, root, short_name)
                    files_list.append(file_name)
            return files_list

    def load(self, name: str, split=True, strip=True) -> object:
        """
        :param split: readlines() instead of read() if True
        :param strip: call strip() on each line
        """
        self.file_types[name] = 'normal'
        if self.verbose:
            logger.debug('loading %s', self[name])
        with open(self.get_path(name), "r") as f:
            if split:
                return [t.strip() if strip else t for t in f.readlines()]
            else:
                return f.read()

    def csv_load(self, name: str, headers=True, separator=',') -> List:
        if self.is_empty(name):
            return []
        data = self.load(name)[1 if headers else 0:]
        return [tuple(d.split(separator)) for d in data]

    def smart_load(self, name, **kwargs) -> object:
        """
        Automatically loads based on the file type.
        Supports JSON/YAML and will do a regular load for everything else
        """

        ext = os.path.splitext(self[name])[1]

        if ext == '.yaml':
            return self.yaml_load(name, **kwargs)
        elif ext == '.json':
            return self.json_load(name, **kwargs)
        elif ext == '.csv':
            return self.csv_load(name, **kwargs)

        return self.load(name)

    def json_load(self, name: str, **kwargs) -> dict:
        self.file_types[name] = 'json'
        if self.is_empty(name):
            return {}
        if self.verbose:
            logger.debug('loading %s', self[name])
        with open(self.get_path(name), "r") as f:
            return json.load(f, **kwargs)

    def yaml_load(self, name: str, loader=yaml.FullLoader,
                  iterable=True) -> Optional[object]:
        self.file_types[name] = 'yaml'
        if self.verbose:
            logger.debug('loading %s', self[name])
        with open(self.get_path(name), "r") as f:
            if iterable:
                return list(yaml.load_all(f, loader))
            return yaml.load(f, loader)

    def save(self, name: str, data):
        self.file_types[name] = 'normal'
        if self.verbose:
            logger.debug('saving data to %s...', self[name])
        with open(self.get_path(name), "w+") as f:
            if not isinstance(data, Iterable):
                f.write(data)
            else:
                f.write('\n'.join(
                        [f if isinstance(f, str) else str(f) for f in data]))

    def csv_save(self, name: str, data: Union[list, set, tuple],
                 headers: str):
        if self.verbose:
            logger.debug('saving csv data to %s...', self[name])
        if not len(data) > 0:
            return
        data = list(data)
        data.insert(0, headers)
        self.save(name, data)

    def json_save(self, name: str, data, default=None, **kwargs):
        self.file_types[name] = 'json'
        with open(self.get_path(name), "w+") as f:
            json.dump(data, f, indent=2, default=default, **kwargs)

    def yaml_save(self, name: str, data, **kwargs):
        self.file_types[name] = 'yaml'
        with open(self.get_path(name), "w+") as f:
            if isinstance(data, Iterable):
                return yaml.dump_all(data, f, **kwargs)
            yaml.dump(data, f, **kwargs)

    def exists(self, name: str) -> bool:
        return exists(self.get_path(name))

    def smart_save(self, name, data, **kwargs):
        """
        Automatically saves based on the file type.
        Supports JSON/YAML and will do a regular save for everything else
        """

        ext = os.path.splitext(self[name])[1]
        if ext == '.yaml':
            self.yaml_save(name, data, **kwargs)
        elif ext == '.json':
            self.json_save(name, data, **kwargs)
        elif ext == '.csv':
            self.csv_save(name, data, **kwargs)
        else:
            self.save(name, data)

    def is_empty(self, name: str):
        try:
            file = open(self.get_path(name))
        except FileNotFoundError:
            return False
        else:
            data = file.read()
            file.close()
            return not data
