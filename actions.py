from talon import Module, actions, cron

module = Module()
insert_delay = module.setting(
    'talon_key_rebindings_insert_delay',
    type = int,
    default = 0,
    desc = 'How long to pause between disabling hot keys and inserting the text with the talon_key_rebindings_insert action'
)
@module.action_class
class Actions:
    def talon_key_rebindings_insert(text: str):
        '''Temporarily disables all hot keys, inserts the text, and re enables the hotkeys'''
        actions.mode.disable("hotkey")
        def insert_and_reenable_hotkeys(text):
            actions.insert(text)
            actions.mode.enable("hotkey")
        cron.after(f'{insert_delay.get()}ms', lambda: insert_and_reenable_hotkeys(text))
