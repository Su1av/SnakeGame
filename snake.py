import pygame
import random
from sys import exit
import time

# Initialize Pygame
pygame.init()

# Load sound effects and music
pygame.mixer.music.load("background_music.mp3")  # Background music file
pygame.mixer.music.play(-1, 0.0)  # Loop forever

eat_sound = pygame.mixer.Sound("eat_sound.mp3")  # Sound when food is eaten
death_sound = pygame.mixer.Sound("death_sound.mp3")  # Sound when the snake dies

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

# Font resizing function
def get_font(size):
    return pygame.font.SysFont('Arial', size)

# Snake body and food positioning
snake_pos = [100, 50]
food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0

# Load and save high scores
def load_high_scores():
    try:
        with open("high_scores.txt", "r") as f:
            high_scores = [line.strip().split(",") for line in f.readlines()]
            high_scores = [(name, int(score)) for name, score in high_scores]  # Convert score to integer
            return high_scores
    except:
        return []

def save_high_scores(high_scores):
    with open("high_scores.txt", "w") as f:
        for name, score in high_scores:
            f.write(f"{name},{score}\n")

# Update high score (overwrite if score is higher)
def update_high_scores(player_name, score):
    high_scores = load_high_scores()

    # Check if the player's name already exists in the high scores
    for i, (name, old_score) in enumerate(high_scores):
        if name == player_name:
            if score > old_score:  # If the new score is higher, update it
                high_scores[i] = (name, score)
            return high_scores

    # If the player doesn't exist, add a new entry
    high_scores.append((player_name, score))
    return high_scores

def show_high_scores():
    high_scores = load_high_scores()
    high_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score (high to low)
    return high_scores[:5]  # Return the top 5 high scores

# Game Over function with player name input
def game_over():
    global score
    screen.fill(BLACK)

    # Show Game Over message
    go_font = get_font(screen_height // 8)
    go_surface = go_font.render('GAME OVER', True, RED)
    go_rect = go_surface.get_rect(center=(screen_width // 2, screen_height // 3))
    screen.blit(go_surface, go_rect)
    
    score_font = get_font(screen_height // 20)
    score_surface = score_font.render(f'Score: {score}', True, TEXT_COLOR)
    score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(score_surface, score_rect)
    
    # Ask for player's name
    name_prompt_font = get_font(screen_height // 25)
    name_prompt_surface = name_prompt_font.render("Enter your name (max 10 characters):", True, TEXT_COLOR)
    name_prompt_rect = name_prompt_surface.get_rect(center=(screen_width // 2, screen_height // 1.5))
    screen.blit(name_prompt_surface, name_prompt_rect)
    
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
                        # Update high scores and save
                        high_scores = update_high_scores(player_name, score)
                        save_high_scores(high_scores)
                        input_active = False
                        main_menu()  # Go back to the home screen after saving
                    else:
                        player_name = "Anonymous"  # Default name if empty
                        high_scores = update_high_scores(player_name, score)
                        save_high_scores(high_scores)
                        input_active = False
                        main_menu()  # Go back to the home screen after saving

                elif event.key == pygame.K_BACKSPACE:  # Remove character on backspace
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:  # Max 10 characters
                        player_name += event.unicode

                # Display the name being typed
                screen.fill(BLACK)
                screen.blit(go_surface, go_rect)
                screen.blit(score_surface, score_rect)
                screen.blit(name_prompt_surface, name_prompt_rect)
                name_surface = name_prompt_font.render(player_name, True, TEXT_COLOR)
                name_rect = name_surface.get_rect(center=(screen_width // 2, screen_height // 1.25))
                screen.blit(name_surface, name_rect)
                pygame.display.flip()

# Pause function
def pause_game():
    paused = True
    pause_font = get_font(screen_height // 20)
    pause_text = pause_font.render("PAUSED - Press P to Resume or Q to Quit", True, RED)
    pause_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(pause_text, pause_rect)
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
    title_font = get_font(screen_height // 10)
    title_text = title_font.render("Welcome to Snake Game!", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 5))

    new_game_font = get_font(screen_height // 20)
    new_game_text = new_game_font.render("Press 'N' for New Game", True, TEXT_COLOR)
    new_game_rect = new_game_text.get_rect(center=(screen_width // 2, screen_height // 2))

    high_scores_font = get_font(screen_height // 20)
    high_scores_text = high_scores_font.render("Press 'H' for High Scores", True, TEXT_COLOR)
    high_scores_rect = high_scores_text.get_rect(center=(screen_width // 2, screen_height // 1.5))

    quit_font = get_font(screen_height // 20)
    quit_text = quit_font.render("Press 'Q' to Quit", True, TEXT_COLOR)
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 1.2))

    # Show the menu options
    screen.fill(BLACK)  # Fill the screen with black background
    screen.blit(title_text, title_rect)
    screen.blit(new_game_text, new_game_rect)
    screen.blit(high_scores_text, high_scores_rect)
    screen.blit(quit_text, quit_rect)
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
                elif event.key == pygame.K_h:  # View high scores
                    high_scores_page()
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()

# High Scores page
def high_scores_page():
    screen.fill(BLACK)  # Fill the screen with black background

    high_scores = show_high_scores()
    
    title_font = get_font(screen_height // 10)
    title_text = title_font.render("High Scores", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 5))
    screen.blit(title_text, title_rect)
    
    y_offset = screen_height // 3
    score_font = get_font(screen_height // 20)
    for name, score in high_scores:
        score_text = score_font.render(f'{name}: {score}', True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(screen_width // 2, y_offset))
        screen.blit(score_text, score_rect)
        y_offset += 50

    back_font = get_font(screen_height // 20)
    back_text = back_font.render("Press 'B' to Back to Menu", True, TEXT_COLOR)
    back_rect = back_text.get_rect(center=(screen_width // 2, y_offset + 50))
    screen.blit(back_text, back_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Return to the main menu
                    main_menu()

# Main game loop with fixed direction keys
def game_loop():
    global snake_pos, body, direction, change_to, food_pos, score, screen_width, screen_height

    # Reset the game state
    snake_pos = [100, 50]
    food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
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

            # Check for key presses and prevent opposite direction movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':  # Prevent going DOWN when going UP
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':  # Prevent going UP when going DOWN
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':  # Prevent going RIGHT when going LEFT
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':  # Prevent going LEFT when going RIGHT
                    change_to = 'RIGHT'
                elif event.key == pygame.K_p:  # Pause the game
                    pause_game()

        # Update the snake direction according to `change_to`
        direction = change_to

        # Move the snake body
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
            eat_sound.play()  # Play the sound when food is eaten        
        else:
            body.pop()

        if snake_pos[0] < 0 or snake_pos[0] >= screen_width or snake_pos[1] < 0 or snake_pos[1] >= screen_height:
            death_sound.play()  # Play the death sound when the snake hits the wall
            game_over()

        # Draw everything
        screen.fill(BLACK)  # Fill the screen with black background
        for block in body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Display score
        score_font = get_font(screen_height // 20)
        score_surface = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))

        pygame.display.update()

        # Frame Per Second / Refresh Rate
        clock.tick(20)

# Start the game with the main menu
main_menu()
