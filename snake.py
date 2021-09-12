"""
The classic game of snake. Made with python
and pygame.


Date Modified:  Sep 12, 2021
Author: https://www.github.com/benni347
"""

# Imports
import pygame
import random
from enum import Enum
from collections import namedtuple

# init pygame
pygame.init()

# use the arial font
font = pygame.font.Font("arial.ttf", 25)


class Direction(Enum):
    """
    Direction class representing the direction.
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


point = namedtuple("point", "x, y")

# RGB Color Vars
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# Game vars
BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:
    """
    SnakeGame class representing the game.
    """

    def __init__(self, width=640, height=480):
        """
        Initialize the object
        :param width: starting x pos (int)
        :param height: starting y pos (int)
        :return: None
        """
        self.width = width
        self.height = height
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = point(self.width/2, self.height/2)
        self.snake = [self.head,
                      point(self.head.x-BLOCK_SIZE, self.head.y),
                      point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        """
        Place the food somewhere on the screen.
        :return: None
        """
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE  # random x pos for spawning food (int)
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE  # random y pos for spawning food (int)
        self.food = point(x, y)
        if self.food in self.snake:  # this will check if food would spawn in the snake if yes it tries again
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the window when the x is pressed
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # change snake direction to LEFT
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:  # change snake direction to RIGHT
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:  # change snake direction to UP
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:  # change snake direction to DOWn
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits self
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        """
        Update the user interface.
        :return: None
        """
        self.display.fill(BLACK)

        # draw the snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # draw the food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # draw the score in the upper left
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        """
        Move the snake head
        :return: None
        """
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score: ', score)

    pygame.quit()