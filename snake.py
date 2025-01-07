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
BUTTON_COLOR = (66, 133, 244)  # Soft blue color for buttons
BUTTON_HOVER_COLOR = (33, 150, 243)  # Lighter blue for hover effect
TEXT_COLOR = (255, 255, 255)
DARK_GRAY = (50, 50, 50)  # For background or subtle elements
LIGHT_GRAY = (220, 220, 220)  # For softer contrast on text and elements

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


def draw_button(text, font, color, x, y, width, height):
    """Draw a rounded button with a text on it"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    radius = 15  # Rounded corner radius

    # Draw button with rounded corners
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect, border_radius=radius)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=radius)

    # Render the text and place it on the button
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def draw_rounded_button(text, font, color, x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    radius = 20  # rounded corners

    # Change color on hover
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect, border_radius=radius)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=radius)

    # Center the text in the button
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def hover_effect_button(button_text, font, color, x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Change color or size on hover
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Add text with hover effect (increased size when hovered)
    text_surface = font.render(button_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    if button_rect.collidepoint(mouse_x, mouse_y):
        text_rect.center = (text_rect.centerx, text_rect.centery - 2)
    screen.blit(text_surface, text_rect)




def fade_out():
    """Fades out the screen to black."""
    surface = pygame.Surface((screen_width, screen_height))
    surface.fill(BLACK)
    screen.blit(surface, (0, 0))
    pygame.display.update()
    pygame.time.delay(500)

def fade_in():
    """Fades in the screen from black."""
    surface = pygame.Surface((screen_width, screen_height))
    surface.fill(BLACK)
    screen.blit(surface, (0, 0))
    pygame.display.update()
    pygame.time.delay(500)


def game_over():
    """Handle game over logic"""
    global score
    screen.fill(DARK_GRAY)
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
                    fade_out()
                    main_menu()  # Return to main menu

                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10:
                        player_name += event.unicode

                screen.fill(DARK_GRAY)
                display_text('GAME OVER', game_over_font, RED, 150, 200)
                display_text(f'Score: {score}', font, TEXT_COLOR, 50, 300)
                display_text("Enter your name (max 10 characters):", font, TEXT_COLOR, 150, 350)
                display_text(player_name, font, TEXT_COLOR, 150, 400)
                pygame.display.flip()


def pause_game():
    """Handle pause logic"""
    paused = True
    screen.fill(DARK_GRAY)
    display_text("PAUSED - Press P to Resume or Q to Quit", paused_font, BUTTON_COLOR, 150, 250)
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
                    fade_out()
                    main_menu()


def main_menu():
    """Main menu of the game"""
    fade_in()
    screen.fill(DARK_GRAY)
    display_text("Welcome to Snake Game!", game_over_font, TEXT_COLOR, 150, 100)

    # Define button positions and sizes
    button_width = 300
    button_height = 60
    button_x = (screen_width - button_width) // 2

    # Draw buttons
    draw_button("New Game", font, BUTTON_COLOR, button_x, 250, button_width, button_height)
    draw_button("High Scores", font, BUTTON_COLOR, button_x, 320, button_width, button_height)
    draw_button("Settings", font, BUTTON_COLOR, button_x, 390, button_width, button_height)
    draw_button("Instructions", font, BUTTON_COLOR, button_x, 460, button_width, button_height)
    draw_button("Quit", font, BUTTON_COLOR, button_x, 530, button_width, button_height)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if any button was clicked
                if button_x <= mouse_x <= button_x + button_width:
                    if 250 <= mouse_y <= 250 + button_height:
                        fade_out()
                        game_loop()
                    elif 320 <= mouse_y <= 320 + button_height:
                        fade_out()
                        high_scores_page()
                    elif 390 <= mouse_y <= 390 + button_height:
                        fade_out()
                        settings_menu()  # Go to the settings menu
                    elif 460 <= mouse_y <= 460 + button_height:
                        fade_out()
                        instructions_page()
                    elif 530 <= mouse_y <= 530 + button_height:
                        pygame.quit()
                        exit()



def high_scores_page():
    """Display high scores"""
    screen.fill(DARK_GRAY)

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
                    fade_out()
                    main_menu()


def instructions_page():
    """Display the game instructions"""
    screen.fill(DARK_GRAY)
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
                    fade_out()
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
    """Settings menu where players can adjust the game settings."""
    global fps, fullscreen, screen

    screen.fill(DARK_GRAY)
    display_text("Settings", game_over_font, TEXT_COLOR, screen_width // 2 - 100, 50)

    # Example settings options
    difficulty_text = f"Difficulty: {'Easy' if fps == 15 else 'Hard'}"
    display_text(difficulty_text, font, TEXT_COLOR, screen_width // 2 - 100, 150)
    
    fullscreen_text = f"Fullscreen: {'ON' if fullscreen else 'OFF'}"
    display_text(fullscreen_text, font, TEXT_COLOR, screen_width // 2 - 100, 200)

    display_text("Press 'B' to go Back", font, TEXT_COLOR, screen_width // 2 - 100, 300)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    waiting_for_input = False
                    fade_out()
                    main_menu()

                elif event.key == pygame.K_d:
                    # Toggle difficulty between Easy and Hard
                    fps = 25 if fps == 15 else 15
                    settings_menu()

                elif event.key == pygame.K_f:
                    # Toggle fullscreen mode
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    settings_menu()



# Main program starts here
main_menu()
