import csv
import re
import os
from talon import resource
from talon import fs


class InvalidBindException(Exception):
    pass


class InvalidContextException(Exception):
    pass


class Keybinds:
    def __init__(self):
        self.context = ''
        self.bindings = {}

    def load(self, target: str):
        self.context = target.removesuffix('.csv')
        if re.fullmatch('^[a-zA-Z_]+$') is None:
            raise InvalidContextException('context names should only contain letters and underscore')
        with resource.open(target, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for index, row in enumerate(reader):
                if len(row) != 2:
                    raise InvalidBindException(f'error on line {index + 1}: bindings must have exactly two columns '
                                               f'keypress,targetkey')
                self.bindings[row[0]] = row[1]

    def __iter__(self):
        return self.bindings.items().__iter__()


class ContextSet:
    def __init__(self):
        self.bindings = []
        self.reload_callback = lambda: None

    # FIXME: in the event the script is not unloaded this will cause memory usage to balloon
    def reload(self, folder: str):
        for filename in os.listdir(folder):
            binding = Keybinds()
            binding.load(filename)
            self.bindings.append(binding)
        self.reload_callback()

    def load(self, folder: str):
        fs.watch(folder, lambda path, flags: self.reload(folder))
        self.reload(folder)

    def __iter__(self):
        return self.bindings.__iter__()
