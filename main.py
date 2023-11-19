import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from enum import Enum
import numpy as np
from collections import namedtuple

pygame.init()

class Directions(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", "x, y")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 139)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
YELLOW = (0, 255, 255)

BLOCK_SIZE = 20
SNAKE_SPEED = 40

font = pygame.font.SysFont(None, 35)

class SnakeGameAi:
    def __init__(self, w=800, h=800):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Directions.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SNAKE_SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(GRAY)
        self.draw_grid()
        head = self.snake[0]
        for pt in self.snake:
            if pt == head:
                pygame.draw.rect(self.display, RED, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  
            else:  
                pygame.draw.rect(self.display, DARK_BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    
    def draw_grid(self):
        for x in range(0, self.w, BLOCK_SIZE):
            for y in range(0, self.w, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.display, DARK_GRAY, rect, 1)

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Directions.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Directions.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Directions.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Directions.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
