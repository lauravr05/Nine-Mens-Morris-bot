
class Player:
    def __init__(self, ID : int):#
        """"
        Variables:
            - pieces_in_hand : Initial amount of pieces given to player before start of game.
                    These need to be placed on board, -1 with every piece placed (phase 1).
                    When this variable reaches 0, switch 'state' variable to 1.
            - pieces_on_board : Initial nr op pieces placed on board.
                    While state = 1, +1 with every piece placed
                    If pieces_on_board <= 3, state = 2.
                    While state = 2, -1 with every piece taken by opponent.
                        If pieces_on_board <=2, player loses.
            - state : Game state of player, defines their allowed actions.
                    0 = placing pieces.
                    1 = moving pieces
                    2 = flying

        """
        #TODO check if entered ID is either 1 or -1?
        self.ID = ID
        self.pieces_in_hand = 9
        self.pieces_on_board = 0
        self.state = 0
        self.has_lost = False

    def update_state(self):
        if self.pieces_in_hand > 0:
            self.state = 0 # Placing
        elif self.pieces_on_board == 3:
            self.state = 2  # Flying
        elif self.pieces_on_board < 3:
            self.has_lost = True
        else:
            self.state = 1  # Moving

