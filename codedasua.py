import tkinter as tk
from tkinter import messagebox, font
import numpy as np

BOARD_SIZE = 20
WIN_CONDITION = 5

# Tạo bảng trò chơi 20x20
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
current_player = 1

# Lịch sử các nước đi
move_history = []

# Kiểm tra người chơi đã thắng chưa
def check_winner(player):
    # Kiểm tra hàng ngang
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - WIN_CONDITION + 1):
            if np.all(board[i, j:j+WIN_CONDITION] == player):
                return True

    # Kiểm tra hàng dọc
    for i in range(BOARD_SIZE - WIN_CONDITION + 1):
        for j in range(BOARD_SIZE):
            if np.all(board[i:i+WIN_CONDITION, j] == player):
                return True

    # Kiểm tra đường chéo chính
    for i in range(BOARD_SIZE - WIN_CONDITION + 1):
        for j in range(BOARD_SIZE - WIN_CONDITION + 1):
            if np.all(np.diag(board[i:i+WIN_CONDITION, j:j+WIN_CONDITION]) == player):
                return True

    # Kiểm tra đường chéo phụ
    for i in range(BOARD_SIZE - WIN_CONDITION + 1):
        for j in range(WIN_CONDITION - 1, BOARD_SIZE):
            if np.all(np.diag(np.fliplr(board[i:i+WIN_CONDITION, j-WIN_CONDITION+1:j+1])) == player):
                return True

    return False

# Xử lý sự kiện khi ô trên bảng được nhấp
def cell_click(row, col):
    global current_player

    if board[row, col] == 0:
        board[row, col] = current_player
        move_history.append((row, col))

        if current_player == 1:
            buttons[row][col].config(text="X", state="disabled", font=("Arial", 12, "bold"))
            if check_winner(1):
                messagebox.showinfo("Kết quả", "Người chơi X thắng!")
                reset_game()
            else:
                current_player = 2
        else:
            buttons[row][col].config(text="O", state="disabled", font=("Arial", 12, "bold"))
            if check_winner(2):
                messagebox.showinfo("Kết quả", "Người chơi O thắng!")
                reset_game()
            else:
                current_player = 1

# Đặt lại trò chơi
def reset_game():
    global board, current_player, move_history
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    current_player = 1
    move_history = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j].config(text="", state="normal", font=("Arial", 12))

# Đi lại nước đi trước đó
def undo_move():
    if len(move_history) > 0:
        last_move = move_history.pop()
        row, col = last_move
        board[row, col] = 0
        buttons[row][col].config(text="", state="normal", font=("Arial", 12))
        global current_player
        current_player = 3 - current_player  # Chuyển lượt cho người chơi khác

# Tạo giao diện
root = tk.Tk()
root.title("OX Game")

button_font = font.Font(family="Arial", size=12, weight="bold")

buttons = []
for i in range(BOARD_SIZE):
    row_buttons = []
    for j in range(BOARD_SIZE):
        button = tk.Button(root, text="", width=2, height=1,
                           command=lambda row=i, col=j: cell_click(row, col), font=button_font)
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

reset_button = tk.Button(root, text="Đặt lại", command=reset_game, font=button_font)
reset_button.grid(row=BOARD_SIZE, column=0, columnspan=BOARD_SIZE//2)

undo_button = tk.Button(root, text="Đi lại", command=undo_move, font=button_font)
undo_button.grid(row=BOARD_SIZE, column=BOARD_SIZE//2+1, columnspan=BOARD_SIZE//2)

root.mainloop()