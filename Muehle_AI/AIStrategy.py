import random
from abc import ABC, abstractmethod


class AIStrategy(ABC):
    def __init__(self, ID : int = -1):
        self.ID = ID

    def get_possible_placements(self, board):
        """
        Get all possible placement positions.
        Concrete method; the logic is common for all strategies.

        Args:
            board: The game board instance
        Returns:
            List of integers representing possible placement positions
        """

        possible_placements = []
        for i in range(len(board.positions)):
            if board.positions[i] == 0:
                possible_placements.append(i)
        # print(possible_placements)
        return possible_placements

    def get_possible_moves(self, board):
        """
        Get all possible moves for the current player.
        Concrete method; the logic is common for all strategies.

        Args:
            board: The game board instance
        Returns:
            List of tuples (from_pos, to_pos) representing possible moves
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

    def get_opponent_pieces(self, board):
        opponent_pieces = []
        for i in range(len(board.positions)):
            if board.positions[i] == self.ID*-1:
                opponent_pieces.append(i)
        return opponent_pieces



    @abstractmethod
    def get_move(self, board): pass

    @abstractmethod
    def get_placement(self, board): pass

    @abstractmethod
    def remove_opponent_piece(self, board, player): pass


#----------------------------------------------------
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




#-----------------------------------------------------------
class GreedyAI(AIStrategy):
    def __init__(self):
        super().__init__()



#-----------------------------------------------------------
class MinimaxAI(AIStrategy):
    def __init__(self):
        super().__init__()