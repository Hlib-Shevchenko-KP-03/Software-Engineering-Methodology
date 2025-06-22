import tkinter as tk
from tkinter import messagebox

# Константи
BOARD_SIZE = 19
CELL_SIZE = 40  # Розмір клітинки в пікселях
STONE_RADIUS = 16  # Радіус каменю
WIN_CONDITION = 5  # Кількість каменів для перемоги

# Перевірка, чи координати в межах дошки
def is_inside_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

# Функція перевірки перемоги
def check_win(x, y):
    color = board[y][x]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        # Знаходимо початок серії
        start_x, start_y = x, y
        while is_inside_board(start_x - dx, start_y - dy) and board[start_y - dy][start_x - dx] == color:
            start_x -= dx
            start_y -= dy

        # Рахуємо кількість поспіль
        count = 0
        nx, ny = start_x, start_y
        while is_inside_board(nx, ny) and board[ny][nx] == color:
            count += 1
            nx += dx
            ny += dy

        if count == WIN_CONDITION:
            # Перевіряємо, що після серії немає ще одного такого самого каменя
            if not (is_inside_board(nx, ny) and board[ny][nx] == color):
                return True

    return False

# Обробка кліку мишкою
def click(event):
    global current_player

    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE

    if is_inside_board(x, y) and board[y][x] == 0:
        board[y][x] = current_player
        draw_stone(x, y, current_player)

        if check_win(x, y):
            winner = "Чорні" if current_player == 1 else "Білі"
            messagebox.showinfo("Перемога!", f"{winner} перемогли!")
            reset_board()
            return

        current_player = 2 if current_player == 1 else 1
        player_turn_label.config(text=f"Зараз хід: {'Чорні' if current_player == 1 else 'Білі'}")

# Малювання каменя
def draw_stone(x, y, player):
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    color = "black" if player == 1 else "white"
    canvas.create_oval(cx - STONE_RADIUS, cy - STONE_RADIUS, cx + STONE_RADIUS, cy + STONE_RADIUS, fill=color)

# Скидання гри
def reset_board():
    global board, current_player
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 1
    canvas.delete("all")
    draw_board()
    player_turn_label.config(text="Зараз хід: Чорні")

# Малювання дошки
def draw_board():
    for i in range(BOARD_SIZE):
        canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                           CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE)
        canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                           CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE)

# Створюємо основне вікно
root = tk.Tk()
root.title("Renju — The Game")

# Ініціалізація дошки та гравця
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1

# Створюємо Canvas
canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE, bg="#F0D9B5")
canvas.pack()
draw_board()

# Підпис ходу гравця
player_turn_label = tk.Label(root, text="Зараз хід: Чорні", font=("Arial", 14))
player_turn_label.pack(pady=5)

# Кнопка нової гри
reset_button = tk.Button(root, text="Нова гра", command=reset_board)
reset_button.pack(pady=5)

# Обробка кліків
canvas.bind("<Button-1>", click)

# Експорт у файл
def export_board():
    try:
        with open("game_result.txt", "w") as f:
            f.write(f"{current_player}\n")
            for row in board:
                f.write(" ".join(str(cell) for cell in row) + "\n")
        messagebox.showinfo("Експорт", "Наявна ситуація збережена в game_result.txt")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

# Кнопка експорту
export_button = tk.Button(root, text="Експорт", command=export_board)
export_button.pack(pady=5)

# Запуск гри
root.mainloop()
