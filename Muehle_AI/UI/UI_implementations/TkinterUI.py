import os
import threading
from tkinter import *
from PIL import Image, ImageTk

from Muehle_AI.Board import Board
from Muehle_AI.Player.Player import Player
from Muehle_AI.UI.AbstractUI import AbstractUI


class TkinterUI(AbstractUI):

    def __init__(self, board):
        self.board = board
        # Initiate values for window size
        self.window_width = 1300
        self.window_height = 900


        # Get the directory containing TkinterUI.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate to the Images directory
        images_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "Images")

        # Load images using absolute paths
        self.bg_image = Image.open(os.path.join(images_dir, "woodenbg.png"))
        self.board_image = Image.open(os.path.join(images_dir, "Board.png"))

        self.window = Tk()
        self.window.geometry("1300x900")
        self.window.title("Mühle")

        self.canvas = Canvas(self.window)
        self.canvas.pack(fill="both", expand=True)

        self.instruction_text = StringVar()
        self.instruction_text.set("Click position to place a piece")
        self.instructionLabel = Label(self.canvas, textvariable=self.instruction_text, font=("Arial", 20), bg="burlywood3")
        self.instructionLabel.pack(pady=15)


        self.position_coords = self.define_position_coords()
        self.display_board()

        self.resize_job = None
        self.window.bind('<Configure>', self.throttled_resize)

        self.get_user_input()


        self.window.mainloop()


    # def start_ui(self):
    #     self.window.mainloop()


    def define_position_coords(self):
        position_coords = [
            (0.05, 0.05),  # 0
            (0.50, 0.05),  # 1
            (0.95, 0.05),  # 2
            (0.17, 0.17),  # 3
            (0.50, 0.17),  # 4
            (0.83, 0.17),  # 5
            (0.29, 0.29),  # 6
            (0.50, 0.29),  # 7
            (0.71, 0.29),  # 8
            (0.05, 0.50),  # 9
            (0.17, 0.50),  # 10
            (0.29, 0.50),  # 11
            (0.71, 0.50),  # 12
            (0.83, 0.50),  # 13
            (0.95, 0.50),  # 14
            (0.29, 0.71),  # 15
            (0.50, 0.71),  # 16
            (0.71, 0.71),  # 17
            (0.17, 0.83),  # 18
            (0.50, 0.83),  # 19
            (0.83, 0.83),  # 20
            (0.05, 0.95),  # 21
            (0.50, 0.95),  # 22
            (0.95, 0.95)  # 23
        ]
        return position_coords


    def display_board(self, event=None):
        self.canvas.delete("all")

        # Get current window size
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()

        if self.window_width <= 1 or self.window_height <= 1:
            self.window_width = 1300
            self.window_height = 900


        self.board_size = min(self.window_width, self.window_height) * 0.8      # 80% of the smaller window dimension
        self.x_board = (self.window_width - self.board_size) // 2             # Calculate center positions
        self.y_board = (self.window_height - self.board_size) // 2

        # Resize background image to fit the window
        bg_resized = self.bg_image.resize((self.window_width, self.window_height), Image.Resampling.LANCZOS)
        self.bg_texture = ImageTk.PhotoImage(bg_resized)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg_texture)

        # Graphics detail
        self.make_board_sunken(self.window_width, self.window_height)

        # Resize board picture to the appropriate size
        board_resized = self.board_image.resize((int(self.board_size), int(self.board_size)), Image.Resampling.LANCZOS)
        self.board_texture = ImageTk.PhotoImage(board_resized)
        self.canvas.create_image(self.x_board, self.y_board, anchor=NW, image=self.board_texture)

        self.draw_all_pieces()

        self.canvas.update()
        print("Board updated")




    def draw_all_pieces(self):
        print("Drawing pieces")
        for position, value in enumerate(self.board.positions):
            if value == 1:
                self._render_piece(position, colour="floral white")
            elif value == -1:
                self._render_piece(position, colour="black")

    def _render_piece(self, position, colour):
        rel_x, rel_y = self.position_coords[position]  # Relative (0 to 1) coords on board

        # Convert to absolute board-relative coordinates
        cx = self.x_board + rel_x * self.board_size
        cy = self.y_board + rel_y * self.board_size

        radius = self.board_size * 0.05  # Tune 0.03 for piece size relative to board

        self.canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill=colour, outline=""
        )


    def throttled_resize(self, event):
        if self.resize_job is not None:
            self.window.after_cancel(self.resize_job)
        self.resize_job = self.window.after(100, lambda: self.display_board())




    def make_board_sunken(self, window_width, window_height):
        """
        Helper graphics function to draw the board sunken effect.
        """
        # 1. Setup for board position and bevel size
        board_size = int(min(window_width, window_height) * 0.8)
        x = (window_width - board_size) // 2
        y = (window_height - board_size) // 2
        bevel = 8  # Thickness of sunken edge

        # 2. Base "inset" rectangle behind the board
        self.canvas.create_rectangle(
            x - bevel, y - bevel,
            x + board_size + bevel, y + board_size + bevel,
            fill="burlywood3", outline=""
        )

        # 3. Top-left highlight (simulate light)
        self.canvas.create_line(
            [(x - bevel, y + board_size + bevel),
             (x - bevel, y - bevel),
             (x + board_size + bevel, y - bevel)],
            fill="#8a6c48",
            width=6
        )

        # 4. Bottom-right shadow (simulate depth)
        self.canvas.create_line(
            [(x + board_size + bevel, y - bevel),
             (x + board_size + bevel, y + board_size + bevel),
             (x - bevel, y + board_size + bevel)],
            fill="navajo white",
            width=4
        )

    def get_user_input(self, prompt : str = "Enter a position: ") -> int:
        prompt = "Choose a position: "
        print(prompt)

        position = IntVar()
        self.canvas.bind("<Button-1>", self.on_click)

        self.window.wait_variable(position)
        return position.get()


    def on_click(self, event):
        """
        Called when the mouse is clicked on the canvas. Calls get_position to check which
        position the click is on and initialises the required action.

        :param event: mouseclick
        :return: None
        """
        window_x,window_y = event.x, event.y
        board_x = window_x - self.x_board
        board_y = window_y - self.y_board


        #TODO loop for when input is invalid?
        pos = self.get_position(board_x, board_y)
        if pos is not None:
            print(f"You clicked at ({pos})")



    def get_position(self, x, y) -> int:
        """
        Based on the location of the mouse click, returns a position on the board

        :param x: x coord of the mouseclick
        :param y: y coord of the mouseclick
        :return: int position on the board
        """
        for idx, (rel_x, rel_y) in enumerate(self.position_coords):
            radius = self.board_size * 0.05
            posx = rel_x * self.board_size
            posy = rel_y * self.board_size
            if posx - radius <= x <= posx + radius and posy - radius <= y <= posy + radius:
                return idx
        print("Invalid position")
        return None

    def display_instruction(self, instruction : str = "Click position to place a piece "):
        self.instructionLabel.config(text=instruction)
        self.instructionLabel.pack()
        self.window.update()
        print("Instruction updated")






board = Board()
tkinterUI = TkinterUI(board)
get_user_input = tkinterUI.get_user_input
