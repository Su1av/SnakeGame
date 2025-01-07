import pygame
import random
from sys import exit
import time

# Initialize Pygame
pygame.init()

# Set up the display (resizable window)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
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

# Load background image
background_image = pygame.image.load(r'C:\Coding\GitHub\SnakeGame\background.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale it to fit the screen

# Snake body and food positioning
snake_pos = [100, 50]
food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0

# Load and save high score function
def load_high_scores():
    try:
        with open("high_scores.txt", "r") as f:
            high_scores = [line.strip().split(",") for line in f.readlines()]
            return high_scores
    except:
        return []

def save_high_score(player_name, score):
    with open("high_scores.txt", "a") as f:
        f.write(f"{player_name},{score}\n")

def show_high_scores():
    high_scores = load_high_scores()
    high_scores.sort(key=lambda x: int(x[1]), reverse=True)  # Sort by score (high to low)
    return high_scores[:5]  # Return the top 5 high scores

# Game Over function with player name input
def game_over():
    global score
    screen.fill(BLACK)

    # Show Game Over message
    go_surface = game_over_font.render('GAME OVER', True, RED)
    screen.blit(go_surface, (150, 200))
    
    score_surface = font.render(f'Score: {score}', True, TEXT_COLOR)
    screen.blit(score_surface, (50, 300))
    
    # Ask for player's name
    name_prompt_surface = font.render("Enter your name (max 10 characters):", True, TEXT_COLOR)
    screen.blit(name_prompt_surface, (150, 350))
    
    pygame.display.flip()

    player_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Save and exit after entering name
                    if player_name:
                        save_high_score(player_name, score)
                        input_active = False
                        main_menu()  # Go back to the home screen after saving
                    else:
                        player_name = "Anonymous"  # Default name if empty
                        save_high_score(player_name, score)
                        input_active = False
                        main_menu()  # Go back to the home screen after saving

                elif event.key == pygame.K_BACKSPACE:  # Remove character on backspace
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:  # Max 10 characters
                        player_name += event.unicode

                # Display the name being typed
                screen.fill(BLACK)
                screen.blit(go_surface, (150, 200))
                screen.blit(score_surface, (50, 300))
                screen.blit(name_prompt_surface, (150, 350))
                name_surface = font.render(player_name, True, TEXT_COLOR)
                screen.blit(name_surface, (150, 400))
                pygame.display.flip()

# Pause function
def pause_game():
    paused = True
    pause_text = paused_font.render("PAUSED - Press P to Resume or Q to Quit", True, RED)
    screen.blit(pause_text, (150, 250))
    pygame.display.flip()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # If P is pressed, resume
                    paused = False
                elif event.key == pygame.K_q:  # If Q is pressed, quit to menu
                    main_menu()

# Main menu with options and high scores
def main_menu():
    title_text = game_over_font.render("Welcome to Snake Game!", True, TEXT_COLOR)
    new_game_text = font.render("Press 'N' for New Game", True, TEXT_COLOR)
    quit_text = font.render("Press 'Q' to Quit", True, TEXT_COLOR)

    # Show the high scores
    high_scores = show_high_scores()
    high_score_text = font.render("High Scores:", True, TEXT_COLOR)
    
    # Display the menu options
    screen.blit(background_image, (0, 0))  # Display the background image
    screen.blit(title_text, (150, 100))
    screen.blit(new_game_text, (250, 250))
    screen.blit(quit_text, (250, 300))
    screen.blit(high_score_text, (150, 350))

    # Display the top 5 high scores
    y_offset = 400
    for name, score in high_scores:
        score_text = font.render(f'{name}: {score}', True, TEXT_COLOR)
        screen.blit(score_text, (150, y_offset))
        y_offset += 50
    
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Start new game
                    game_loop()
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()

# Main game loop
def game_loop():
    global snake_pos, body, direction, change_to, food_pos, score, screen_width, screen_height
    
    # Reset the game state
    snake_pos = [100, 50]
    food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
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
            food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
        else:
            body.pop()

        # Game Over conditions
        if body[0][0] < 0 or body[0][0] >= screen_width or body[0][1] < 0 or body[0][1] >= screen_height:
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
    main_menu()  # Show the main menu

# Start the game
if __name__ == "__main__":
    main()
