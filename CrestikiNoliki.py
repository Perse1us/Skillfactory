def draw_board(board):
  for row in board:
    print('|', end='')
    for cell in row:
      print(f' {cell} |', end='')
    print()

def check_win(board, player):
  for i in range(3):
    if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
      return True
  return all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3))

def is_board_full(board):
  return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
  board = [[' ' for cell in range(3)] for row in range(3)]
  players = ['X', 'O']
  current_player = 0

  while True:
    draw_board(board)
    row = int(input(f"Игрок {players[current_player]}, введите номер строки (1-3): ")) - 1
    col = int(input(f"Игрок {players[current_player]}, введите номер столбца (1-3): ")) - 1

    if board[row][col] != ' ':
      print("Клетка уже занята!")
      continue

    board[row][col] = players[current_player]

    if check_win(board, players[current_player]):
      draw_board(board)
      print(f"Игрок {players[current_player]} выиграл!")
      break
    elif is_board_full(board):
      draw_board(board)
      print("Ничья!")
      break

    current_player = 1 - current_player

play_game()

print("Хотите сыграть еще раз? (да/нет)")
answer = input()
if answer.lower() == 'да':
  play_game()
else:
  print("Спасибо за игру!")