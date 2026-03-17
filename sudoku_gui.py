import tkinter as tk
import random
from tkinter import messagebox

root = tk.Tk()
root.title("Sudoku Generator & Solver")

cells = {}
digit_labels = {}

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

grid_frame = tk.Frame(main_frame)
grid_frame.grid(row=0, column=0)

digit_frame = tk.Frame(main_frame)
digit_frame.grid(row=0, column=1, padx=30)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def create_grid():
    for r in range(9):
        for c in range(9):
            top = 2 if r == 0 else 1
            left = 2 if c == 0 else 1
            if r in [3,6]:
                top = 3
            if c in [3,6]:
                left = 3
            frame = tk.Frame(
                grid_frame,
                bg="blue" if (r in [3,6] or c in [3,6]) else "black"
            )
            frame.grid(row=r, column=c, padx=(left,0), pady=(top,0))
            e = tk.Entry(
                frame,
                width=2,
                font=("Arial",18),
                justify="center",
                bd=0
            )
            e.pack(padx=1, pady=1)
            vcmd = (root.register(validate_input), "%P")
            e.config(validate="key", validatecommand=vcmd)
            e.bind("<KeyRelease>", lambda event: update_digit_counts())
            cells[(r,c)] = e
def validate_input(P):
    return P == "" or (P.isdigit() and 1 <= int(P) <= 9)

def create_digit_panel():
    for i in range(1, 10):
        r = (i - 1) // 5
        c = (i - 1) % 5
        box = tk.Frame(digit_frame, bd=2, relief="solid", width=50, height=50)
        box.grid(row=r, column=c, padx=5, pady=5)
        box.grid_propagate(False)
        num = tk.Label(box, text=str(i), font=("Arial", 16))
        num.pack()
        count = tk.Label(box, text="9", font=("Arial", 8))
        count.pack()
        digit_labels[i] = count

def update_digit_counts():
    board = get_board()
    counts = {i: 0 for i in range(1, 10)}
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val in counts:
                counts[val] += 1
    for num in range(1, 10):
        remaining = 9 - counts[num]
        digit_labels[num].config(text=str(remaining))

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False
    return True

def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, r, c, num):
                        board[r][c] = num
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True

def generate_full_board():
    board = [[0]*9 for _ in range(9)]
    solve(board)
    return board

def make_puzzle(board):
    puzzle = [row[:] for row in board]
    remove = random.randint(40, 55)
    while remove > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            remove -= 1
    return puzzle

def display(board):
    for r in range(9):
        for c in range(9):
            cell = cells[(r,c)]
            cell.config(state="normal")   # enable first
            cell.delete(0, tk.END)
            if board[r][c] != 0:
                cell.insert(0, str(board[r][c]))
                # lock original puzzle numbers
                cell.config(state="disabled", disabledforeground="black")
            else:
                cell.config(state="normal")
    update_digit_counts()

def get_board():
    board = []
    for r in range(9):
        row = []
        for c in range(9):
            val = cells[(r, c)].get()
            if val == "" or not val.isdigit():
                row.append(0)
            else:
                row.append(int(val))
        board.append(row)
    return board

def solve_gui():
    board = get_board()
    if solve(board):
        display(board)
    else:
        messagebox.showinfo("Sudoku", "No solution exists")

def new_game():
    full = generate_full_board()
    puzzle = make_puzzle(full)
    display(puzzle)

def clear_board():
    for (r,c), cell in cells.items():
        if cell["state"] == "normal":
            cell.delete(0, tk.END)
    update_digit_counts()

create_grid()
create_digit_panel()

btn1 = tk.Button(button_frame, text="Solve", width=10, command=solve_gui)
btn1.grid(row=0, column=0, padx=10)

btn2 = tk.Button(button_frame, text="New Game", width=10, command=new_game)
btn2.grid(row=0, column=1, padx=10)

btn3 = tk.Button(button_frame, text="Clear", width=10, command=clear_board)
btn3.grid(row=0, column=2, padx=10)

new_game()
root.mainloop()