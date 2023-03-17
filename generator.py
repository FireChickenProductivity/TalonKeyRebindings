from re import A
from .ingest import ContextSet
import os
from .fire_chicken.tag_utilities import compute_postfix
from .tag_manager import manager

MOUSE_BINDING_PREFIX = 'mouse '
TYPING_BINDING_PREFIX = 'type '
TAP_BINDING_KEYWORD = ' tap '
KEY_MODIFIERS = ['ctrl', 'shift', 'alt', 'super']

class TalonBuilder:
    def __init__(self, contexts: ContextSet):
        self.user_callback = lambda: None
        self.initialize_file_representations()
        self.contexts = contexts

    def initialize_file_representations(self):
        self.talon_files = {}
        self.python_files = {}

    def callback(self):
        self.build()
        self.user_callback()

    def build(self):
        self.initialize_file_representations()
        for context in self.contexts:
            context_tag_name = compute_tag_name_for_context(context.context)
            intermediary = compute_talon_script_header(context_tag_name)
            for real_key, action_description in context:
                keybind_talonscript = ''
                if is_action_tag_activatation(action_description):
                    keybind_talonscript = build_tag_activation_keybind(real_key, compute_tag_change_action_tag(action_description))
                elif is_action_tag_deactivatation(action_description):
                    keybind_talonscript = build_tag_deactivation_keybind(real_key, compute_tag_change_action_tag(action_description))
                elif is_mouse_button_binding(action_description):
                    keybind_talonscript = build_mouse_button_key_bind(real_key, action_description)
                elif is_tap_binding(action_description):
                    keybind_talonscript = build_tapping_key_bind(real_key, action_description)
                elif is_typing_binding(action_description):
                    keybind_talonscript = build_typing_key_bind(real_key, action_description)
                else:
                    keybind_talonscript = build_key_rebind(real_key, action_description)
                intermediary += keybind_talonscript
            self.talon_files[context.context] = intermediary
            self.python_files[context.context] = build_tag_creation_code(context_tag_name)
        print(self.talon_files)

    def watch(self, callback):
        self.contexts.set_reload_callback(self.callback)
        self.user_callback = callback

    def build_and_watch(self, callback):
        self.build()
        self.watch(callback)
    
    def get_talon_files(self):
        return self.talon_files
    
    def get_python_files(self):
        return self.python_files

class TalonGenerator:
    def __init__(self, builder: TalonBuilder, output_directory, tag_manager_filepath):
        self.builder = builder
        self.builder.watch(self.generate_code)
        self.output_directory = output_directory
        self.tag_manager_filepath = tag_manager_filepath

    def generate_code(self):
        remove_files_from(self.output_directory)
        manager.reset()
        generate_python_files(self.output_directory, self.builder.get_python_files())
        generate_talon_files(self.output_directory, self.builder.get_talon_files())

def compute_modifier_key_combinations(modifiers):
    modifier_combinations = []
    for index, modifier in enumerate(modifiers):
        modifier_combinations.append(modifier)
        remaining_modifiers = []
        if index < len(modifiers) - 1:
            remaining_modifiers = modifiers[index + 1:]
        new_combinations = []
        for remaining_modifier in remaining_modifiers:
            new_combination_base = '-'+ remaining_modifier
            for new_combination in new_combinations[:]:
                new_combinations.append(new_combination + new_combination_base)
            new_combinations.append(modifier + new_combination_base)
        modifier_combinations.extend(new_combinations)
    return modifier_combinations

def remove_files_from(directory):
    for filename in os.listdir(directory):
        os.remove(os.path.join(directory, filename))

def refresh_file(path):
    contents = ''
    with open(path, 'r') as original:
        contents = original.read()
    with open(path, 'w') as output:
        output.write(contents)

def generate_python_files(directory, python_files):
    for python_file_name in python_files:
        generate_python_file(directory, python_file_name, python_files[python_file_name])

def generate_python_file(directory, python_file_name, code):
    path = os.path.join(directory, python_file_name + '.py')
    with open(path, "w") as file:
        file.write(code)

def generate_talon_files(directory, talon_files):
    for talon_file_name in talon_files:
        generate_talon_file(directory, talon_file_name, talon_files[talon_file_name])
   
def generate_talon_file(directory, python_file_name, code):
    path = os.path.join(directory, python_file_name + '.talon')
    with open(path, "w") as file:
        file.write(code)

def compute_talon_script_header(required_tag_name: str):
    header = f'tag: {required_tag_name}\n-\n'
    return header

def is_action_tag_activatation(action: str):
    return action.startswith('on ')

def is_action_tag_deactivatation(action: str):
    return action.startswith('off ')

def is_mouse_button_binding(action: str):
    return action.startswith(MOUSE_BINDING_PREFIX)

def is_tap_binding(action: str):
    return ' tap ' in action and not is_typing_binding(action)

def is_typing_binding(action: str):
    return action.startswith(TYPING_BINDING_PREFIX)

