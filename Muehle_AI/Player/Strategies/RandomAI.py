import random

from Muehle_AI.Player.AIStrategy import AIStrategy


class RandomAI(AIStrategy):
    def __init__(self):
        super().__init__()


    def get_placement(self, board):
        """"
        Get all possible placement positions
        Choose a random position from the available positions
        Return placement : int
        """
        available_placements = self.get_possible_placements(board)
        if available_placements:
            placement = random.choice(available_placements)
            print("Cpu chose position: ", placement)
            return placement
        else:
            print("No available placements")
            return available_placements


    def get_move(self, board):
        """"
        Choose a random move from the possible moves
        Returns tuple: from_pos, to_pos
        """
        possible_moves = self.get_possible_moves(board)
        move = random.choice(possible_moves)
        print(move)
        from_pos = move[0]
        to_pos = move[1]
        return from_pos, to_pos

    def get_opponent_piece_to_remove(self, board, player) -> int:
        opponent_pieces = self.get_opponent_pieces(board)
        position = random.choice(opponent_pieces)
        return position