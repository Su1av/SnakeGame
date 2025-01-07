import pygame
import random
import time
from sys import exit

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Set up initial screen properties
screen_width = 800
screen_height = 600
fullscreen = True  # Start in fullscreen mode
fps = 15  # Default FPS (difficulty)

# Create screen object (Fullscreen by default)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
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

# Load sound files
eat_sound = pygame.mixer.Sound("eat_sound.mp3")  # Replace with your actual file path
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")  # Replace with your actual file path

# Snake body and food positioning
snake_pos = [100, 50]
food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0


def get_font(size):
    """Returns a font of a given size"""
    return pygame.font.SysFont('Arial', size)


def load_high_scores():
    """Load high scores from file"""
    try:
        with open("high_scores.txt", "r") as f:
            high_scores = [line.strip().split(",") for line in f.readlines()]
            high_scores = [(name, int(score)) for name, score in high_scores]  # Convert score to integer
            return high_scores
    except:
        return []


def save_high_scores(high_scores):
    """Save high scores to file"""
    with open("high_scores.txt", "w") as f:
        for name, score in high_scores:
            f.write(f"{name},{score}\n")


def update_high_scores(player_name, score):
    """Update the high scores list with the player's score"""
    high_scores = load_high_scores()
    for i, (name, old_score) in enumerate(high_scores):
        if name == player_name:
            if score > old_score:
                high_scores[i] = (name, score)
            return high_scores
    high_scores.append((player_name, score))
    return high_scores


def show_high_scores():
    """Return the top 5 high scores"""
    high_scores = load_high_scores()
    high_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score (high to low)
    return high_scores[:5]


def display_text(text, font, color, x, y):
    """Helper function to render and display text on the screen"""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def game_over():
    """Handle game over logic"""
    global score
    screen.fill(BLACK)
    display_text('GAME OVER', game_over_font, RED, 150, 200)
    display_text(f'Score: {score}', font, TEXT_COLOR, 50, 300)

    display_text("Enter your name (max 10 characters):", font, TEXT_COLOR, 150, 350)
    pygame.display.flip()

    # Play the game over sound
    game_over_sound.play()  # Play the game over sound

    player_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name:
                        high_scores = update_high_scores(player_name, score)
                    else:
                        high_scores = update_high_scores("Anonymous", score)
                    save_high_scores(high_scores)
                    input_active = False
                    main_menu()  # Return to main menu

                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:
                        player_name += event.unicode

                screen.fill(BLACK)
                display_text('GAME OVER', game_over_font, RED, 150, 200)
                display_text(f'Score: {score}', font, TEXT_COLOR, 50, 300)
                display_text("Enter your name (max 10 characters):", font, TEXT_COLOR, 150, 350)
                display_text(player_name, font, TEXT_COLOR, 150, 400)
                pygame.display.flip()


def pause_game():
    """Handle pause logic"""
    paused = True
    screen.fill(BLACK)
    display_text("PAUSED - Press P to Resume or Q to Quit", paused_font, RED, 150, 250)
    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    main_menu()


def main_menu():
    """Main menu of the game"""
    screen.fill(BLACK)
    display_text("Welcome to Snake Game!", game_over_font, TEXT_COLOR, 150, 100)
    display_text("Press 'N' for New Game", font, TEXT_COLOR, 250, 250)
    display_text("Press 'H' for High Scores", font, TEXT_COLOR, 250, 300)
    display_text("Press 'S' for Settings", font, TEXT_COLOR, 250, 350)
    display_text("Press 'I' for Instructions", font, TEXT_COLOR, 250, 400)
    display_text("Press 'Q' to Quit", font, TEXT_COLOR, 250, 450)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    game_loop()
                elif event.key == pygame.K_h:
                    high_scores_page()
                elif event.key == pygame.K_s:
                    settings_menu()
                elif event.key == pygame.K_i:
                    instructions_page()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


def high_scores_page():
    """Display high scores"""
    screen.fill(BLACK)

    high_scores = show_high_scores()
    
    display_text("High Scores", game_over_font, TEXT_COLOR, 300, 50)
    
    y_offset = 150
    for name, score in high_scores:
        display_text(f'{name}: {score}', font, TEXT_COLOR, 300, y_offset)
        y_offset += 50

    display_text("Press 'B' to Back to Menu", font, TEXT_COLOR, 250, y_offset + 50)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()


def instructions_page():
    """Display the game instructions"""
    screen.fill(BLACK)
    display_text("Snake Game Instructions", game_over_font, TEXT_COLOR, 200, 50)

    instructions = [
        "Use Arrow Keys to Move",
        "Eat the Red Food to Grow",
        "Avoid Hitting the Walls and Yourself",
        "Press P to Pause",
        "Press Q to Quit During Game"
    ]
    y_offset = 150
    for line in instructions:
        display_text(line, font, TEXT_COLOR, 200, y_offset)
        y_offset += 40

    display_text("Press 'B' to Back to Menu", font, TEXT_COLOR, 250, y_offset + 50)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()


def game_loop():
    """Main game loop"""
    global snake_pos, body, direction, change_to, food_pos, score, screen_width, screen_height

    snake_pos = [100, 50]
    food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
    body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_p:
                    pause_game()

        direction = change_to

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
        else:
            body.pop()

        if snake_pos[0] < 0 or snake_pos[0] >= screen_width or snake_pos[1] < 0 or snake_pos[1] >= screen_height:
            game_over()

        screen.fill(BLACK)
        for block in body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        display_text(f"Score: {score}", font, WHITE, 10, 10)

        pygame.display.update()
        clock.tick(fps)


def settings_menu():
    """Settings menu for toggling fullscreen and difficulty"""
    global screen, fullscreen, fps, screen_width, screen_height

    settings_font = get_font(40)
    settings_text = settings_font.render("Settings", True, TEXT_COLOR)
    settings_rect = settings_text.get_rect(center=(screen_width // 2, screen_height // 5))

    fullscreen_text = get_font(30).render(f"Fullscreen: {'ON' if fullscreen else 'OFF'}", True, TEXT_COLOR)
    fullscreen_rect = fullscreen_text.get_rect(center=(screen_width // 2, screen_height // 2.5))

    difficulty_text = get_font(30).render(f"Difficulty: {'Easy' if fps == 15 else 'Hard'}", True, TEXT_COLOR)
    difficulty_rect = difficulty_text.get_rect(center=(screen_width // 2, screen_height // 2))

    back_text = get_font(30).render("Press 'B' to Back to Menu", True, TEXT_COLOR)
    back_rect = back_text.get_rect(center=(screen_width // 2, screen_height // 1.5))

    # Draw settings screen
    screen.fill(BLACK)
    screen.blit(settings_text, settings_rect)
    screen.blit(fullscreen_text, fullscreen_rect)
    screen.blit(difficulty_text, difficulty_rect)
    screen.blit(back_text, back_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                    settings_menu()

                elif event.key == pygame.K_d:
                    fps = 25 if fps == 15 else 15
                    settings_menu()

                elif event.key == pygame.K_b:
                    main_menu()


# Start the game with the main menu
main_menu()
