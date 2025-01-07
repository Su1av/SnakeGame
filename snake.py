import pygame
from sys import exit
import time

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

def draw_score(screen, score):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def draw_snake(screen, snake):
    for pos in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

def draw_food(screen, food):
    pygame.draw.rect(screen, WHITE, pygame.Rect(food[0], food[1], 10, 10))

def game_over():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render('GAME OVER', True, WHITE)
    screen.blit(text, (250, 300))
    pygame.display.update()
    time.sleep(2)
    exit()

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
        time.sleep(0.1)  # Avoid CPU overload while paused

def main():
    running = True
    direction = 'RIGHT'
    snake = [[80, 50], [70, 50], [60, 50]]
    food = [300, 300]
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_p:
                    pause_game()

        # Move snake
        if direction == 'UP':
            snake[0][1] -= 10
        elif direction == 'DOWN':
            snake[0][1] += 10
        elif direction == 'LEFT':
            snake[0][0] -= 10
        elif direction == 'RIGHT':
            snake[0][0] += 10

        # Check for food collision
        if snake[0] == food:
            score += 1
            while True:  # Generate new food position that doesn't collide with the snake
                new_food = [pygame.randint(0, 79) * 10, pygame.randint(0, 59) * 10]
                if new_food not in snake:
                    food = new_food
                    break
            snake.append([snake[-1][0], snake[-1][1]])  # Grow the snake by one block
        else:
            snake.pop()  # Remove last block if no collision

        # Check for game over conditions
        if snake[0][0] < 0 or snake[0][0] >= 800 or snake[0][1] < 0 or snake[0][1] >= 600:
            game_over()
        elif snake[0] in snake[1:]:  # Check for self-collision
            game_over()

        screen.fill(BLACK)
        draw_score(screen, score)
        draw_snake(screen, snake)
        draw_food(screen, food)
        pygame.display.update()
        clock.tick(10)  # Game speed is 10 frames per second

if __name__ == '__main__':
    main()
