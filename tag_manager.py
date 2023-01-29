from talon import Module, Context
from .fire_chicken.tag_utilities import compute_postfix

class InvalidTagException(Exception):
    pass

# Based on a tag manager made by whatIV
class TagManager:
    def __init__(self):
        self.module = Module()
        self.tags = {}
    
    def create_tag(self, tag_name):
        postfix = tag_name
        if '.' in postfix:
            postfix = compute_postfix(postfix)
        self.module.tag(postfix, desc = compute_tag_description(tag_name))
        tag_context = Context()
        self.tags[tag_name] = tag_context

    def tag_on(self, tag_name):
        if self.has_tag(tag_name):
            tag_context = self.tags[tag_name]
            tag_context.tags = [tag_name]
        else:
            self.raise_invalid_tag_exception(tag_name)

    def tag_off(self, tag_name):
        if self.has_tag(tag_name):
            self.tags[tag_name].tags = []
        else:
            self.raise_invalid_tag_exception(tag_name)
    
    def has_tag(self, tag_name):
        return self.tags.get(tag_name) != None
    
    def raise_invalid_tag_exception(self, tag_name):
        raise InvalidTagException(f'The tag manager does not have the tag {tag_name}!')

def compute_tag_description(tag_name):
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

