import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOUR = (24, 105, 120)
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 30) * SIZE
        self.y = random.randint(1, 18) * SIZE
        # size of surface divided by size of one block head minus 2


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.snake_block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "right"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((24, 105, 120))
        for i in range(self.length):
            self.parent_screen.blit(self.snake_block, (self.x[i], self.y[i]))

        pygame.display.flip()  # Update the full display Surface to the screen, the lines of code (wherever display changes) will not work if this line is never called.

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.fill(BACKGROUND_COLOUR)
        self.snake = Snake(
            self.surface, 1
        )  # Object of Snake class created inside Game class constructor
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.wall_x = (0, 1300)
        self.wall_y = (0, 800)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colliding with apple
        if self.is_collision(
            self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y
        ):
            # print("Collision Detected")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                # print("game over")
                raise "Game Over"

        # Snake colliding with wall
        if (
            self.snake.x[0] < 0
            or self.snake.x[0] > WINDOW_WIDTH
            or self.snake.y[0] < 0
            or self.snake.y[0] > WINDOW_HEIGHT
        ):
            raise "Game Over"

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (1100, 10))

    def show_gameover(self):
        self.surface.fill(BACKGROUND_COLOUR)
        font = pygame.font.SysFont("arial", 30)
        gameover = font.render(
            f"Game over! Your score was: {self.snake.length}", True, (200, 200, 200)
        )
        self.surface.blit(gameover, (200, 300))
        retry = font.render("To play again, press Enter", True, (200, 200, 200))
        self.surface.blit(retry, (200, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_gameover()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()

    # pygame.display.flip()
