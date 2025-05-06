# Импорт
import pygame
import sys
import random
import math
import os
import json

# Настройки
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BG_COLOR = (10, 10, 25)
BALL_COLOR = (100, 200, 255)
BLOCK_COLOR = (150, 50, 250)
PADDLE_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarBreaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
title_font = pygame.font.SysFont("consolas", 64, bold=True)

# --- НАСТРОЙКА СЛОЖНОСТИ ---
difficulty = "Normal"  # Easy / Normal / Hard

def apply_difficulty():
    global ball_speed, selected_rocket_img, paddle_speed
    if difficulty == "Easy":
        ball_speed[:] = [3, -3]
        selected_rocket_img = rocket_imgs[0]  # широкая
    elif difficulty == "Normal":
        ball_speed[:] = [5, -5]
        selected_rocket_img = rocket_imgs[1]
    elif difficulty == "Hard":
        ball_speed[:] = [7, -7]
        selected_rocket_img = rocket_imgs[2]  # узкая

# Статистика
stats_file = "stats.json"

def load_stats():
    if os.path.exists(stats_file):
        with open(stats_file, "r") as f:
            return json.load(f)
    return {"Easy": {"wins": 0, "losses": 0}, "Normal": {"wins": 0, "losses": 0}, "Hard": {"wins": 0, "losses": 0}}

def save_stats(stats):
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

stats = load_stats()

# Ракеты (временно — цветные прямоугольники)
rocket_imgs = [
    pygame.Surface((100, 30)),  # Easy
    pygame.Surface((80, 25)),   # Normal
    pygame.Surface((60, 20)),   # Hard
]
rocket_imgs[0].fill((255, 100, 100))
rocket_imgs[1].fill((100, 255, 100))
rocket_imgs[2].fill((100, 100, 255))
selected_rocket_img = rocket_imgs[1]

# Фоновая графика
galaxy_img = pygame.Surface((600, 600))
galaxy_img.fill((20, 20, 40))
galaxy_pos = [0, 0]

# Звезды
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.choice([1, 1, 2])
        self.speed = random.uniform(0.5, 1.5)
        self.color = (random.randint(150, 255),) * 3

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

stars = [Star() for _ in range(100)]

# Кнопки
buttons = [
    {"text": "Start Game", "rect": pygame.Rect(WIDTH // 2 - 150, 220, 300, 50)},
    {"text": "Difficulty", "rect": pygame.Rect(WIDTH // 2 - 150, 290, 300, 50)},
    {"text": "Stats", "rect": pygame.Rect(WIDTH // 2 - 150, 360, 300, 50)},
    {"text": "Quit", "rect": pygame.Rect(WIDTH // 2 - 150, 430, 300, 50)},
]

# Меню
def draw_menu():
    screen.fill(BG_COLOR)
    screen.blit(galaxy_img, galaxy_pos)
    for star in stars:
        star.move()
        star.draw(screen)

    title = title_font.render("StarBreaker", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
    diff_label = font.render(f"Difficulty: {difficulty}", True, WHITE)
    screen.blit(diff_label, (WIDTH - diff_label.get_width() - 20, 20))

    for btn in buttons:
        pygame.draw.rect(screen, (30, 30, 60), btn["rect"], border_radius=12)
        pygame.draw.rect(screen, WHITE, btn["rect"], 2, border_radius=12)
        label = font.render(btn["text"], True, WHITE)
        screen.blit(label, (btn["rect"].x + 20, btn["rect"].y + 10))

    pygame.display.flip()

def menu_loop():
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["text"] == "Start Game":
                            return
                        elif btn["text"] == "Difficulty":
                            global difficulty
                            difficulty = {"Easy": "Normal", "Normal": "Hard", "Hard": "Easy"}[difficulty]
                        elif btn["text"] == "Stats":
                            showing_stats = True
                            while showing_stats:
                                screen.fill(BG_COLOR)
                                screen.blit(galaxy_img, galaxy_pos)
                                for star in stars:
                                    star.move()
                                    star.draw(screen)
                                title = title_font.render("STATS", True, WHITE)
                                screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
                                y = 180
                                for level in ["Easy", "Normal", "Hard"]:
                                    line = f"{level}: Wins: {stats[level]['wins']} | Losses: {stats[level]['losses']}"
                                    line_surf = font.render(line, True, WHITE)
                                    screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, y))
                                    y += 50
                                exit_txt = font.render("Press ESC to return", True, (180,180,180))
                                screen.blit(exit_txt, (WIDTH // 2 - exit_txt.get_width() // 2, HEIGHT - 60))
                                pygame.display.flip()
                                for ev in pygame.event.get():
                                    if ev.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                                        showing_stats = False
                        elif btn["text"] == "Quit":
                            pygame.quit()
                            sys.exit()
        clock.tick(FPS)

def main():
    menu_loop()
    apply_difficulty()
    # ... тут начнётся запуск выбора ракеты, игра и прочее

if __name__ == "__main__":
    main()
