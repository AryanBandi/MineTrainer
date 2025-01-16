import tkinter as tk
from tkinter import messagebox
import random

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
        
    def is_flagged(self):
        return self.flagged
    
    def is_mine(self):
        return self.number == -1
        
    #modifier methods
    def flag(self):
        self.flagged = True
    
    def reveal(self):
        self.revealed = True
        
    def assign_mine(self):
        self.number = -1

class Minesweeper:
    def __init__(self, master, rows=5, cols=5, mines=10):
        self.master = master
        self.board = [[Cell(x, y) for x in range(rows)] for y in range(cols)]
        self.mines_positions = []
        
        self.fill_mines(mines)
    
    #currently doesn't work
    def fill_mines(self, mines):
        for i in range(mines):
            x = randint(0, len(self.board) -1)
            y = randint(0, len(self.board[0] - 1)
            if not self.board[x][y].is_mine():
                self.board[x][y].assign_mine()
            else:
                mines--     #keeps mine count constant since no mines added
            

root = tk.Tk()
root.title("Minesweeper")
game = Minesweeper(root)
root.mainloop()