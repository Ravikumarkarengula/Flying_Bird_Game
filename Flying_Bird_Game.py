import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flying Bird Game")

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GREEN = (50, 205, 50)
BROWN = (139, 69, 19)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
ORANGE = (255, 69, 0)

# Frame rate
FPS = 60

# Dragon parameters
DRAGON_WIDTH, DRAGON_HEIGHT = 60, 40
DRAGON_SPEED_DOWN = 7  # Downward movement speed

# Font
FONT = pygame.font.SysFont('comicsans', 30)

# Buttons
def draw_button(win, text, x, y, w, h, color, text_color=BLACK):
    pygame.draw.rect(win, color, (x, y, w, h))
    text_surf = FONT.render(text, True, text_color)
    win.blit(text_surf, (x + w//2 - text_surf.get_width()//2, y + h//2 - text_surf.get_height()//2))
    return pygame.Rect(x, y, w, h)

class Dragon:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 150  # Start a bit higher than ground
        self.width = DRAGON_WIDTH
        self.height = DRAGON_HEIGHT
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True

    def move_down(self):
        self.y += DRAGON_SPEED_DOWN
        if self.y > HEIGHT - 100:  # Stop at ground
            self.y = HEIGHT - 100
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y >= HEIGHT - 100:
            self.y = HEIGHT - 100
            self.is_jumping = False
            self.vel_y = 0

        if self.y <= 0:
            self.y = 0
            self.vel_y = 0

        self.rect.topleft = (self.x, self.y)

    def draw(self, win):
        pygame.draw.rect(win, RED, self.rect)
        pygame.draw.polygon(win, DARK_RED, [
            (self.rect.left - 10, self.rect.top + 10),
            (self.rect.left + 10, self.rect.bottom - 10),
            (self.rect.left + 20, self.rect.bottom - 10)
        ])

class Cloud:
    def __init__(self):
        self.x = random.randint(WIDTH, WIDTH + 100)
        self.y = random.randint(50, 150)
        self.speed = random.uniform(0.5,1.5)

    def update(self):
        self.x -= self.speed
        if self.x < -80:
            self.x = random.randint(WIDTH, WIDTH + 100)
            self.y = random.randint(50, 150)
            self.speed = random.uniform(0.5,1.5)

    def draw(self, win):
        pygame.draw.ellipse(win, WHITE, (self.x, self.y, 50, 30))
        pygame.draw.ellipse(win, WHITE, (self.x + 20, self.y - 10, 50, 40))
        pygame.draw.ellipse(win, WHITE, (self.x + 40, self.y, 50, 30))

class Obstacle:
    def __init__(self):
        self.type = random.choice(["rock", "tree", "fireball"])
        if self.type == "fireball":
            self.width = 30
            self.height = 30
            self.y = HEIGHT - 70  # Lower than the dragon start position
        else:
            self.width = random.choice([20, 40, 60])
            self.height = random.choice([40, 60, 30])
            self.y = HEIGHT - 100 + (60 - self.height)

        self.x = WIDTH + random.randint(0, 300)
        self.speed = 12
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, win):
        if self.type == "rock":
            pygame.draw.rect(win, GREY, self.rect)
        elif self.type == "tree":
            trunk = pygame.Rect(self.x + self.width//2 - 5, self.y + self.height//2, 10, self.height//2)
            leaves = pygame.Rect(self.x, self.y, self.width, self.height//2)
            pygame.draw.rect(win, BROWN, trunk)
            pygame.draw.ellipse(win, (34, 139, 34), leaves)
        elif self.type == "fireball":
            pygame.draw.circle(win, ORANGE, (self.x + self.width//2, self.y + self.height//2), self.width//2)

def draw_window(dragon, clouds, obstacles, score):
    WIN.fill(SKY_BLUE)
    for cloud in clouds:
        cloud.draw(WIN)
    pygame.draw.rect(WIN, GREEN, (0, HEIGHT - 40, WIDTH, 40))
    dragon.draw(WIN)
    for obstacle in obstacles:
        obstacle.draw(WIN)
    score_text = FONT.render(f'Score: {score}', True, BLACK)
    WIN.blit(score_text, (WIDTH - 150, 10))
    pygame.display.update()

def start_screen():
    while True:
        WIN.fill(SKY_BLUE)
        title = pygame.font.SysFont('comicsans', 60).render("Flying Bird Game", True, BLACK)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3 - 50))
        start_btn = draw_button(WIN, "Start", WIDTH//2 - 120, HEIGHT//2, 100, 50, GREEN)
        quit_btn = draw_button(WIN, "Quit", WIDTH//2 + 20, HEIGHT//2, 100, 50, RED)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def game_over_screen(score):
    while True:
        WIN.fill(SKY_BLUE)
        over_text = pygame.font.SysFont('comicsans', 60).render("Game Over", True, BLACK)
        score_text = FONT.render(f'Score: {score}', True, BLACK)
        WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3 - 50))
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 20))
        restart_btn = draw_button(WIN, "Restart", WIDTH//2 - 110, HEIGHT//2 + 50, 100, 50, GREEN)
        quit_btn = draw_button(WIN, "Quit", WIDTH//2 + 10, HEIGHT//2 + 50, 100, 50, RED)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def main(show_start=True):
    if show_start:
        start_screen()

    clock = pygame.time.Clock()
    dragon = Dragon()
    clouds = [Cloud() for _ in range(5)]
    obstacles = [Obstacle()]
    score = 0
    run = True

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dragon.jump()

        if keys[pygame.K_DOWN]:
            dragon.move_down()  # Now dragon moves downward

        dragon.update()

        for cloud in clouds:
            cloud.update()

        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)
                score += 1
                obstacles.append(Obstacle())

        # Collision detection
        for obstacle in obstacles:
            if dragon.rect.colliderect(obstacle.rect):
                game_over_screen(score)
                main(show_start=False)

        draw_window(dragon, clouds, obstacles, score)

if __name__ == "__main__":
    main()
