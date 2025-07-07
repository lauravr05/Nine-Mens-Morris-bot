from abc import ABC, abstractmethod


class AbstractUI(ABC):
    @abstractmethod
    def get_user_input(self, prompt : str) -> int: pass
    """
    Requires string input to provide information of the specific 
    action the user needs to take.
    """
    # @abstractmethod
    # def start_ui(self): pass


    @abstractmethod
    def display_board(self, board): pass

    def display_instruction(self, message): pass