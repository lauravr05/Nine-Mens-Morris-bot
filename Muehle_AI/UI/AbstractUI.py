from abc import ABC, abstractmethod


class AbstractUI(ABC):
    @abstractmethod
    def get_user_input(self) -> int: pass

    @abstractmethod
    def display_board(self, board): pass