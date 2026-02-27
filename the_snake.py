"""
Игра «Змейка», реализованная с использованием Pygame.

Модуль содержит основную игровую логику: главный цикл,
движение змейки, генерацию яблока, обработку столкновений,
отрисовку объектов и подсчет очков.

Игра работает на основе сеточной системы координат
и обновляется с фиксированным FPS.
"""
from random import randint, choice

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

# Позиции, в которых появится яблоку
PROHIBITING_POS = [
    CENTER_SCREEN,
    (SCREEN_WIDTH + GRID_SIZE, SCREEN_HEIGHT),
    (SCREEN_WIDTH - GRID_SIZE, SCREEN_HEIGHT),
    (SCREEN_WIDTH, SCREEN_HEIGHT + GRID_SIZE),
    (SCREEN_WIDTH, SCREEN_HEIGHT - GRID_SIZE),
]

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
        raise NotImplementedError("Метод должен быть переопределен")

    def _draw_cell(self, position, color):
        """Рисует ячейку сетки с заданным положением и цветом."""
        position = position or self.position
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблочка."""

    def __init__(self, positions=PROHIBITING_POS):
        """
        Инициализирует объект яблока.

        Задает случайную позицию на игровом поле и
        назначает цвет яблока по умолчанию.
        """
        super().__init__()
        self.randomize_position(positions)
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
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        self.positions = [CENTER_SCREEN]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 1

    def draw(self):
        """Отрисовывает змейку целиком."""
        for index in range(self.length):
            head_rect = pg.Rect(self.positions[index], (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, head_rect)
            pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def add_length(self):
        """Увеличение длины змейки."""
        self.length += 1

    def change_color(self):
        """Меняет цвет змейки."""
        if self.body_color != APPLE_COLOR:
            self.body_color = (
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)
            )
        else:
            self.body_color = (BOARD_BACKGROUND_COLOR)

    def check_board(self, head_x_coord, head_y_coord):
        """Проверяет выход змейки за границы экрана."""
        return (
            head_x_coord % SCREEN_WIDTH,
            head_y_coord % SCREEN_HEIGHT,
        )

    def delete_last_segment(self):
        """Удаляет последний сегмент."""
        self.positions = self.positions[:-1]

    def move(self):
        """Двигает змейку на одну клетку."""
        x_pos, y_pos = self.get_head_position()
        dx, dy = self.direction
        x_pos += dx * GRID_SIZE
        y_pos += dy * GRID_SIZE
        new_coordinates = self.check_board(x_pos, y_pos)
        self.positions.insert(0, new_coordinates)


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
                pg.K_UP: (UP, DOWN),
                pg.K_DOWN: (DOWN, UP),
                pg.K_LEFT: (LEFT, RIGHT),
                pg.K_RIGHT: (RIGHT, LEFT)
            }  # словарь - Клавиша: (нужное зн-е, недопустимое зн-е)
            if event.key in key_bindings:
                if game_object.direction != key_bindings.get(event.key)[1]:
                    game_object.next_direction = key_bindings.get(event.key)[0]


def main():
    """
    Главный игровой цикл.

    Управляет:
    - обновлением состояния
    - обработкой событий
    - отрисовкой объектов
    """
    pg.init()
    font = pg.font.SysFont(FONT_NAME, FONT_SIZE)

    snake = Snake()
    apple = Apple(snake.positions)

    running = True
    score = 0

    while running:
        clock.tick(FPS)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_position_func = snake.get_head_position()

        if head_position_func == apple.position:
            snake.change_color()
            snake.add_length()
            apple.randomize_position(snake.positions)
            score += 1
        else:
            snake.delete_last_segment()

        if head_position_func in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            score = 0
            screen.fill(BOARD_BACKGROUND_COLOR)

        text_surface = font.render(f'Счет игры: {score}', True, T_COLOR)
        screen.blit(text_surface, TEXT_POSITION)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
