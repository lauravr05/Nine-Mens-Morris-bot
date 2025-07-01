from Muehle_AI.UI.AbstractUI import AbstractUI


class TerminalUI(AbstractUI):
    def __init__(self, board):
        self.board = board

    def start_ui(self): pass

    def get_user_input(self, prompt : str = "Enter a position: ") -> int:
            print(prompt)
            min_val = 0
            max_val = 23
            while True:
                try:
                    position = int(input())
                    if position < min_val or position > max_val:
                        print("Please enter a valid position (range 0-23).")
                        continue
                    return position
                except ValueError:
                    print("This is not a number. Try again")

    def display_board(self):
        self.board.print_board()