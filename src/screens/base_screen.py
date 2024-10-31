class BaseScreen:
    def __init__(self, game):
        self.game = game
    
    def update(self):
        pass
    
    def draw(self, surface):
        pass
    
    def handle_events(self, events):
        pass
