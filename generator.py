from .ingest import ContextSet


class TalonBuilder:
    def __init__(self, contexts: ContextSet):
        self.contexts = contexts
        self.user_callback = lambda: None
        self.files = {}

    def callback(self):
        self.build()
        self.user_callback()

    def build(self):
        for context in self.contexts:
            intermediary = ''
            for real_key, target_key in context:
                intermediary += f'key({real_key}):\n\tkey({target_key})\n\n'
            self.files[compute_tag_name_for_context(context.context)] = intermediary

    def watch(self, callback):
        self.contexts.reload_callback = self.callback
        self.user_callback = callback

    def build_and_watch(self, callback):
        self.build()
        self.watch(callback)

def compute_tag_name_for_context(context_name: str) -> str:
    '''Computes the tag name for a context given its name'''
    tag_name_with_project_prefix = 'user.keybinder_' + context_name
    return tag_name_with_project_prefix

def build_tag_creation_code(tag_name: str) -> str:
    '''Returns the python code for a file that creates a tag with the specified tag name using the tag manager.
        Assumes that the file is stored in a subdirectory of the directory with the tag_manager.py file'''
    intermediary = f"from ..tag_manager import manager\nmanager.create_tag('{tag_name}')"
    return intermediary

def build_tag_activation_keybind(keybind: str, tag_name: str) -> str:
    intermediary = build_key_command_start(keybind)
    intermediary += build_tag_activation_action_call(tag_name)
    return intermediary

def build_tag_deactivation_keybind(keybind: str, tag_name: str):
    intermediary = build_key_command_start(keybind)
    intermediary += build_tag_deactivation_action_call(tag_name)
    return intermediary

def build_key_command_start(keybind: str) -> str:
    intermediary = f'key({keybind}):\n'
    return intermediary

def build_tag_activation_action_call(tag_name: str) -> str:
    intermediary = f"\tuser.talon_key_rebindings_activate_tag('{tag_name}')\n\n"
    return intermediary

def build_tag_deactivation_action_call(tag_name: str) -> str:
    intermediary = f"\tuser.talon_key_rebindings_deactivate_tag('{tag_name}')\n\n"
    return intermediary
