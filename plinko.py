import random
import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Plinko Task Decider')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()

# Pegs settings
PEG_RADIUS = 5
PEG_SPACING = 50

# Ball settings
BALL_RADIUS = 10
BALL_GRAVITY = 1
BALL_FRICTION = 0.99
BALL_BOUNCE = 0.9
BALL_MOVE_SPEED = 5

# Task list
tasks = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]

# Font settings
font = pygame.font.SysFont(None, 36)

# Function to create pegs
def create_pegs():
    """Create a list of pegs."""
    pegs = []
    for y in range(100, HEIGHT - 150, PEG_SPACING):  # Adjust to leave space at bottom for tasks
        offset = PEG_SPACING // 2 if (y // PEG_SPACING) % 2 == 0 else 0
        for x in range(offset, WIDTH, PEG_SPACING):
            pegs.append((x, y))
    return pegs

# Function to draw pegs
def draw_pegs(pegs):
    """Draw pegs on the screen."""
    for peg in pegs:
        pygame.draw.circle(screen, BLACK, peg, PEG_RADIUS)

# Function to draw ball
def draw_ball(x, y):
    """Draw the ball on the screen."""
    pygame.draw.circle(screen, RED, (x, y), BALL_RADIUS)

# Function to draw tasks
def draw_tasks():
    """Draw tasks at the bottom of the screen."""
    segment_width = WIDTH // len(tasks)
    for i, task in enumerate(tasks):
        x = i * segment_width
        text = font.render(task, True, BLUE)
        screen.blit(text, (x + segment_width // 2 - text.get_width() // 2, HEIGHT - 50))
        pygame.draw.line(screen, BLACK, (x, HEIGHT - 100), (x, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (WIDTH, HEIGHT - 100), (WIDTH, HEIGHT), 2)

# Main function
def main():
    """Main game loop."""
    running = True
    pegs = create_pegs()
    ball_x, ball_y = WIDTH // 2, BALL_RADIUS
    ball_vx, ball_vy = 0, 0
    ball_dropped = False
    control_enabled = True
    resting = False

    while running:
        screen.fill(WHITE)
        draw_pegs(pegs)
        draw_tasks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball_dropped and control_enabled:
                    ball_dropped = True
                    ball_vy = BALL_MOVE_SPEED  # Start moving down when dropped
                    control_enabled = False  # Disable control after dropping
                elif event.key == pygame.K_a and control_enabled:
                    ball_vx = -BALL_MOVE_SPEED  # Move left
                elif event.key == pygame.K_d and control_enabled:
                    ball_vx = BALL_MOVE_SPEED  # Move right
                elif event.key == pygame.K_RETURN and resting:
                    resting = False
                    ball_x, ball_y = WIDTH // 2, BALL_RADIUS
                    ball_vx, ball_vy = 0, 0
                    control_enabled = True

        # Ensure ball stays within screen bounds
        ball_x += ball_vx
        if ball_x < BALL_RADIUS:
            ball_x = BALL_RADIUS
        elif ball_x > WIDTH - BALL_RADIUS:
            ball_x = WIDTH - BALL_RADIUS

        if ball_dropped and not resting:
            ball_vy += BALL_GRAVITY  # Apply gravity to vertical velocity
            ball_y += ball_vy

            for peg in pegs:
                peg_x, peg_y = peg
                dx = ball_x - peg_x
                dy = ball_y - peg_y
                distance = math.hypot(dx, dy)
                if distance < PEG_RADIUS + BALL_RADIUS:
                    ball_vx = random.choice([-BALL_MOVE_SPEED, BALL_MOVE_SPEED])
                    ball_vy = -ball_vy * BALL_BOUNCE

                    # Move the ball out of collision
                    overlap = PEG_RADIUS + BALL_RADIUS - distance
                    ball_x += overlap * (dx / distance)
                    ball_y += overlap * (dy / distance)

            ball_vx *= BALL_FRICTION

            if ball_y > HEIGHT - BALL_RADIUS:  # Check if ball hits bottom
                if abs(ball_vy) < 1:  # If ball's vertical velocity is low enough
                    resting = True  # Set ball to resting state
                    ball_y = HEIGHT - BALL_RADIUS  # Position ball at bottom
                    ball_vy = 0  # Reset vertical velocity

        draw_ball(ball_x, ball_y)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
