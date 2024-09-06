import random


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.orientation == 'h':
                cur_x += i
            elif self.orientation == 'v':
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, size=6):
        self.size = size
        self.user_field = [['O' for _ in range(size)] for _ in range(size)]
        self.enemy_field = [['O' for _ in range(size)] for _ in range(size)]
        self.busy = []
        self.ships = []
        self.count_living = 0

    def add_ship(self, ship, user_field=True):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise ValueError("Недопустимая позиция корабля")
        for d in ship.dots:
            self.busy.append(d)
            if user_field:
                self.user_field[d.x][d.y] = "■"
            else:
                self.enemy_field[d.x][d.y] = "■"
        self.contur(ship)
        self.ships.append(ship)
        self.count_living += 1

    def out(self, d):
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def shot(self, d, user_field=True):
        if self.out(d):
            raise ValueError("Выстрел за пределы поля")

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                if user_field:
                    # Если выстрел был по игроку (ИИ стреляет)
                    self.user_field[d.x][d.y] = "X"  # Попадание ИИ на доске игрока
                else:
                    # Если выстрел был по ИИ (игрок стреляет)
                    self.enemy_field[d.x][d.y] = "X"  # Попадание игрока на доске ИИ
                if ship.lives == 0:
                    self.count_living -= 1
                return True  # Возвращаем True при попадании

        # Если выстрел не попал в корабль (промах)
        if user_field:
            self.user_field[d.x][d.y] = "T"  # Промах ИИ на доске игрока
        else:
            self.enemy_field[d.x][d.y] = "T"  # Промах игрока на доске ИИ

        return False  # Возвращаем False при промахе

    def begin(self):
        self.busy = []
        self.ships = []
        self.count_living = 0

    def __str__(self):
        user_board_str = "Ваши корабли:                     Корабли противника:\n"
        user_board_str += "  | 1 | 2 | 3 | 4 | 5 | 6 |   ||     | 1 | 2 | 3 | 4 | 5 | 6 |\n"

        for i in range(self.size):
            user_row = " | ".join(self.user_field[i])
            enemy_row = " | ".join(self.enemy_field[i])
            user_board_str += f"{i + 1} | {user_row} |   ||   {i + 1} | {enemy_row} |\n"

        return user_board_str

    def print(self):
        print(self.__str__())

    def contur(self, ship):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not self.out(cur) and cur not in self.busy:
                    self.busy.append(cur)


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        while True:
            try:
                x, y = map(int, input("Ваш ход (формат X Y): ").split())
                return Dot(x - 1, y - 1)
            except ValueError:
                print("Ошибка ввода. Введите два числа через пробел.")

    def move(self):
        while True:
            d = self.ask()
            if self.enemy_board.shot(d, user_field=False):
                print("Попал!")
                self.board.print()
                if self.enemy_board.count_living == 0:
                    print("Вы выиграли!")
                    return True
            else:
                print("Промах!")
                self.board.print()
                return False


class AI(Player):
    def move(self):
        while True:
            d = Dot(random.randint(0, self.board.size - 1), random.randint(0, self.board.size - 1))
            if self.board.shot(d):
                print("Компьютер попал!")
                self.board.print()
                if self.board.count_living == 0:
                    print("Компьютер выиграл!")
                    return True
            else:
                print("Компьютер промахнулся!")
                self.board.print()
                return False


class Game:
    def __init__(self, size=6):
        self.size = size
        player_board = self.random_board(size)
        ai_board = self.random_board(size)
        self.us = Player(player_board, ai_board)
        self.comp = AI(ai_board, player_board)

    @staticmethod
    def random_board(size=6):
        board = Board(size)
        ship_counts = {3: 1, 2: 2, 1: 4}
        for length, count in ship_counts.items():
            for _ in range(count):
                while True:
                    ship = Ship(Dot(random.randint(0, size - 1), random.randint(0, size - 1)), length,
                                random.choice(['h', 'v']))
                    try:
                        board.add_ship(ship)
                        break
                    except ValueError:
                        pass
        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            self.us.board.print()
            print("-" * 20)
            print("Ход пользователя:")

            if self.us.move():
                if self.comp.enemy_board.count_living == 0:
                    print("Игра завершена. Вы выиграли!")
                    return
            else:
                print("-" * 20)
                print("Ход компьютера:")
                if self.comp.move():
                    if self.us.board.count_living == 0:
                        print("Игра завершена. Компьютер выиграл!")
                        return

            num += 1
        print("Количество ходов:", num)


if __name__ == "__main__":
    game = Game()
    game.loop()
