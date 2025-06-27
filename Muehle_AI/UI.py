from tkinter import *
from PIL import Image, ImageTk

class GUI:

    def __init__(self):
        self.width = 1300
        self.height = 900
        self.size = str(self.width) + "x" + str(self.height)

        self.window = Tk()
        self.window.geometry(self.size)
        self.window.title("Mühle")

        self.set_background()

        self.resize_job = None
        self.window.bind('<Configure>', self.throttled_resize)

        self.window.mainloop()

    # board_image = PhotoImage(file='Board.png')
    # window.iconphoto(True, board_image)

    def update_bg_dimensions(self, event=None):
        # Get current window size
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()

        if window_width <= 1 or window_height <= 1:
            window_width = self.width
            window_height = self.height


        board_size = min(window_width, window_height) * 0.8  # 80% of the smaller window dimension
        # Calculate center position
        x = (window_width - board_size) // 2
        y = (window_height - board_size) // 2


        bg_resized = self.bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        board_resized = self.board_image.resize((int(board_size), int(board_size)), Image.Resampling.LANCZOS)

        self.bg_texture = ImageTk.PhotoImage(bg_resized)
        self.board_texture = ImageTk.PhotoImage(board_resized)

        self.wood_label.configure(image=self.bg_texture)
        self.background_label.configure(image=self.board_texture)
        self.background_label.place(x=x, y=y)


    def set_background(self):
        self.bg_image = Image.open("woodenbg.png")
        self.board_image = Image.open("Board.png")

        self.wood_label = Label(self.window)
        self.wood_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.background_label = Label(
            self.window,
            border=10,
            relief="sunken",
            bg="peru"
        )

        self.update_bg_dimensions()
        self.window.bind('<Configure>', lambda e: self.update_bg_dimensions(e))

    def throttled_resize(self, event):
        if self.resize_job is not None:
            self.window.after_cancel(self.resize_job)
        self.resize_job = self.window.after(100, self.update_bg_dimensions)


if __name__ == "__main__":
    gui = GUI()



