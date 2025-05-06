import pygame
import random
import sys
import math

# Настройки
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BG_COLOR = (10, 10, 25)
BALL_COLOR = (100, 200, 255)
BLOCK_COLOR = (150, 50, 250)
PADDLE_COLOR = (255, 255, 255)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarBreaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# Платформа
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)
paddle_speed = 8

# Шарик
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [5, -5]

# Загрузка фоновых изображений
galaxy_img = pygame.image.load("galaxy.png").convert_alpha()

# Масштабируем под размер экрана (или меньше)
galaxy_img = pygame.transform.scale(galaxy_img, (500, 500))

# Позиции
galaxy_pos = [0, 0]

# Блоки
blocks = []
block_rows = 5
block_cols = 10
block_width = WIDTH // block_cols
block_height = 30

for row in range(block_rows):
    for col in range(block_cols):
        rect = pygame.Rect(col * block_width + 5, row * block_height + 5, block_width - 10, block_height - 10)
        blocks.append(rect)

# Счёт
score = 0
lives = 3

# Звезды на фоне
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.choice([1, 1, 2])
        self.speed = random.uniform(0.5, 1.5)
        self.color = (random.randint(150, 255),) * 3  # светлые оттенки

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

stars = [Star() for _ in range(100)]  # Массив звёзд


# Основной цикл
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)
    galaxy_pos[1] = math.sin(pygame.time.get_ticks() * 0.001) * 10

    # Рисуем планету и галактику
    screen.blit(galaxy_img, galaxy_pos)

    # Звезды поверх
    for star in stars:
        star.move()
        star.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Движение мяча
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Отражения от стен
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1
    if ball.bottom >= HEIGHT:
        lives -= 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed = [5 * random.choice([-1, 1]), -5]

    # Отражение от платформы
    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    # Столкновение с блоками
    for block in blocks[:]:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_speed[1] *= -1
            score += 10
            break

    # Рисование
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.ellipse(screen, BALL_COLOR, ball)

    for block in blocks:
        pygame.draw.rect(screen, BLOCK_COLOR, block)

    # Текст
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Проверка окончания
    if lives <= 0:
        game_over = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    elif not blocks:
        win_text = font.render("YOU WIN!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 70, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
