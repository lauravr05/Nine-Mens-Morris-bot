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



TODO: AI logic for taking opponent piece after a mill is formed

"""
import random

from Muehle_AI.Board import Board
from Muehle_AI.Player import Player


class AI_Player(Player) :
    """"
    AI is a child class of Player.
    """
    def __init__(self, ID : int, board):
        super().__init__(ID)
        self.board = board


    def get_possible_placements(self, board):
        possible_placements = []
        for i in range(len(board.positions)):
            if board.positions[i] == 0:
                possible_placements.append(i)
        # print(possible_placements)
        return possible_placements


    def get_possible_moves(self, board):
        """"
        - get all pieces owned by cpu
        - for each owned piece, get neighbours from adjList
        - check if from-to is possible, if yes add to moves_list
        """
        possible_moves = []
        owned_positions = []
        # Check which positions are taken by cpu
        for i in range(len(board.positions)):
            if board.positions[i] == self.ID:
                owned_positions.append(i)
        # For each owned position, check what positions are in reach and open
        for position in owned_positions:
            neighbours = board.get_neighbours(position)
            for target in neighbours:
                if board.positions[target] == 0:
                    move = (position, target)
                    possible_moves.append(move)

        print(possible_moves)
        return possible_moves



    def random_placement(self, board):
        """"
        Get all possible placement positions
        Choose a random move
        """
        available_placements = self.get_possible_placements(board)
        if available_placements:
            placement = random.choice(available_placements)
            print("Cpu chose position: ", placement)
            return placement
        else:
            print("No available placements")
            return available_placements


    def random_move(self, board):
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



board = Board()
p1 = Player(1)
ai = AI_Player(-1, board)

board.set_piece(ai, 2)
board.set_piece(ai,1)

fr, to = ai.random_move(board)







