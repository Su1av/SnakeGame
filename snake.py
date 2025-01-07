import pygame
import random
from sys import exit
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (50, 150, 255)  # Button color
BUTTON_HOVER_COLOR = (100, 200, 255)  # Button hover color
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.SysFont('Arial', 30)
game_over_font = pygame.font.SysFont('Arial', 90)
paused_font = pygame.font.SysFont('Arial', 50)
home_font = pygame.font.SysFont('Arial', 40)

# Snake body and food positioning
snake_pos = [100, 50]
food_pos = [random.randrange(1, (800//10)) * 10, random.randrange(1, (600//10)) * 10]
body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0

# Load and save high score function
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Game Over function
def game_over():
    global score
    high_score = load_high_score()
    
    # Save the high score if necessary
    if score > high_score:
        save_high_score(score)
        high_score = score
    
    go_surface = game_over_font.render('GAME OVER', True, RED)
    screen.blit(go_surface, (150, 200))
    
    score_surface = font.render(f'Score: {score}', True, TEXT_COLOR)
    screen.blit(score_surface, (50, 300))
    
    high_score_surface = font.render(f'High Score: {high_score}', True, TEXT_COLOR)
    screen.blit(high_score_surface, (50, 350))
    
    restart_surface = font.render("Press 'R' to Restart", True, TEXT_COLOR)
    screen.blit(restart_surface, (50, 400))
    
    pygame.display.flip()
    time.sleep(1)

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    game_loop()

# Pause function
def pause_game():
    paused = True
    pause_text = paused_font.render("PAUSED - Press P to Resume", True, RED)
    screen.blit(pause_text, (200, 250))
    pygame.display.flip()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # If P is pressed, resume
                    paused = False

# Home screen with a Start Game button
def home_screen():
    title_text = game_over_font.render("Welcome to Snake Game!", True, TEXT_COLOR)
    instructions_text = font.render("Press any key or click 'Start Game' to begin", True, TEXT_COLOR)
    
    # Create Start Game button
    button_rect = pygame.Rect(300, 350, 200, 50)
    mouse_pos = pygame.mouse.get_pos()

    # Change button color on hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    button_text = home_font.render("Start Game", True, TEXT_COLOR)
    screen.blit(button_text, (button_rect.x + 50, button_rect.y + 10))
    
    screen.fill(BLACK)
    screen.blit(title_text, (150, 150))
    screen.blit(instructions_text, (150, 250))
    pygame.display.flip()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                waiting_for_input = False
                game_loop()  # Start the game after the player presses a key
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # If the button is clicked
                    waiting_for_input = False
                    game_loop()  # Start the game after clicking the button

# Main game loop
def game_loop():
    global snake_pos, body, direction, change_to, food_pos, score
    
    # Reset the game state
    snake_pos = [100, 50]
    food_pos = [random.randrange(1, (800//10)) * 10, random.randrange(1, (600//10)) * 10]
    body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                if event.key == pygame.K_p:  # Pause the game
                    pause_game()

        # Update the snake direction according to `change_to`
        if change_to == 'UP':
            snake_pos[1] -= 10
        if change_to == 'DOWN':
            snake_pos[1] += 10
        if change_to == 'LEFT':
            snake_pos[0] -= 10
        if change_to == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_pos = [random.randrange(1, (800//10)) * 10, random.randrange(1, (600//10)) * 10]
        else:
            body.pop()

        # Game Over conditions
        if body[0][0] < 0 or body[0][0] >= 800 or body[0][1] < 0 or body[0][1] >= 600:
            game_over()

        # Check if the snake collides with itself
        for block in body[1:]:
            if body[0] == block:
                game_over()

        # Drawing the elements on screen
        screen.fill(BLACK)
        for pos in body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Display score
        score_surface = font.render(f'Score: {score}', True, TEXT_COLOR)
        screen.blit(score_surface, (10, 10))

        # Update the display
        pygame.display.update()
        clock.tick(20)

# Main entry point
def main():
    home_screen()  # Show the home screen before the game starts

# Start the game
if __name__ == "__main__":
    main()
