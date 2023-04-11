class GameStats:
    """Track statistics of alien invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.high_score = 0
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

        
