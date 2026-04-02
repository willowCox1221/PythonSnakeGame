import pygame
import random
import sys

pygame.init()
print("Program started")

width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)

snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

def show_score(score):
    value = font.render("Score: " + str(score), True, white)
    screen.blit(value, [10, 10])

def show_time(time_left):
    display_time = max(0, int(time_left))
    value = font.render("Time: " + str(display_time), True, white)
    screen.blit(value, [width - 140, 10]) #This line puts it in the top right of the screen

def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x [1], block, block])

def message(msg, color):
    mesg = font.render(msg, True, color)
    screen.blit(mesg, [width/6, height/3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0 
    y1_change = 0 

    snake_List = []
    length_of_snake = 1
    score = 0
    start_time = pygame.time.get_ticks()
    time_limit = 30

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close == True:
            screen.fill(black)
            time_left = max(0, time_limit - (pygame.time.get_ticks() - start_time)) / 1000
            
            message(f"You Lost! Score: {score} Time: {int(time_left)}  Q-Quit C-Play Again", red)
            show_time(time_left)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0 
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0 
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
            
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_List.append(snake_Head)

        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        show_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1

        clock.tick(snake_speed)
        
    pygame.quit()
    sys.exit()
gameLoop()