import ingest


class TalonBuilder:
    def __init__(self, contexts: ingest.ContextSet):
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
            self.files[f'user.keybinder_{context.context}'] = intermediary

    def watch(self, callback):
        self.contexts.reload_callback = self.callback
        self.user_callback = callback

    def build_and_watch(self, callback):
        self.build()
        self.watch(callback)