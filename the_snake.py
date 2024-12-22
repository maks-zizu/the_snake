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
    """Объект на игровом поле с определённым цветом и позицией."""

    def __init__(self, body_color=None):
        """Инициализирует объект с начальной позицией и цветом."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def paint_cell(self, position, background_color=None):
        """Отрисовывает ячейку на игровом поле."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if background_color:
            pygame.draw.rect(screen, background_color, rect)

    def draw(self):
        """Отрисовывает объект. Реализуется в дочерних классах."""


class Snake(GameObject):
    """Управляемый игроком объект, который перемещается по полю."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку с начальной позицией и направлением."""
        super().__init__(body_color)
        self.reset()
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки, если есть новое."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позиции сегментов змейки в соответствии с направлением."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head_position = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                             (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        for segment in self.positions:
            self.paint_cell(segment)

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Съедобный объект, который появляется в случайной позиции."""

    def __init__(self, snake_positions=None, body_color=APPLE_COLOR):
        """Инициализирует яблоко на игровом поле."""
        super().__init__(body_color)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions=None):
        """Определяет случайную позицию яблока на поле."""
        while True:
            rand_x = randint(0, GRID_WIDTH - 1)
            rand_y = randint(0, GRID_HEIGHT - 1)
            new_pos = (rand_x * GRID_SIZE, rand_y * GRID_SIZE)
            # Если список позиций змейки не задан или новая позиция яблока
            # не пересекается со змейкой — выходим
            if not snake_positions or new_pos not in snake_positions:
                self.position = new_pos
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.paint_cell(self.position)


def handle_keys(snake):
    """Обрабатывает события ввода с клавиатуры и задаёт новое направление."""
    key_to_direction = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    for event in pygame.event.get():
        """
            !!! try ... except и кастомное исключениe,
            не позволяют пройти автотесты !!!
        """
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Соответствует ли нажатая клавиша возможному направлению
            new_direction = key_to_direction.get(event.key)
            if new_direction:
                # Проверяем, что новое направление не противоположно текущему
                current_direction = snake.direction
                if (new_direction[0] != -current_direction[0]
                        and new_direction[1] != -current_direction[1]):
                    snake.next_direction = new_direction
            elif event.key == pygame.K_ESCAPE:
                sys.exit()


def main():
    """Основная функция игрового цикла."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake_positions=snake.positions)

    while True:
        # Ограничиваем FPS
        clock.tick(SPEED)
        # 1. Сначала обрабатываем нажатия
        handle_keys(snake)
        # 2. Обновляем направление
        snake.update_direction()
        # 3. Двигаем змейку
        snake.move()

        # Сохраним позицию головы змейки в переменную,
        # чтобы не вызывать get_head_position() несколько раз
        head_position = snake.get_head_position()

        # 4. Проверяем столкновение с яблоком
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # 5. Проверяем столкновение со своим телом
        if head_position in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        # Очищаем экран и отрисовываем свежую картинку
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        # 6. Обновляем экран
        pygame.display.update()


if __name__ == '__main__':
    main()
