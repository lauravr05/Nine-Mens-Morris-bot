""""
Plan:
1. Random input:
    Bot considers all currently possible moves and chooses a random move without logic.

2. Greedy Algorithm:
    Bot considers the current possible moves and chooses the option that is the best
    right now, without any consideration for future consequences

3. Minimax Algorithm:
    Bot calculates all possible game moves for the whole board and chooses the path that maximises
    its score for the duration of the whole game
"""
from Muehle_AI.Player.AIStrategy import AIStrategy
from Muehle_AI.Player.Player import Player
from Muehle_AI.Player.Strategies.RandomAI import RandomAI


class AIPlayer(Player) :
    """"
    AI is a child class of Player.
    """
    def __init__(self, ID : int, board, strategy : AIStrategy = None):
        super().__init__(ID)
        self.board = board
        self.strategy = strategy if strategy else RandomAI()

    def get_placement(self, board):
        return self.strategy.get_placement(board)

    def get_move(self, board):
        return self.strategy.get_move(board)

    def remove_opponent_piece(self, board, player):
        """"
        Function for CPU to remove piece. If removal is successful, return position of removed piece.
        """
        position = self.strategy.get_opponent_piece_to_remove(board, player)
        if board.remove_piece(position, player):
            print("Cpu removed", position)
            return position
        else:
            print("Cpu could not remove piece")
            return None






# board = Board()
# p1 = Player(1)
# ai_random = AIPlayer(-1, board)
# # ai_greedy = AI_Player(-1, board, GreedyAI())
# # ai_minimax = AI_Player(-1, board, MinimaxAI())
#
# board.set_piece(ai_random, 2)
# board.set_piece(ai_random,1)
#
# fr, to = ai_random.get_move(board)