def compute_tag_name_for_context(context_name: str) -> str:
    '''Computes the tag name for a context given its name'''
    tag_name_with_project_prefix = 'user.keybinder_' + context_name
    return tag_name_with_project_prefix

def compute_tag_change_action_tag(action: str):
    parts = action.split(' ')
    tag_name = parts[1]
    tag_name_with_appropriate_prefix = compute_tag_name_for_context(tag_name)
    return tag_name_with_appropriate_prefix

def build_key_rebind(real_key: str, target_key: str):
    intermediary = build_key_command_start(real_key)
    intermediary += f'\tkey({target_key})\n\n'
    return intermediary

def build_mouse_button_key_bind(key: str, action: str):
    mouse_button = compute_mouse_button_from_mouse_button_key_bind_description(action)
    intermediary = f'key({key}:down): mouse_drag({mouse_button})\nkey({key}:up): mouse_release({mouse_button})\n\n'
    return intermediary

def compute_mouse_button_from_mouse_button_key_bind_description(description: str):
    position = len(MOUSE_BINDING_PREFIX)
    button = description[position:]
    return button

def build_typing_key_bind(key: str, action: str):
    intermediary = build_key_command_start(key)
    text = compute_text_after_prefix(TYPING_BINDING_PREFIX, action)
    properly_formatted_text = text.replace('"', '\\"')
    intermediary += f'\tuser.talon_key_rebindings_insert("{properly_formatted_text}")\n\n'
    return intermediary

def build_tapping_key_bind(key: str, action: str):
    arguments, _, keystroke = action.partition(TAP_BINDING_KEYWORD)
    argument_list = arguments.split(' ')
    limit = 0
    interval = 0
    intermediary = ''
    if len(argument_list) > 0 and argument_list[0].isnumeric():
        interval = int(argument_list[0])
    if len(argument_list) > 1 and argument_list[1].isnumeric():
        limit = int(argument_list[1])
    if limit == 0:
        intermediary += build_hold_down_key_command_start(key) + f'\tuser.talon_key_rebindings_start_tap("{keystroke}", {interval})\n\n'
        intermediary += build_release_key_command_start(key) + f'\tuser.talon_key_rebinding_stop_tap("{keystroke}")\n\n'
    else:
        intermediary += build_hold_down_key_command_start(key) + f'\tskip()\n\n'
        intermediary += build_release_key_command_start(key) + f'\tuser.talon_key_rebindings_start_tap("{keystroke}", {interval}, {limit})\n\n'
    return intermediary

def build_hold_down_key_command_start(keybind: str):
    return build_key_command_start(keybind + ':down')

def build_release_key_command_start(keybind: str):
    return build_key_command_start(keybind + ':up')

def build_tag_creation_code(tag_name: str) -> str:
    '''Returns the python code for a file that creates a tag with the specified tag name using the tag manager.
        Assumes that the file is stored in a subdirectory of the directory with the tag_manager.py file'''
    intermediary = f"from talon import Module\nmodule = Module()\nmodule.tag('{compute_postfix(tag_name)}', '{compute_tag_description(tag_name)}')\nfrom ..tag_manager import manager\nmanager.insert_tag('{tag_name}')"
    return intermediary

def compute_tag_description(tag_name: str) -> str:
    tag_postfix = compute_postfix(tag_name)
    description = f'Activates the keybindings in the {tag_postfix} context'
    return description

def build_tag_activation_keybind(keybind: str, tag_name: str) -> str:
    '''Returns talon script code to bind to the specified keybind the activation of the specified tag in the tag manager'''
    intermediary = build_key_command_start(keybind)
    intermediary += build_tag_activation_action_call(tag_name)
    return intermediary

def build_tag_deactivation_keybind(keybind: str, tag_name: str) -> str:
    '''Returns talon script code to bind to the specified keybind the deactivation of the specified tag in the tag manager'''
    intermediary = build_key_command_start(keybind)
    intermediary += build_tag_deactivation_action_call(tag_name)
    return intermediary

def build_key_command_start(keybind: str) -> str:
    '''Returns the start of a keypress talon script command given the keybind to bind the command to'''
    intermediary = f'key({keybind}):\n'
    return intermediary

def build_tag_activation_action_call(tag_name: str) -> str:
    '''Returns the telling script code to activate the tag in the tag manager specified by name'''
    intermediary = f"\tuser.talon_key_rebindings_activate_tag('{tag_name}')\n\n"
    return intermediary

def build_tag_deactivation_action_call(tag_name: str) -> str:
    '''Returns the telling script code to activate the tag specified by name in the tag manager'''
    intermediary = f"\tuser.talon_key_rebindings_deactivate_tag('{tag_name}')\n\n"
    return intermediary

def compute_text_after_prefix(prefix: str, text: str):
    '''Returns the text after the number of characters in the prefix. Currently assumes that the prefix starts the string'''
    if prefix == text:
        return ''
    return text[len(prefix):]
