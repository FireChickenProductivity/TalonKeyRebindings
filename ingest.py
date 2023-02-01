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

    def load(self, directory: str, target: str):
        self.context = target.removesuffix('.csv')
        if re.fullmatch('^[a-zA-Z_]+$', self.context) is None:
            raise InvalidContextException(f'Invalid context name: {self.context} Context names should only contain letters and underscore')
        filepath = os.path.join(directory, target)
        with open(filepath, 'r') as file:
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
    def reload(self, directory: str):
        for filename in os.listdir(directory):
            binding = Keybinds()
            binding.load(filename)
            self.bindings.append(binding)
        self.reload_callback()

    def load(self, directory: str):
        fs.watch(directory, lambda path, flags: self.reload(directory))
        self.reload(directory)

    def __iter__(self):
        return self.bindings.__iter__()
