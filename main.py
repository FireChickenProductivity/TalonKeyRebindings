from .ingest import ContextSet
from .generator import TalonBuilder, TalonGenerator
from .fire_chicken.path_utilities import compute_file_directory, create_directory_if_nonexistent
import os
from talon import Module

INPUT_DIRECTORY = os.path.join(compute_file_directory(__file__), 'Key Bindings')
OUTPUT_DIRECTORY = os.path.join(compute_file_directory(__file__), 'talon_output')
TAG_MANAGER_FILEPATH = os.path.join(compute_file_directory(__file__), 'tag_manager.py')
def set_up():
    create_directory_if_nonexistent(INPUT_DIRECTORY)
    create_directory_if_nonexistent(OUTPUT_DIRECTORY)
    context_set = ContextSet()
    builder = TalonBuilder(context_set)
    generator = TalonGenerator(builder, OUTPUT_DIRECTORY, TAG_MANAGER_FILEPATH)
    context_set.load(INPUT_DIRECTORY)

set_up()

module = Module()
@module.action_class
class Actions:
    def keybinder_add_key_bind(text: str, context_name: str = 'main'):
        ''''''
        filepath = get_keybinding_filepath(context_name) + '.txt'
        with open(filepath, 'a') as file:
            file.write('\n' + text)
            print('appending')
    
    def keybinder_remove_key_bind(binding_keystroke: str, context_name: str = 'main'):
        ''''''
        filepath = get_keybinding_filepath(context_name) + '.txt'
        lines = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
        with open(filepath, 'w') as file:
            for line in lines:
                if does_not_match(line, binding_keystroke):
                    file.write(line)


def get_keybinding_filepath(context_name: str):
    return os.path.join(INPUT_DIRECTORY, context_name)

def does_not_match(binding: str, binding_keystroke: str):
    return not (binding.startswith(binding_keystroke + ',') or binding.startswith('"' + binding_keystroke + '"' + ','))
