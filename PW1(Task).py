def check_win(board, player, x, y):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1

        # Рахуємо вперед
        i, j = x + dx, y + dy
        while 0 <= i < 19 and 0 <= j < 19 and board[i][j] == player:
            count += 1
            i += dx
            j += dy

        # Рахуємо назад
        i, j = x - dx, y - dy
        while 0 <= i < 19 and 0 <= j < 19 and board[i][j] == player:
            count += 1
            i -= dx
            j -= dy

        if count == 5:
            prev_x, prev_y = x - dx, y - dy
            next_x, next_y = x + dx * 5, y + dy * 5

            prev_ok = not (0 <= prev_x < 19 and 0 <= prev_y < 19 and board[prev_x][prev_y] == player)
            next_ok = not (0 <= next_x < 19 and 0 <= next_y < 19 and board[next_x][next_y] == player)

            if prev_ok and next_ok:
                start_x, start_y = x, y
                while True:
                    px = start_x - dx
                    py = start_y - dy
                    if 0 <= px < 19 and 0 <= py < 19 and board[px][py] == player:
                        start_x, start_y = px, py
                    else:
                        break
                return player, start_x + 1, start_y + 1

    return 0, -1, -1


def analyze_game(board, title=""):
    black_count = sum(row.count(1) for row in board)
    white_count = sum(row.count(2) for row in board)

    print(f"\n=== {title} ===")
    print("Легенда:")
    print(" 0 — порожня клітинка")
    print(" 1 — камінь чорного гравця")
    print(" 2 — камінь білого гравця")
    print(f"Кількість чорних каменів: {black_count}, білих каменів: {white_count}\n")

    print("Ігрове поле:")
    print("    " + " ".join(f"{i+1:2}" for i in range(19)))
    for idx, row in enumerate(board):
        print(f"{idx+1:2} | " + " ".join(str(cell) for cell in row))

    # Перевірка правильності кількості каменів
    if title == "game_result.txt":
        if white_count > black_count:
            print("\nРезультат: Помилка! Кількість білих каменів більша за чорні.")
            return
        if black_count - white_count > 1:
            print("\nРезультат: Помилка! Кількість чорних каменів більша за білі більш ніж на 1.")
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

    print("\nРезультат гри:")
    if result == 0:
        print(" Нічия або гра триває — переможця немає.")
    else:
        player = "Чорні (1)" if result == 1 else "Білі (2)"
        print(f" {player} виграли!")
        print(f" Початок переможної комбінації: рядок {res_x}, стовпчик {res_y}")

    print("=" * 60)


def read_game_result(file_path):
    import os

    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не знайдено. Будь ласка, перевірте шлях і спробуйте ще раз.")
        return

    with open(file_path, "r") as file:
        lines = file.readlines()

    if len(lines) < 1:
        print("Файл порожній або некоректний формат.")
        return

    try:
        num_games = int(lines[0].strip())
    except ValueError:
        print("Перший рядок файлу повинен містити ціле число — кількість тестів.")
        return

    index = 1
    for game_number in range(num_games):
        if index + 19 > len(lines):
            print(f"Недостатньо рядків для гри #{game_number+1}. Очікується 19 рядків для дошки.")
            break

        board = []
        correct_format = True
        for line_num in range(19):
            row_line = lines[index].strip()
            row = row_line.split()
            if len(row) != 19:
                print(f"Помилка у форматі рядка {index+1} (гра #{game_number+1}): має бути 19 чисел, отримано {len(row)}.")
                correct_format = False
                break
            try:
                row_int = list(map(int, row))
            except ValueError:
                print(f"Помилка у форматі рядка {index+1} (гра #{game_number+1}): всі значення мають бути цілими числами.")
                correct_format = False
                break

            # Перевірка значень (0,1,2)
            if any(c not in (0, 1, 2) for c in row_int):
                print(f"Помилка у рядку {index+1} (гра #{game_number+1}): дозволені лише числа 0, 1 або 2.")
                correct_format = False
                break

            board.append(row_int)
            index += 1

        if not correct_format:
            print(f"Гра #{game_number+1} пропущена через помилки формату.")
            continue

        analyze_game(board, file_path)


if __name__ == "__main__":
    read_game_result("game_result.txt")
