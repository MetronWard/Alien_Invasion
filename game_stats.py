class GameStats:
    """Track statistics of alien invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.game_active = False
        self.high_score = 0
        self.reset_stats()
        try:
            with open('scores.txt', mode='r') as txt_file:
                scores = txt_file.read().split(',')
                del scores[-1]
                high_score = max([int(item) for item in scores])
                self.high_score = high_score
        except FileNotFoundError:
            pass

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

        
