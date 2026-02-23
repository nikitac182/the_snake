"""
Игра «Змейка», реализованная с использованием Pygame.

Модуль содержит основную игровую логику: главный цикл,
движение змейки, генерацию яблока, обработку столкновений,
отрисовку объектов и подсчет очков.

Игра работает на основе сеточной системы координат
и обновляется с фиксированным FPS.
"""
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CENTER_SCREEN = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2,
)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Позиция текста
TEXT_POSITION = (500, 30)

# Параметры текста
FONT_SETTINGS = 'Arial', 16
FONT_NAME, FONT_SIZE = FONT_SETTINGS

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# FPS
FPS = 15

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет текста
T_COLOR = (0, 255, 0)

# Счет
score = 0

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Snake')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self):
        """
        Инициализирует игровой объект.

        Устанавливает начальное положение в центре экрана
        и присваивает цвет тела по умолчанию.
        """
        self.position = CENTER_SCREEN
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Метод отрисовки класса (переопределяется в дочерних классах)."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблочка."""

    def __init__(self, position):
        """
        Инициализирует объект яблока.

        Задает случайную позицию на игровом поле и
        назначает цвет яблока по умолчанию.
        """
        super().__init__()
        self.randomize_position(position)
        self.body_color = APPLE_COLOR

    def randomize_position(self, occupied_positions):
        """Случайно устанавливает позицию, избегая змейки."""
        while True:
            random_position = (
                GRID_SIZE * randint(0, GRID_WIDTH - 1),
                GRID_SIZE * randint(0, GRID_HEIGHT - 1)
            )
            if random_position not in occupied_positions:
                self.position = random_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        self.reset()

    def update_direction(self):
        """Обновление направления движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позиция головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        self.positions = [CENTER_SCREEN]
        self.direction = (RIGHT, LEFT, UP, DOWN)[randint(0, 3)]
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 1

    def draw(self):
        """Отрисовывает змейку целиком."""
        for index in range(self.length):
            head_rect = pg.Rect(self.positions[index], (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, head_rect)
            pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def add(self):
        """Добавление сегмента."""
        self.length += 1
        coordinates = self.positions[0]
        self.positions.append(coordinates)

    def change_color(self):
        """Меняет цвет змейки."""
        if self.body_color != APPLE_COLOR:
            self.body_color = (
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)
            )

    def check_board(self, head_x_coord, head_y_coord):
        """Проверяет выход змейки за границы экрана."""
        return (
            head_x_coord % SCREEN_WIDTH,
            head_y_coord % SCREEN_HEIGHT,
        )

    def move(self):
        """Двигает змейку на одну клетку."""
        x_pos, y_pos = self.get_head_position()
        dx, dy = self.direction
        x_pos += dx * GRID_SIZE
        y_pos += dy * GRID_SIZE
        new_coordinates = self.check_board(x_pos, y_pos)
        self.positions.insert(0, new_coordinates)
        self.positions = self.positions[:-1]


def handle_keys(game_object):
    """
    Обработка событий клавиатуры.

    Обновление направления объекта на основе ввода пользователя.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            key_bindings = {
                (pg.K_UP): (UP, DOWN),
                (pg.K_DOWN): (DOWN, UP),
                (pg.K_LEFT): (LEFT, RIGHT),
                (pg.K_RIGHT): (RIGHT, LEFT)
            }  # словарь - Клавиша: (нужное зн-е, недопустимое зн-е)
            if event.key in key_bindings:
                if game_object.direction != key_bindings.get(event.key)[1]:
                    game_object.next_direction = key_bindings.get(event.key)[0]


def increase_score():
    """Увеличивает счет игры."""
    global score
    score += 1


def reset_score():
    """Сбрасывает счет игры."""
    global score
    score = 0


def main():
    """
    Главный игровой цикл.

    Управляет:
    - обновлением состояния
    - обработкой событий
    - отрисовко объектов
    """
    pg.init()
    font = pg.font.SysFont(FONT_NAME, FONT_SIZE)

    snake = Snake()
    apple = Apple(snake.positions)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.change_color()
            snake.add()
            apple.randomize_position(snake.positions)
            increase_score()
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            reset_score()
            screen.fill(BOARD_BACKGROUND_COLOR)

        text_surface = font.render(f'Счет игры: {score}', True, T_COLOR)
        screen.blit(text_surface, TEXT_POSITION)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
