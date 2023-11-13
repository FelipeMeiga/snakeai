import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

pygame.init()

dis_width = 800
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jogo da Cobrinha AI')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 15

font = pygame.font.SysFont(None, 35)

white = (255, 255, 255)
green = (0, 255, 0)
blue_dark = (0, 0, 139)
red = (255, 0, 0)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
yellow = (0, 255, 255)

class snake:
    def __init__(self):
        self.length = 1
        self.snake_body = []
        self.head_x = random.choice(range(0, int(dis_width/snake_block)))
        self.head_y = random.choice(range(0, int(dis_height/snake_block)))
        self.snake_body.append((self.head_x, self.head_y))
        print("Snake object initialized...")

    def print_snake_info(self):
        for i, tup in enumerate(self.snake_body):
            if i == 0:
                print("X = ", tup[0], "Y = ", tup[1], " <- Head")
            else:
                print("X = ", tup[0], "Y = ", tup[1])
    
    def get_head_position(self):
        return self.head_x, self.head_y
    
    def update_head_position(self, new_x, new_y):
        self.head_x = new_x
        self.head_y = new_y
        self.snake_body.insert(0, (new_x, new_y))
        if len(self.snake_body) > self.length:
            self.snake_body.pop()

    def update_length(self):
        self.length += 1
        self.snake_body.insert(0, (self.head_x, self.head_y))

    def check_collision(self):
        head = self.snake_body[0]
        for segment in self.snake_body[1:]:
            if head == segment:
                return True
        return False
    
    def draw(self):
        for i, tup in enumerate(self.snake_body):
            if i == 0:
                color = red
            else:
                color = blue_dark
            pygame.draw.rect(dis, color, [tup[0]*snake_block, tup[1]*snake_block, snake_block, snake_block])

snake = snake()
snake.print_snake_info()

def draw_grid():
    for x in range(0, dis_width, snake_block):
        for y in range(0, dis_height, snake_block):
            rect = pygame.Rect(x, y, snake_block, snake_block)
            pygame.draw.rect(dis, dark_gray, rect, 1)

def calculate_distance(food_x, food_y):
    head_pos = snake.get_head_position()
    return (head_pos[0] - food_x, head_pos[1] - food_y)

def gameloop():
    game_over = False
    game_close = False

    delta_x = 0
    delta_y = 0

    food_x = random.choice(range(0, int(dis_width/snake_block)))
    food_y = random.choice(range(0, int(dis_height/snake_block)))

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    delta_x = -1
                    delta_y = 0
                elif event.key == pygame.K_RIGHT:
                    delta_x = 1
                    delta_y = 0
                elif event.key == pygame.K_UP:
                    delta_x = 0
                    delta_y = -1
                elif event.key == pygame.K_DOWN:
                    delta_x = 0
                    delta_y = 1

        head_pos = snake.get_head_position()

        snake.update_head_position(head_pos[0] + delta_x, head_pos[1] + delta_y)

        if snake.check_collision():
            game_over = True

        dis.fill(gray)
        draw_grid()
        snake.draw()
        pygame.draw.rect(dis, green, [food_x*snake_block, food_y*snake_block, snake_block, snake_block])
        pygame.display.update()
        clock.tick(snake_speed)

        if head_pos[0] + delta_x >= dis_width/snake_block or head_pos[0] + delta_x < 0 or head_pos[1] + delta_y >= dis_height/snake_block or head_pos[1] + delta_y <= 0:
            game_over = True

        if head_pos[0] + delta_x == food_x and head_pos[1] + delta_y == food_y:
            food_x = random.choice(range(0, int(dis_width/snake_block)))
            food_y = random.choice(range(0, int(dis_height/snake_block)))
            snake.update_length()
        
        print(calculate_distance(food_x, food_y))

    pygame.quit()
    quit()

gameloop()
