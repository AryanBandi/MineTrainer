import tkinter as tk
from tkinter import messagebox
import random
from queue import Queue

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.number = 0     #if the cell is a mine, number = -1
        self.flagged = False
    
    #accessor methods
    def get_number(self):
        return self.number

    def is_mine(self):
        return self.number == -1
        
    def is_flagged(self):
        return self.flagged

    def is_revealed(self):
        return self.revealed
        
    #modifier methods
    def set_flag(self, state):
        self.flagged = state
    
    def reveal(self):
        self.revealed = True
        
    def assign_mine(self):
        self.number = -1

class Minesweeper:
    def __init__(self, master, rows=5, cols=5, mines=10):
        self.master = master
        self.board = [[Cell(x, y) for x in range(rows)] for y in range(cols)]
        self.mines_positions = []
        self.times = Queue(maxsize = 5)

        # Load images
        # self.cell_image = tk.PhotoImage(file = "path/to/cell.png")
        # self.flag_image = tk.PhotoImage(file = "path/to/flag.png")
        # self.mine_image = tk.PhotoImage(file = "path/to/mine.png")
        
        self.fill_mines(mines)
        self.buttons = [[create_button(x, y) for x in range(rows)] for y in range(cols)]

    def create_button(self, x, y):
        btn = tk.Button(self, master, width = 1, height = 1, command = lambda x = x, y = y: self.reveal_cell(x, y))
        btn.bind('<Button-3>', lambda event, x = x, y = y: self.flag_cell(x, y))
        btn.grid(row=x, column=y)
        return btn
    
    def fill_mines(self, mines):
        for i in range(mines):
            x = random.randint(0, len(self.board) -1)
            y = random.randint(0, len(self.board[0]) - 1)
            if not self.board[x][y].is_mine():
                self.board[x][y].assign_mine()
            else:
                mines -= 1     #keeps mine count constant since no mines added

    def count_adjacent(self, x, y):
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or j < 0 or i > len(gameboard) or j > len(gameboard[0]):
                    continue
                if self.board[i, j].is_mine():
                    count += 1
        return count

    def flag_cell(self, x, y):
        target = self.board[x][y]
        if not target.is_revealed:
            target.set_flag = not target.is_flagged()

    def reveal_cell(self, x, y):
        target = self.board[x][y]
        target.reveal()

    def add_time(self, time):
        if self.times.full():
            self.times.get()        #removes the oldest time
        self.times.put(time)

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine() and not cell.is_revealed():
                    return False
        return True
            

root = tk.Tk()
root.title("Minesweeper")
game = Minesweeper(root)
root.mainloop()
