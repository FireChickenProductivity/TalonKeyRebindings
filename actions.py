from talon import Module, actions, cron, settings

module = Module()
insert_delay_setting_name = 'talon_key_rebindings_insert_delay'
insert_delay = 'user.' + insert_delay_setting_name
module.setting(
    insert_delay_setting_name,
    type = int,
    default = 0,
    desc = 'How long to pause between disabling hot keys and inserting the text with the talon_key_rebindings_insert action'
)

class TapManager:
    def __init__(self):
        self.active_tappings = {}
    
    def start(self, keystroke: str, interval: float, limit):
        if keystroke in self.active_tappings:
            self.stop(keystroke)
        self.active_tappings[keystroke] = Tapping(keystroke, interval, limit)

    def stop(self, keystroke: str):
        if keystroke in self.active_tappings:
            self.active_tappings[keystroke].stop()
    
class Tapping:
    def __init__(self, keystroke: str, interval: float, limit):
        self.keystroke = keystroke
        self.interval = interval
        self.limit = limit
        self.taps_performed = 0
        if self.limit > 0:
            actions.key(self.keystroke)
            self.taps_performed += 1
        self.job = cron.interval(f'{interval}ms', self.tap)

    
    def tap(self):
        if self.limit > 0:
            self.taps_performed += 1
        if self.taps_performed > self.limit and self.limit > 0:
            self.stop()
        else:
            actions.key(self.keystroke)
    
    def stop(self):
        if self.job:
            cron.cancel(self.job)
        self.job = None

tap_manager = TapManager()

@module.action_class
class Actions:
    def talon_key_rebindings_insert(text: str):
        '''Temporarily disables all hot keys, inserts the text, and re enables the hotkeys'''
        actions.mode.disable("hotkey")
        def insert_and_reenable_hotkeys(text):
            actions.insert(text)
            actions.mode.enable("hotkey")
        cron.after(f'{settings.get(insert_delay)}ms', lambda: insert_and_reenable_hotkeys(text))
    
    def talon_key_rebindings_start_tap(keystroke: str, interval: float, limit: int = 0):
        ''''''
        tap_manager.start(keystroke, interval, limit)

    def talon_key_rebinding_stop_tap(keystroke: str):
        ''''''
        tap_manager.stop(keystroke)
