import tkinter as tk
from tkinter import messagebox
import random
from queue import Queue
import time
from tkinter.font import BOLD

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = x
        self.revealed = False
        self.number = 0     # if the cell is a mine, number = -1
        self.flagged = False
    
    def get_number(self):
        return self.number

    def is_mine(self):
        return self.number == -1

    def is_flagged(self):
        return self.flagged

    def is_revealed(self):
        return self.revealed

    def set_flag(self, state):
        self.flagged = state

    def set_number(self, num):
        self.number = num

    def reveal(self):
        self.revealed = True
       
    def hide(self):
        self.revealed = False

    def assign_mine(self):
        self.number = -1

class Minesweeper:
    def __init__(self, master, rows=16, cols=30, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = []
        self.buttons = []
        self.times = Queue(maxsize=5)
        self.actions = []
        
        self.title = tk.Label(self.master, text='MineTrainer', font=("Bahnschrift Semicondensed", 22, BOLD), fg='black', justify='center')
        self.title.grid(row=0, column=0, columnspan=2, pady=10)

        # Create frames for the board and the options panel
        self.board_frame = tk.Frame(self.master)
        self.board_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.options = tk.Frame(self.master, width=200, height=750)
        self.options.pack_propagate(False)
        self.options.grid(row=1, column=1, padx=10, pady=10, sticky="ns")

        # Initialize the board
        self.create_board()

        # Initialize timer
        self.timer_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.timer_title = tk.Label(self.options, text="Time:", font=("Bahnschrift Semicondensed", 22, BOLD), anchor='center')
        self.timer_title.pack()
        self.timer_label = tk.Label(self.options, text="00:00:00:000", font=("Bahnschrift Semicondensed", 22, BOLD), anchor='center')
        self.timer_label.pack(pady=10)
        self.first_click = False
        self.paused = False
        self.pause_time = 0

        # Initialize reset button
        reset_button = tk.Button(self.options, text="New Game", command=self.reset)
        reset_button.pack(pady=10, fill='x')

        # Initialize undo button
        undo_button = tk.Button(self.options, text="Undo", command=self.undo)
        undo_button.pack(pady=10, fill='x')

        # Initialize view times button
        view_times_button = tk.Button(self.options, text="View Times", command=self.show_times)
        view_times_button.pack(pady=10, fill='x')

        # Create the times panel but keep it hidden initially
        self.create_times_panel()

    def create_board(self):
        self.board = [[Cell(x, y) for y in range(self.cols)] for x in range(self.rows)]
        self.fill_mines(self.mines)
        for x in range(self.rows):
            for y in range(self.cols):
                self.board[x][y].set_number(self.count_adjacent(x, y))

        self.buttons = [[self.create_button(x, y) for y in range(self.cols)] for x in range(self.rows)]

    def create_button(self, x, y):
        btn = tk.Button(self.board_frame, width=2, height=1, command=lambda x=x, y=y: self.reveal_cell(x, y))
        btn.bind('<Button-3>', lambda event, x=x, y=y: self.flag_cell(x, y, False))
        btn.grid(row=x, column=y)
        return btn

    def fill_mines(self, mines):
        for i in range(mines):
            while True:
                x = random.randint(0, len(self.board) - 1)
                y = random.randint(0, len(self.board[0]) - 1)
                if not self.board[x][y].is_mine() and not (x == 0 and y == 0):
                    self.board[x][y].assign_mine()
                    break

    def count_adjacent(self, x, y):
        #if (x, y) is a mine, return -1
        if self.board[x][y].is_mine():
            return -1
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or j < 0 or i >= len(self.board) or j >= len(self.board[0]):
                    continue
                if self.board[i][j].is_mine():
                    count += 1
        return count

    def flag_cell(self, x, y, undone):
        target = self.board[x][y]
        if not target.is_revealed():
            target.set_flag(not target.is_flagged())
            if target.is_flagged():
                self.buttons[x][y].config(text="⚑", fg='red')
            else:
                self.buttons[x][y].config(text="")

        if not undone:
            self.actions.append(('flag', x, y))

    def configure_button(self, x, y, text, fg=None):
        self.buttons[x][y].config(
            text=text,
            disabledforeground=fg,
            state="disabled",
            relief=tk.SUNKEN,
            bg='#d9d9d9'  # Set a slightly darker background color for revealed cells
        )

    def reveal_cell(self, x, y, from_flood_fill=False):           
        colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'darkblue', 5: 'darkred', 6: 'cyan', 7: 'black', 8: 'gray'}
        target = self.board[x][y]
        target_number = target.get_number()
        target_color = colors.get(target_number, 'black')
       
        if target.is_revealed() or target.is_flagged():
            return
        
        if self.first_click == False:
            self.first_click = True
            self.start_timer()
            if target.is_mine():
                self.switch_places(x, y)
                #reassigns target since cell state changed
                target = self.board[x][y]
                target_number = target.get_number()
                target_color = colors.get(target_number, 'black')

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

        self.actions.append(('reveal', x, y))
        self.check_win()
        
    def switch_places(self, x, y):
        #move mine to the top left
        self.board[0][0].assign_mine()
        #temporarily set number to 0 to remove mine, will update properly later
        self.board[x][y].set_number(0)
        
        #update the surrounding spaces of the space at (0,0)
        for i in range(2):
            for j in range(2):
                if not (i == 0 and j == 0):
                    self.board[i][j].set_number(self.count_adjacent(i, j))

        #update the surrounding spaces of the target space
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or j < 0 or i >= len(self.board) or j >= len(self.board[0]):
                    continue
                self.board[i][j].set_number(self.count_adjacent(i, j))

    def undo(self):
        if not self.actions:
            return
        action = self.actions.pop()
        if action[0] == 'flag':
            self.flag_cell(action[1], action[2], True)
        else:
            x, y = action[1], action[2]
            self.board[x][y].hide()
            self.buttons[x][y].config(
                text="",
                fg='black',
                state="normal",
                relief=tk.RAISED,
                bg=self.board_frame.cget('bg')
            )

    def add_time(self, time):
        if self.times.full():
            self.times.get()
        self.times.put(time)

    def clear_times(self):
        while not self.times.empty():
            self.times.get()
        
    def show_times(self):
        self.update_times_display()
        self.times_panel.grid(row=1, column=1, padx=10, pady=10, sticky="ns")
        self.options.grid_forget()

    def hide_times(self):
        self.options.grid(row=1, column=1, padx=10, pady=10, sticky="ns")
        self.times_panel.grid_forget()

    def create_times_panel(self):
        self.times_panel = tk.Frame(self.master, width = 200, height = 750)
        self.times_panel.pack_propagate(False)
        self.times_title = tk.Label(self.times_panel, text="Past Times", font=("Bahnschrift Semicondensed", 22, BOLD), anchor='center')
        self.times_title.pack()
        self.times_boxes = []
        #create each box for the times
        for _ in range(5):
            frame = tk.Frame(self.times_panel, relief=tk.RIDGE, borderwidth=2)
            frame.pack(fill=tk.X, padx=25)
            label = tk.Label(frame, text="")
            label.pack()
            self.times_boxes.append(label)
        #create average time box
        times_avg_frame = tk.Frame(self.times_panel, relief=tk.RIDGE, borderwidth=2)
        times_avg_frame.pack(fill=tk.X, padx = 15, pady = 25)
        self.times_avg = tk.Label(times_avg_frame, text="Average of 5: N/A", font=("Bahnschrift Semicondensed", 12, BOLD))
        self.times_avg.pack()
        #create best time box
        times_best_frame = tk.Frame(self.times_panel, relief=tk.RIDGE, borderwidth=2)
        times_best_frame.pack(fill=tk.X, padx = 15, pady = 0)
        self.times_best = tk.Label(times_best_frame, text="Best of 5: N/A", font=("Bahnschrift Semicondensed", 12, BOLD))
        self.times_best.pack()

        #clear times button
        clear_button = tk.Button(self.times_panel, text="Clear", font=("Bahnschrift Semicondensed", 16, BOLD), command=self.clear_times)
        clear_button.pack(pady=10, fill='x')
        #back button
        back_button = tk.Button(self.times_panel, text="Back", font=("Bahnschrift Semicondensed", 16, BOLD), command=self.hide_times)
        back_button.pack(pady=10, fill='x')
        self.times_panel.grid_forget()      # hides the panel initially

    def update_times_display(self):
        avg = 0
        best = 0
        for i, label in enumerate(self.times_boxes):
            if i < self.times.qsize():
                #retrieve formatted time
                avg += self.times.queue[i]
                if self.times.queue[i] < best:
                    best = self.times.queue[i] 
                time = self.format_time(self.times.queue[i])
                label.config(text=time, font=("Bahnschrift Semicondensed", 12))
            else:
                label.config(text="")
        avg = avg / self.times.qsize()
        self.times_avg.config(text=avg)
        self.times_best.config(text=best)
        

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine() and not cell.is_revealed():
                    return False
        self.stop_timer(game_won=True)
        messagebox.showinfo("Victory", "You won the game!")
        answer = messagebox.askyesno("Play Again?", "Play Again?")
        if answer:
            self.reset()

    def flood_fill(self, x, y, is_first):
        if x < 0 or y < 0 or x >= len(self.board) or y >= len(self.board[0]):
            return
        target = self.board[x][y]
        if not is_first and (target.is_revealed() or target.is_mine() or target.is_flagged()):
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

    def stop_timer(self, game_won):
        self.timer_running = False
        self.paused = False
        if game_won:
            self.add_time(self.elapsed_time)
        self.elapsed_time = 0
        
    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.paused = True
            self.pause_time = time.perf_counter()
        
    def resume_timer(self):
        if self.paused:
            self.start_time += time.perf_counter() - self.pause_time
            self.timer_running = True
            self.paused = False
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.perf_counter() - self.start_time
            self.timer_label.config(text=self.format_time(self.elapsed_time))
            self.master.after(10, self.update_timer)
            
    def format_time(self, time):
        millis = int((time * 1000) % 1000)
        seconds = int(time) % 60
        minutes = int(time // 60) % 60
        hours = int(time // 3600)
        return f"{hours:02}:{minutes:02}:{seconds:02}:{millis:03}"
        
    def reset(self):
        self.stop_timer(game_won=False)
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        
        self.create_board()
        self.timer_label.config(text="00:00:00:000")
        self.first_click = False
        self.actions.clear()

root = tk.Tk()
root.title("Minesweeper")
root.geometry("1000x500")
root.resizable(False, False)  # Disable window resizing
game = Minesweeper(root)
root.mainloop()
