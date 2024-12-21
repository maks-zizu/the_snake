import sys
import pygame
from random import choice, randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
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

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для всех игровых объектов."""

    def __init__(self, body_color=None):
        """
        Инициализирует объект с начальной позицией и цветом.
        Args:
            body_color (tuple, optional): Цвет объекта в формате RGB.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def paint_cell(self, position, background_color=None):
        """
        Отрисовывает ячейку на игровом поле.
        Args:
            position (tuple): Координаты ячейки.
            background_color (tuple, optional): Цвет фона ячейки.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if background_color:
            pygame.draw.rect(screen, background_color, rect)

    def draw(self):
        """
        Метод для отрисовки объектов на экране.
        Реализуется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко для игры 'Змейка'."""

    def __init__(self, snake=None, body_color=APPLE_COLOR):
        """
        Инициализирует яблоко на игровом поле.
        Args:
            snake (Snake, optional): Объект змейки для проверки пересечений.
            body_color (tuple): Цвет яблока в формате RGB.
        """
        super().__init__(body_color)
        self.randomize_position(snake)

    def randomize_position(self, snake=None):
        """
        Определяет случайную позицию яблока на игровом поле.
        Args:
            snake (Snake, optional): Объект змейки для проверки пересечений.
        """
        while snake and self.position in snake.positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.paint_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку для игры."""

    def __init__(self, body_color=SNAKE_COLOR):
        """
        Инициализирует змейку с начальной позицией и направлением.
        Args:
            body_color (tuple): Цвет змейки в формате RGB.
        """
        super().__init__(body_color)
        self.reset()
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """
        Возвращает текущую позицию головы змейки.
        Returns:
            tuple: Координаты головы змейки.
        """
        return self.positions[0]

    def move(self):
        """Обновляет позиции сегментов змейки в соответствии с направлением."""
        head_x, head_y = self.get_head_position()
        self.positions.insert(0, ((head_x + self.direction[0]
                                   * GRID_SIZE) % SCREEN_WIDTH,
                                  (head_y + self.direction[1]
                                   * GRID_SIZE) % SCREEN_HEIGHT))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        self.paint_cell(self.get_head_position())
        if self.last:
            self.paint_cell(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """
    Обрабатывает события ввода с клавиатуры.
    Args:
        game_object (GameObject):
        Игровой объект, для которого обрабатываются события.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                sys.exit()


def main():
    """Основная функция игрового цикла."""
    pygame.init()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple(snake)
    apple.draw()

    while True:
        clock.tick(SPEED)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
            apple.draw()

        if (snake.get_head_position() in snake.positions[1:]
                or snake.get_head_position() == snake.last):
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.draw()

        snake.move()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()

        pygame.display.update()


if __name__ == '__main__':
    main()
