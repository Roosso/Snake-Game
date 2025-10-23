import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 30  # width of the field in cells
HEIGHT = 30  # height of the field in cells
CELL_SIZE = 20  # size of one cell in pixels
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake - 30x30")
clock = pygame.time.Clock()

# Font for displaying the score
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - 1, HEIGHT // 2), (WIDTH // 2 - 2, HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Add new head
        self.body.insert(0, new_head)

        # If we don't grow, remove the tail
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        # Prevent turning 180 degrees
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow_snake(self):
        self.grow = True

    def check_collision(self):
        head = self.body[0]

        # Collision with walls
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True

        # Collision with itself
        if head in self.body[1:]:
            return True

        return False

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body):
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if (x, y) not in snake_body:
                return (x, y)

    def respawn(self, snake_body):
        self.position = self.generate_position(snake_body)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_snake(snake):
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN,
                        (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED,
                    (food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to exit", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        # Restart the game
                        main()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)

        if not game_over:
            snake.move()

            # Check if the snake has eaten the food
            if snake.body[0] == food.position:
                snake.grow_snake()
                food.respawn(snake.body)
                score += 10

            # Check for collision
            if snake.check_collision():
                game_over = True

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_score(score)

        if game_over:
            game_over_screen(score)

        pygame.display.flip()
        clock.tick(10)  # Game speed (FPS)

if __name__ == "__main__":
    main()
