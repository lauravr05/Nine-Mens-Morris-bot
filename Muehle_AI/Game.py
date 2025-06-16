#Should be singleton, only a single game can be running at once.

class Game :

    #gamestates:
        # 1 =placing pieces, initial state when beginning game
        # 2 = moving pieces; state after players have both places 9 pieces
        # 3 = flying; state after at least 1 player has 3 or less pieces
    def __init__(self, player1, player2):
        self.player1 = 1
        self.player2 = -1
        self.currentPlayer = self.player1
        self.state = 1
        self.p1_pieces = 9
        self.p2_pieces = 9


    def start_game(self):
        """
        This method is called when the game starts. after the conditions
        to enter state 2 have been fulfullilled, this method switched to
        state 2 and calls necessary methods
        """

    def phase_1(self):
        while self.p1_pieces > 0 or self.p2_pieces > 0:


    def switch_player(self):
        self.currentPlayer *= -1

    # helper method for player printing
    def player_name(self, player):
        return "Player 1" if player == 1 else "Player 2"
