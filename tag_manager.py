from talon import Module, Context
from .fire_chicken.tag_utilities import compute_postfix
from .tag_manager_state_tracker import tracker

class InvalidTagException(Exception):
    pass

# Based on a tag manager made by whatIV
class TagManager:
    def __init__(self):
        self.module = Module()
        self.tags = {}
    
    def create_tag(self, tag_name: str):
        '''Takes the tag name as an argument.
            Creates the desired tag within the tag manager. Should be called as a python file defining the desired tag is loaded.'''
        postfix = tag_name
        if '.' in postfix:
            postfix = compute_postfix(postfix)
        self.module.tag(postfix, desc = compute_tag_description(tag_name))
        tag_context = Context()
        self.tags[tag_name] = tag_context
        if tracker.has(tag_name):
            self.tag_on(tag_name)

    def tag_on(self, tag_name: str):
        '''Takes the tag name as an argument.
            Activates the tag if it is in the manager and otherwise raises an InvalidTagException'''
        if self.has_tag(tag_name):
            tag_context = self.tags[tag_name]
            tag_context.tags = [tag_name]
            tracker.insert(tag_name)
        else:
            raise_invalid_tag_exception(tag_name)

    def tag_off(self, tag_name: str):
        '''Takes the tag name as an argument.
            Deactivates the tag if it is in the manager and otherwise raises an InvalidTagException'''
        if self.has_tag(tag_name):
            self.tags[tag_name].tags = []
            tracker.remove(tag_name)
        else:
            raise_invalid_tag_exception(tag_name)
    
    def has_tag(self, tag_name: str) -> bool:
        '''Takes the tag name as an argument.
            Returns true if a tag with the name is in the manager and false otherwise.'''
        return self.tags.get(tag_name) != None

    
def raise_invalid_tag_exception(tag_name: str):
        raise InvalidTagException(f'The tag manager does not have the tag {tag_name}!')

def compute_tag_description(tag_name: str) -> str:
    tag_postfix = compute_postfix(tag_name)
    description = f'Activates the keybindings in the {tag_postfix} context'
    return description

manager = TagManager()
module = Module()
@module.action_class
class Actions:
    def talon_key_rebindings_activate_tag(name: str):
        '''Activates the specified key rebinding context tag'''
        manager.tag_on(name)
    
    def talon_key_rebindings_deactivate_tag(name: str):
        '''Deactivates the specified key rebinding context tag'''
        manager.tag_off(name)

