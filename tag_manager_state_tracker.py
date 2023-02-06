class StateTracker:
    def __init__(self):
        self.state = set()
    
    def insert(self, tag_name: str):
        self.state.add(tag_name)
    
    def remove(self, tag_name: str):
        if self.has(tag_name):
            self.state.remove(tag_name)
    
    def has(self, tag_name: str):
        return tag_name in self.state

tracker = StateTracker()
tracker.insert('user.keybinder_main')
