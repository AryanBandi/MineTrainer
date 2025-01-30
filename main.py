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
                    pass
                if self.board[i, j].is_mine():
                    count += 1
        return count
            

root = tk.Tk()
root.title("Minesweeper")
game = Minesweeper(root)
root.mainloop()
