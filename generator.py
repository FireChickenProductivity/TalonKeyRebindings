from re import A
from .ingest import ContextSet
import os

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
        refresh_file(self.tag_manager_filepath)
        generate_python_files(self.output_directory, self.builder.get_python_files())
        generate_talon_files(self.output_directory, self.builder.get_talon_files())

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
    return action.startswith('mouse ')

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

def build_mouse_button_key_bind(key: str, mouse_button: str):
    intermediary = f'key({key}:down): mouse_drag({mouse_button})\nkey({key}:up): mouse_release({mouse_button})'
    return intermediary

def build_tag_creation_code(tag_name: str) -> str:
    '''Returns the python code for a file that creates a tag with the specified tag name using the tag manager.
        Assumes that the file is stored in a subdirectory of the directory with the tag_manager.py file'''
    intermediary = f"from ..tag_manager import manager\nmanager.create_tag('{tag_name}')"
    return intermediary

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
