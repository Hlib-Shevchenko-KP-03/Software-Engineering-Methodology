import random
import os

# Генерація random_result.txt
def generate_random_game(filename):
    board_size = 19
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    total_cells = board_size * board_size
    total_moves = random.randint(30, 150)

    black_moves = total_moves // 2 + total_moves % 2
    white_moves = total_moves // 2

    moves = [1] * black_moves + [2] * white_moves + [0] * (total_cells - total_moves)
    random.shuffle(moves)

    idx = 0
    for i in range(board_size):
        for j in range(board_size):
            board[i][j] = moves[idx]
            idx += 1

    with open(filename, 'w') as f:
        f.write("1\n")
        for row in board:
            f.write(" ".join(map(str, row)) + "\n")

    return board

# Перевірка перемоги
def check_win(board, color, x, y):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        nx, ny = x, y
        while True:
            nx += dx
            ny += dy
            if 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == color:
                count += 1
            else:
                break
        nx, ny = x, y
        while True:
            nx -= dx
            ny -= dy
            if 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == color:
                count += 1
            else:
                break
        if count == 5:
            nx, ny = x, y
            while True:
                px = nx - dx
                py = ny - dy
                if 0 <= px < 19 and 0 <= py < 19 and board[px][py] == color:
                    nx, ny = px, py
                else:
                    break
            return (color, nx+1, ny+1)
    return (0, -1, -1)

# Аналіз результата
def analyze_game(board, title=""):
    black_count = sum(row.count(1) for row in board)
    white_count = sum(row.count(2) for row in board)

    print(f"\n{title} (чорних: {black_count}, білих: {white_count})")

    for row in board:
        print(" ".join(map(str, row)))

    # Перевірка кількості каменів (для кастомної гри)
    if title == "game_result.txt":
        if white_count > black_count or black_count - white_count > 1:
            print("Результат: He`s cheating!")
            return

    result = 0
    res_x, res_y = -1, -1

    for i in range(19):
        for j in range(19):
            if board[i][j] != 0:
                winner, x, y = check_win(board, board[i][j], i, j)
                if winner != 0:
                    result = winner
                    res_x, res_y = x, y
                    break
        if result != 0:
            break

    if result == 0:
        print("Результат: Нічия / Гра триває")
    else:
        player = "Чорні" if result == 1 else "Білі"
        print(f"Результат: {player} виграли! Початок комбінації: {res_x} {res_y}")

# Зчитування поля з файлу
def load_game_file(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    board = []
    for line in data[1:]:
        board.append(list(map(int, line.split())))
    return board

# Основний код
if __name__ == "__main__":
    # Генерация и анализ random_result.txt
    random_board = generate_random_game("random_result.txt")
    analyze_game(random_board, "random_result.txt")

    # Перевірка наявності game_result.txt
    if os.path.exists("game_result.txt"):
        custom_board = load_game_file("game_result.txt")
        analyze_game(custom_board, "game_result.txt")
    else:
        print("\nВідсутня кастомна гра")
