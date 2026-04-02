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

def draw_time_boosts(boosts):
    for boost in boosts:
        x, y, alpha = boost

        text = font.render("+3s", True, (0, 255, 100))
        text.set_alpha(alpha)
        screen.blit(text, (x, y))

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

    time_boost= []
    boostx = None
    boosty = None
    boost_spawn_time = 0
    boost_duration = 5000
    boost_active = False

    while not game_over:
        while game_close == True:
            screen.fill(black)
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            time_left = max(0, time_limit - elapsed_time)
            
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

        current_time = pygame.time.get_ticks()

        #Spawns a boost about every 7 seconds if none exist
        if not boost_active and current_time - boost_spawn_time > 7000:
            boostx = round(random.randrange(0, width - snake_block) / 10.0)
            boosty = round(random.randrange(0, height - snake_block) / 10.0)
            boost_spawn_time = current_time
            boost_active = True

        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

        if boost_active:
            pygame.draw.rect(screen, (0, 255, 255), [boostx, boosty, snake_block, snake_block])
            pygame.draw.rect(screen, white, [boostx, boosty, snake_block, snake_block], 1)
            if boost_active and current_time - boost_spawn_time > boost_duration:
                boost_active = False


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

        #Updates the boosts
        for boost in time_boost:
            boost[1] -= 2 #move up
            boost[2] -= 8 #fade out
        # Remove faded boosts
        time_boost = [b for b in time_boost if b[2] > 0]
        #Draw boosts
        draw_time_boosts(time_boost)


        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_left = time_limit - elapsed_time

        if time_left <= 0:
            game_close = True

        show_time(max(0, time_left))

        pygame.display.update()

        if boost_active and int(x1) == int(boostx) and int(y1) == int(boosty):
            start_time -= 3000
            boost_active = False
            time_boost.append([x1 - 10, y1 - 10, 255])


        if int(x1) == int(foodx) and int(y1) == int(foody):
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1
            start_time -= 3000 # 3000 ms is 3 seconds

            time_boost.append([x1 - 10, y1 - 10, 255]) # Thank you ChatGPT... x, y, opacity
        clock.tick(snake_speed)
        
    pygame.quit()
    sys.exit()
gameLoop()