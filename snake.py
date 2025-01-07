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


class Snake:
    def __init__(self):
        self.snake_pos = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def move(self):
        """Move the snake based on its current direction"""
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

    def grow(self):
        """Grow the snake's body"""
        self.body.insert(0, list(self.snake_pos))

    def check_collision(self):
        """Check if the snake collides with the boundaries or itself"""
        if self.snake_pos[0] < 0 or self.snake_pos[0] >= screen_width or self.snake_pos[1] < 0 or self.snake_pos[1] >= screen_height:
            return True
        if self.snake_pos in self.body[1:]:
            return True
        return False

    def update(self):
        """Update snake's position"""
        self.body.insert(0, list(self.snake_pos))

    def eat(self, food_pos):
        """Check if the snake eats the food"""
        if self.snake_pos == food_pos:
            self.score += 10
            return True
        else:
            return False


class Food:
    def __init__(self):
        self.food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]

    def spawn(self):
        """Spawn a new food item"""
        self.food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]


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


def game_over():
    """Handle game over logic"""
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


def game_loop():
    """Main game loop"""
    global snake_pos, body, direction, change_to, food_pos, score, screen_width, screen_height

    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.change_to = 'RIGHT'
                elif event.key == pygame.K_p:
                    pause_game()

        snake.direction = snake.change_to
        snake.move()

        if snake.eat(food.food_pos):
            food.spawn()
            eat_sound.play()
        else:
            snake.body.pop()

        if snake.check_collision():
            game_over()

        snake.update()

        screen.fill(BLACK)
        for block in snake.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food.food_pos[0], food.food_pos[1], 10, 10))

        display_text(f"Score: {snake.score}", font, WHITE, 10, 10)

        pygame.display.update()
        clock.tick(fps)


def main_menu():
    """Main menu of the game"""
    screen.fill(BLACK)
    display_text("Welcome to Snake Game!", game_over_font, TEXT_COLOR, 150, 100)
    display_text("Press 'N' for New Game", font, TEXT_COLOR, 250, 250)
    display_text("Press 'H' for High Scores", font, TEXT_COLOR, 250, 300)
    display_text("Press 'Q' to Quit", font, TEXT_COLOR, 250, 350)
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


# Start the game with the main menu
main_menu()
