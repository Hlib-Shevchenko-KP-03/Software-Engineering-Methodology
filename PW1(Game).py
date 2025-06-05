import tkinter as tk
from tkinter import messagebox

# Розмір дошки
BOARD_SIZE = 19
CELL_SIZE = 40  # Розмір клітинки в пікселях
STONE_RADIUS = 16  # Радіус каменю

# Створюємо основне вікно
root = tk.Tk()
root.title("Renju — The Game")

# Ініціалізуємо змінні
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # 0 — порожньо
current_player = 1  # 1 — чорний, 2 — білий

# Функція для перевірки перемоги
def check_win(x, y):
    color = board[y][x]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        count = 1

        # Рух вперед
        nx, ny = x + dx, y + dy
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == color:
            count += 1
            nx += dx
            ny += dy

        # Рух назад
        nx, ny = x - dx, y - dy
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == color:
            count += 1
            nx -= dx
            ny -= dy

        # Перемога тільки при рівно 5 каменях
        if count == 5:
            return True
    return False

# Функція для обробки кліку мишкою
def click(event):
    global current_player

    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE

    # Якщо клітинка порожня
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == 0:
        board[y][x] = current_player
        draw_stone(x, y, current_player)

        if check_win(x, y):
            winner = "Чорні" if current_player == 1 else "Білі"
            messagebox.showinfo("Перемога!", f"{winner} перемогли!")
            reset_board()
            return

        # Змінюємо гравця
        current_player = 2 if current_player == 1 else 1
        player_turn_label.config(text=f"Зараз хід: {'Чорні' if current_player == 1 else 'Білі'}")

# Функція для малювання каменя
def draw_stone(x, y, player):
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    color = "black" if player == 1 else "white"
    canvas.create_oval(cx - STONE_RADIUS, cy - STONE_RADIUS, cx + STONE_RADIUS, cy + STONE_RADIUS, fill=color)

# Функція для скидання гри
def reset_board():
    global board, current_player
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 1
    canvas.delete("all")
    draw_board()
    player_turn_label.config(text="Зараз хід: Чорні")

# Функція для малювання дошки
def draw_board():
    for i in range(BOARD_SIZE):
        # Горизонтальні лінії
        canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                           CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE)
        # Вертикальні лінії
        canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                           CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE)

# Створюємо Canvas для гри
canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE, bg="#F0D9B5")
canvas.pack()

# Малюємо початкову дошку
draw_board()

# Підпис ходу гравця
player_turn_label = tk.Label(root, text="Зараз хід: Чорні", font=("Arial", 14))
player_turn_label.pack(pady=5)

# Кнопка для нової гри
reset_button = tk.Button(root, text="Нова гра", command=reset_board)
reset_button.pack(pady=5)

# Прив'язуємо кліки
canvas.bind("<Button-1>", click)

# Функція експорту
def export_board():
    try:
        with open("game_result.txt", "w") as f:
            f.write(f"{current_player}\n")  # Текущий игрок первым в файле
            for row in board:
                f.write(" ".join(str(cell) for cell in row) + "\n")
        messagebox.showinfo("Експорт", "Наявна ситуація збережена в game_result.txt")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалось зберегти файл:\n{e}")

# Кнопка для експорту
export_button = tk.Button(root, text="Експорт", command=export_board)
export_button.pack(pady=5)


# Запускаємо головний цикл
root.mainloop()
