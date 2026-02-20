from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CENTER_SCREEN_WIDTH = SCREEN_WIDTH // 2
CENTER_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Snake')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self):
        """
        Инициализирует объект с позицией в центре экрана
        и цветом по умолчанию.
        """
        self.position = CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Метод отрисовки класса (переопределяется в дочерних классах)."""
        pass


class Apple(GameObject):
    """Класс яблочка."""

    def __init__(self):
        """
        Создает яблоко в случаной позиции
        и задает ему цвет.
        """
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """
        Генерирует случайную позицию на игровом поле,
        кратную размеру сетки.
        """
        return (
            GRID_SIZE * randint(0, GRID_WIDTH - 1),
            GRID_SIZE * randint(0, GRID_HEIGHT - 1)
        )

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT)]
        self.direction = RIGHT
        self.next_direction = None
        self.score = 0

    def update_direction(self):
        """
        Обновляет направление движения змейки,
        если была нажата клавиша.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позиция головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        self.positions = [(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT)]
        self.direction = RIGHT
        self.next_direction = None
        self.score = 0
        self.length = 1
        self.body_color = SNAKE_COLOR

    def draw(self, i=0):
        """Отрисовывает сегмент змейки."""
        head_rect = pygame.Rect(self.positions[i], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def add(self):
        """Добавление сегмента."""
        x, y = self.positions[-1]
        self.positions.append((x + 20, y))

    def check_board(self, x, y):
        """
        Проверяет выход змейки за границы экрана
        и переносит ее на противоположную сторону.
        """
        if x >= SCREEN_WIDTH:
            x = 0
        elif x + GRID_SIZE <= 0:
            x = SCREEN_WIDTH
        if y >= SCREEN_HEIGHT:
            y = 0
        elif y + GRID_SIZE <= 0:
            y = SCREEN_HEIGHT
        return x, y

    def move(self):
        """
        Двигает змейку на одну клетку
        в текущем направлении.
        """
        x, y = self.get_head_position()
        x1, y1 = self.direction
        x += x1 * GRID_SIZE
        y += y1 * GRID_SIZE
        x, y = self.check_board(x, y)
        self.positions.insert(0, (x, y))
        self.positions = self.positions[:-1]


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш и меняет
    направление движения объекта.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Главный игровой цикл.
    Управляет:
    - обновлением состояния
    - обработкой событий
    - отрисовко объектов
    """
    pygame.init()
    # Шрифт
    font = pygame.font.SysFont('Arial', 16)

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        apple.draw()
        handle_keys(snake)
        for i in range(len(snake.positions)):
            snake.draw(i)
        snake.move()
        if snake.get_head_position() == apple.position:  # Если съедаем яблоко
            snake.add()  # Добавляем секцию
            snake.body_color = (
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)
            )  # Меняем цвет змейки)
            apple.position = (
                GRID_SIZE * randint(0, GRID_WIDTH - 1),
                GRID_SIZE * randint(0, GRID_HEIGHT - 1)
            )
            snake.score += 1  # счет игры
            snake.length += 1

        # Если голова заденет тело
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Рендеринг текста
        text_surface = font.render(f'Счет игры: {snake.score}', True, T_COLOR)

        # Отображение текста
        screen.blit(text_surface, (500, 30))

        snake.update_direction()
        pygame.display.update()


if __name__ == '__main__':
    main()
