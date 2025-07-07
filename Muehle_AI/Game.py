#TODO Should be singleton, only a single game can be running at once.
import threading
from time import sleep

from Muehle_AI.Player.AIPlayer import AIPlayer
from Muehle_AI.Board import Board
from Muehle_AI.UI import AbstractUI
from Muehle_AI.Player.Player import Player
from Muehle_AI.UI.UI_implementations.TkinterUI import TkinterUI
from Muehle_AI.UI.UI_implementations.TerminalUI import TerminalUI


class Game :

    #gamestates:
        # 0 = placing pieces, initial state when beginning game
        # 1 = moving pieces; state after players have both places 9 pieces
        # 2 = flying; state after at least 1 player has 3 or less pieces
    def __init__(self, ui : AbstractUI, board: Board):
        """
        :param p1: initialise with 1
        :param p2: initialise with -1
        """
        self.board = board
        self.ui = ui
        self.p1 = Player(1)
        # self.p2 = Player(-1)
        self.p2 = AIPlayer(-1, self.board)
        self.currentPlayer = self.p1


    def start_game(self):
        """
        This method is called when the game starts.
        """
        self.phase_placing_pieces()
        self.phase_moving_pieces()
        self.game_over()



    def phase_placing_pieces(self):
        """Phase 1: setting pieces
            Players iteratively place their pieces. When both players have no more
            pieces left to place, the player states get set to 1.
        """
        board = self.board

        while self.p1.pieces_in_hand > 0 or self.p2.pieces_in_hand > 0:
            player = self.currentPlayer

            #If bot: choose move
            if isinstance(player, AIPlayer):
                self.ui.display_instruction(f"{self.player_name(player)}'s turn. AI is thinking...")
                sleep(1)
                move = player.get_placement(board)
                board.set_piece(player, move)
                self.ui.display_instruction(f"{self.player_name(player)} places piece at position {move}.")
                sleep(1)

            #If player: Player input to decide position of piece to place.
            else:
                while True:
                    # position = self.get_user_input(
                    position = self.ui.get_user_input(
                        f"{self.player_name(player)}'s turn. Choose position to place a piece ({player.pieces_in_hand} left to place)."
                    )
                    #Place piece
                    if board.set_piece(player, position):
                        break

            #Check for any formed mills
            if board.check_mill(player):
                self.handleMill(player)

            # board.print_board()
            self.ui.display_board(board)
            player.update_state()

            #Switch player
            self.switch_player()
        return



    def phase_moving_pieces(self):
        #TODO UI not properly updated when moving pieces. Add update after moving
        #TODO checking for mmills formed
        """Phase 2: moving pieces

        - get user input: fromPos & toPos
        - call check_valid_move with user input; if false, ask user to try again.
        - if move is valid && state is 2, call fly_piece
        - if move is valid && state is 1, call move_piece
        - check for mill
        - switch users
            """
        board = self.board


        while not self.p1.has_lost and not self.p2.has_lost:
            player = self.currentPlayer

            if player.state == 1:
                if isinstance(player, AIPlayer):
                    self.ui.display_instruction(f"{self.player_name(player)}'s turn. AI is thinking...")
                    sleep(1)
                    from_pos, to_pos = player.get_move(board)
                    board.apply_move(player, from_pos, to_pos)

                while True:
                    while True:
                        # Get user input
                        from_pos = self.ui.get_user_input(f"{self.player_name(player)}'s turn. Choose a piece to move.")
                        if self.valid_moves_exist(from_pos):
                            break
                        # No valid move for the chosen piece; ask for new input
                        self.ui.display_instruction("No valid move for this piece. Please select another piece.")
                        sleep(1)
                        continue


                    board.get_neighbours(from_pos)
                    to_pos = self.ui.get_user_input("Select piece destination.")

                # Check if given move is valid, else ask for different input
                    if board.check_valid_move(player, from_pos, to_pos):
                        board.apply_move(player, from_pos, to_pos)
                        break

            elif player.state == 2:
                while True:
                    # Get user input
                    from_pos = self.ui.get_user_input("Select a piece to move.")
                    to_pos = self.ui.get_user_input("Select piece destination.")

                    # Check if given move is valid, else ask for different input
                    if board.check_valid_fly_move(player, from_pos, to_pos):
                        board.apply_move(player, from_pos, to_pos)
                        break

            # Update board and player state, switch player
            if self.board.check_mill(player):
                self.handleMill(player)
            board.print_board()
            player.update_state()
            self.switch_player()

        return



    def game_over(self):
        if self.p1.has_lost:
            print(f"Player {self.player_name(self.p2)} wins!")
        else:
            print(f"Player {self.player_name(self.p1)} wins!")

    def valid_moves_exist(self, pos) -> bool:
        neighbours = self.board.get_neighbours(pos)
        for target in neighbours:
            if self.board.positions[target] == 0:
                move = (pos, target)
                return True
        return False



#-------------------------------------------------
    #HELPER METHODS

    def switch_player(self):
        self.currentPlayer = self.p1 if self.currentPlayer == self.p2 else self.p2

    # helper method for player printing
    #TODO is this necessary, can I utilise Board.player_name?
    def player_name(self, player):
        return "Player 1" if player.ID == 1 else "Player 2"


    def handleMill(self, player):
        if isinstance(player, AIPlayer):
            self.ui.display_instruction("CPU formed a mill and may remove a piece.")
            sleep(2)
            removed = self.p2.remove_opponent_piece(self.board, player)
            self.ui.display_instruction(f"CPU removed piece at position:{removed}")
            sleep(2)
            return

        #TODO is this displayboard necessary?
        self.ui.display_board(self.board)
        while True:
            position = self.ui.get_user_input("Please select an opponent piece to remove:")
            if self.board.remove_piece(position, player):
                break

board = Board()
tkinterUI = TkinterUI(board)
game = Game(tkinterUI, board)
game_thread = threading.Thread(target=game.start_game, daemon=True)
game_thread.start()
tkinterUI.start_ui()


# print(game.p2.ID)

