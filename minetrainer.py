import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows=16, cols=30, mines=99):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.mines_positions = []
        self.flags = set()
        
        self.create_widgets()
        self.place_mines()
        self.update_mine_count()

    def create_widgets(self):
        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.label = tk.Label(top_frame, text="Minesweeper", font=("Helvetica", 16))
        self.label.pack(side=tk.LEFT, padx=10)
        
        self.mine_count_label = tk.Label(top_frame, text=f"Mines: {self.mines}", font=("Helvetica", 16))
        self.mine_count_label.pack(side=tk.RIGHT, padx=10)
        
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack()
        
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.grid_frame, width=2, height=1, font=("Helvetica", 14), 
                                   command=lambda r=r, c=c: self.click(r, c))
                button.grid(row=r, column=c, padx=1, pady=1)
                button.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                self.buttons[(r, c)] = button

    def place_mines(self):
        self.mines_positions = random.sample(self.buttons.keys(), self.mines)
        for pos in self.mines_positions:
            self.buttons[pos].config(command=lambda pos=pos: self.click_mine(pos))

    def update_mine_count(self):
        self.mine_count_label.config(text=f"Mines: {self.mines - len(self.flags)}")

    def click(self, r, c):
        if (r, c) in self.flags:
            return
        
        if (r, c) in self.mines_positions:
            self.game_over()
        else:
            self.reveal(r, c)
            if self.check_victory():
                self.victory()

    def click_mine(self, pos):
        self.buttons[pos].config(text="*", bg="red")
        self.game_over()

    def toggle_flag(self, r, c):
        if self.buttons[(r, c)].cget('state') == 'disabled':
            return
        
        if (r, c) in self.flags:
            self.buttons[(r, c)].config(text="")
            self.flags.remove((r, c))
        else:
            self.buttons[(r, c)].config(text="F", fg="red")
            self.flags.add((r, c))
        
        self.update_mine_count()

    def reveal(self, r, c):
        if self.buttons[(r, c)].cget('state') == 'disabled':
            return
        
        colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'darkblue', 5: 'darkred', 6: 'cyan', 7: 'black', 8: 'gray'}
        mines_count = sum((nr, nc) in self.mines_positions for nr in range(r-1, r+2) for nc in range(c-1, c+2) if 0 <= nr < self.rows and 0 <= nc < self.cols)
        self.buttons[(r, c)].config(text=str(mines_count) if mines_count > 0 else "", state="disabled", relief=tk.SUNKEN,
                                    fg=colors.get(mines_count, 'black'))
        
        if mines_count == 0:
            for nr in range(r-1, r+2):
                for nc in range(c-1, c+2):
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)

    def game_over(self):
        for pos in self.mines_positions:
            self.buttons[pos].config(text="*", bg="red")
        for button in self.buttons.values():
            button.config(state="disabled")
        messagebox.showinfo("Game Over", "You clicked on a mine. Game Over!")
        self.play_again_option()

    def check_victory(self):
        non_mine_cells = set(self.buttons.keys()) - set(self.mines_positions)
        revealed_cells = {pos for pos, button in self.buttons.items() if button.cget('state') == 'disabled'}
        return non_mine_cells == revealed_cells

    def victory(self):
        for pos in self.mines_positions:
            self.buttons[pos].config(text="*", bg="green")
        for button in self.buttons.values():
            button.config(state="disabled")
        messagebox.showinfo("Victory", "Congratulations! You've cleared all the mines!")
        self.play_again_option()

    def play_again_option(self):
        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            self.reset_game()

    def reset_game(self):
        for button in self.buttons.values():
            button.destroy()
        self.buttons.clear()
        self.flags.clear()
        self.create_widgets()
        self.place_mines()
        self.update_mine_count()

root = tk.Tk()
root.title("Minesweeper")
game = Minesweeper(root)
root.mainloop()
