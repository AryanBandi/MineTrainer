import tkinter as tk
from tkinter import messagebox
import random
from queue import Queue
import time

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.number = 0     # if the cell is a mine, number = -1
        self.flagged = False

    # accessor methods
    def get_number(self):
        return self.number

    def is_mine(self):
        return self.number == -1

    def is_flagged(self):
        return self.flagged

    def is_revealed(self):
        return self.revealed

    # modifier methods
    def set_flag(self, state):
        self.flagged = state

    def set_number(self, num):
        self.number = num

    def reveal(self):
        self.revealed = True

    def assign_mine(self):
        self.number = -1

class Minesweeper:
    def __init__(self, master, rows=8, cols=13, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = []
        self.buttons = []
        self.times = Queue(maxsize=5)

        # Initialize timer
        self.timer_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.timer_label = tk.Label(self.master, text="Time: 00:00:00:000")
        self.timer_label.grid(row=self.rows + 1, columnspan=self.cols)
        self.first_click = False
        self.paused = False
        self.pause_time = 0

        
        # Initialize the board
        self.create_board()
        reset_button = tk.Button(self.master, text="Reset", command=self.reset)
        reset_button.grid(row=self.rows, columnspan=self.cols)

    def create_board(self):
        self.board = [[Cell(x, y) for y in range(self.cols)] for x in range(self.rows)]
        self.fill_mines(self.mines)
        for x in range(self.rows):
            for y in range(self.cols):
                if not self.board[x][y].is_mine():
                    self.board[x][y].set_number(self.count_adjacent(x, y))

        self.buttons = [[self.create_button(x, y) for y in range(self.cols)] for x in range(self.rows)]

    def create_button(self, x, y):
        btn = tk.Button(self.master, width=2, height=1, command=lambda x=x, y=y: self.reveal_cell(x, y))
        btn.bind('<Button-3>', lambda event, x=x, y=y: self.flag_cell(x, y))
        btn.grid(row=x, column=y)
        return btn

    def fill_mines(self, mines):
        for i in range(mines):
            while True:
                x = random.randint(0, len(self.board) - 1)
                y = random.randint(0, len(self.board[0]) - 1)
                if not self.board[x][y].is_mine():
                    self.board[x][y].assign_mine()
                    break

    def count_adjacent(self, x, y):
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or j < 0 or i >= len(self.board) or j >= len(self.board[0]):
                    continue
                if self.board[i][j].is_mine():
                    count += 1
        return count

    def flag_cell(self, x, y):
        target = self.board[x][y]
        if not target.is_revealed():
            target.set_flag(not target.is_flagged())  # flips the current flag status
            if target.is_flagged():
                self.buttons[x][y].config(text="⚑", fg='red')
            else:
                self.buttons[x][y].config(text="")

    def configure_button(self, x, y, text, fg=None):
        self.buttons[x][y].config(
            text=text,
            disabledforeground=fg,
            state="disabled",
            relief=tk.SUNKEN,
            bg='#d9d9d9'  # Set a slightly darker background color for revealed cells
        )

    def reveal_cell(self, x, y, from_flood_fill=False):
        if self.first_click == False:
            self.first_click = True
            self.start_timer()
        colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'darkblue', 5: 'darkred', 6: 'cyan', 7: 'black', 8: 'gray'}
        target = self.board[x][y]
        target_number = target.get_number()
        target_color = colors.get(target_number, 'black')
        # ensure that only a valid cell can be revealed
        if target.is_revealed() or target.is_flagged():
            return

        if target.is_mine():
            self.pause_timer()
            messagebox.showinfo("Game Over", "You hit a mine!")
            answer = messagebox.askyesno("Continue?", "Do you want to continue?")
            if answer:
                target.reveal()
                self.configure_button(x, y, "💣", fg="black")
                self.resume_timer()
        else:
            target.reveal()
            if target_number == 0:
                self.configure_button(x, y, "")
                if not from_flood_fill:
                    self.flood_fill(x, y, True)
            else:
                self.configure_button(x, y, str(target_number), fg=target_color)

        self.check_win()

    def add_time(self, time):
        if self.times.full():
            self.times.get()  # removes the oldest time
        self.times.put(time)

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine() and not cell.is_revealed():
                    return False
        self.stop_timer()
        messagebox.showinfo("Victory", "You won the game!")
        answer = messagebox.askyesno("Play Again?", "Play Again?")
        if answer:
            self.reset()

    def flood_fill(self, x, y, isFirst):
        if x < 0 or y < 0 or x >= len(self.board) or y >= len(self.board[0]):
            return
        target = self.board[x][y]
        if not isFirst and (target.is_revealed() or target.is_mine() or target.is_flagged()):
            return

        self.reveal_cell(x, y, from_flood_fill=True)

        if target.get_number() == 0:
            self.flood_fill(x - 1, y, False)
            self.flood_fill(x + 1, y, False)
            self.flood_fill(x, y - 1, False)
            self.flood_fill(x, y + 1, False)

    def start_timer(self):
        if self.first_click:
            self.timer_running = True
            self.start_time = time.perf_counter()
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.paused = False
        self.add_time(self.format_time(self.elapsed_time))
        self.elapsed_time = 0
        
    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.paused = True
            self.pause_time = time.perf_counter()
        
    def resume_timer(self): 
        if self.paused:
            #offsets start time to resume time instead of increment
            self.start_time += time.perf_counter() - self.pause_time
            #restarts timer
            self.timer_running = True
            self.paused = False
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.perf_counter() - self.start_time
            self.timer_label.config(text=self.format_time(self.elapsed_time))
            self.master.after(10, self.update_timer)  # Update every 10 milliseconds
            
    def format_time(self, time):
        millis = int((self.elapsed_time * 1000) % 1000)
        seconds = int(self.elapsed_time) % 60
        minutes = int(self.elapsed_time // 60) % 60
        hours = int(self.elapsed_time // 3600)
        return f"Time: {hours:02}:{minutes:02}:{seconds:02}:{millis:03}"
        

    def reset(self):
        self.stop_timer()
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        
        self.create_board()
        self.timer_label.config(text="Time: 00:00:00:000")
        self.first_click = False

root = tk.Tk()
root.title("Minesweeper")
root.geometry("800x600")  # Set the window size (width x height)
root.resizable(False, False)  # Disable window resizing
game = Minesweeper(root)
root.mainloop()
