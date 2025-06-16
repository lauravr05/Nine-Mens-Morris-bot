
class Board:

    def __init__(self):
        self.positions = self.initialise_empty_board()
        self.adjList = self.create_adj_list()
        self.millList = self.create_mill_list()
        self.millStates = {mill: None for mill in self.millList}


    def initialise_empty_board(self) -> list:
        positions = []
        for i in range(24):
            positions.append(0)
        return positions

    def create_adj_list(self):
        # access neighbours: neighbors = self.adjList(position)
        adjList = {
            0: [1, 9],
            1: [0, 2, 4],
            2: [1, 14],
            3: [4, 10],
            4: [1, 3, 5, 7],
            5: [4, 13],
            6: [7, 11],
            7: [4, 6, 8],
            8: [12, 7],
            9: [0, 21, 10],
            10: [3, 9, 11, 18],
            11: [6, 10, 15],
            12: [8, 13, 17],
            13: [5, 12, 14, 20],
            14: [2, 13, 23],
            15: [11, 16],
            16: [15, 17, 19],
            17: [12, 16],
            18: [10, 19],
            19: [16, 18, 20, 22],
            20: [13, 19],
            21: [9, 22],
            22: [19, 21, 23],
            23: [14, 22]
        }
        return adjList

    def create_mill_list(self):
        millList = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (9, 10, 11),
            (12, 13, 14),
            (15, 16, 17),
            (18, 19, 20),
            (21, 22, 23),
            (0, 9, 21),
            (3, 10, 18),
            (6, 11, 15),
            (1, 4, 7),
            (16, 19, 22),
            (8, 12, 17),
            (5, 13, 20),
            (2, 14, 23)
            ]
        return millList

    def print_board(self):
        i = 0
        for row in self.positions:
            print("Position",i, ": ", row)
            i=i+1


    def set_piece(self, player, position):
        self.positions[position] = player
        self.check_mill(player)


    def move_piece(self, player, fromPos, toPos) :
        neighbours = self.adjList[fromPos]
        if self.positions[fromPos] != player:
            print ("invalid, you do not occupy this position")
            return
        if toPos in neighbours:
            if self.positions[toPos] != 0:
                print("invalid move, position is occupied.")
                return
            else :
                self.positions[fromPos] = 0
                self.positions[toPos] = player
                self.check_mill(player)
        else :
            print("invalid move, target position not in reach.")
            return


    def check_mill(self, player):
        for mill in self.millList:
            if self.positions[mill[0]] == player and self.positions[mill[1]] == player and self.positions[mill[2]] == player:
                # mill is present
                if self.millStates[mill] is None:
                    # mill is not yet created/assigned to player
                    print("Mill created! Player", player, "on positions:", mill)
                    self.print_board()

                    #set created mill's state to True
                    self.millStates[mill] = player
                    print(self.millStates)

                    #player may remove piece of opponent
                    self.user_removal_input(player)


            elif self.millStates[mill] == player:
                #mill was set to true, but mill is no longer present
                print("mill ", mill," was opened by player ", player)
                self.millStates[mill] = None
        return

# TODO if all opponents pieces are in mills, they are allowed to be removed
    def remove_piece(self, position, player) -> bool:
        """
        Attempts to remove an opponent's piece from the given position.
        Players may not :
            - remove their own pieces
            - remove opponents piece if its part of a closed mill

        Args:
            position (int): The board position from which to remove the piece.
            player (int): The player number who is attempting to remove the piece.

        Returns:
            bool: True if removal was successful, False otherwise.
        """
        opponent = player*-1
        allInMills = True
        for pos, piece in enumerate(self.positions):
            if piece == opponent and not self.is_pos_in_closed_mill(pos, opponent):
                allInMills = False
                break

        if self.positions[position] == opponent:
            if allInMills or not self.is_pos_in_closed_mill(position, opponent):
                self.positions[position] = 0
                print(f"{self.player_name(player)} removed piece from position", position)
                return True
        print("Invalid move. This position is either not occupied by opponent or is part of a mill. \nTry another position (0-23)")
        return False


    def user_removal_input(self, player):
        print("Please select an opponent piece to remove")
        while True:
            try:
                position = int(input())
                if self.remove_piece(position, player):
                    break #valid removal, exit loop.
            except ValueError:
                print("This is not a number. Try again")


    def is_pos_in_closed_mill(self, position, opponent):
        for mill, owner in self.millStates.items():
            if owner == opponent and position in mill:
                return True
        return False

    # helper method for player printing
    def player_name(self, player):
        return "Player 1" if player == 1 else "Player 2"


board = Board()
board.set_piece(-1, 5)
board.set_piece(1, 8)
board.set_piece(1, 6)
board.set_piece(1, 7)
board.user_removal_input(-1)
board.print_board()






