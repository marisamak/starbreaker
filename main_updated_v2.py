# StarBreaker - улучшенное меню с настройками
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
HOVER_COLOR = (80, 80, 120)
ACTIVE_COLOR = (120, 120, 180)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarBreaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
title_font = pygame.font.SysFont("consolas", 64, bold=True)

# Музыка
# pygame.mixer.music.load("menu_music.mp3")
# pygame.mixer.music.set_volume(0.7)
# pygame.mixer.music.play(-1)

# Загрузка фона
galaxy_img = pygame.image.load("galaxy.png").convert_alpha()
galaxy_img = pygame.transform.scale(galaxy_img, (600, 600))
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

# Настройки игры
game_settings = {
    "music": True,
    "sound": True,
    "volume": 0.7,
    "difficulty": "normal"
}

main_menu_buttons = [
    {"text": "Start Game", "action": "start"},
    {"text": "Settings", "action": "settings"},
    {"text": "Help", "action": "help"},
    {"text": "Quit", "action": "quit"}
]

settings_buttons = [
    {"text": "Music: ON", "action": "toggle_music", "type": "toggle", "value": "music"},
    {"text": "Sounds: ON", "action": "toggle_sound", "type": "toggle", "value": "sound"},
    {"text": "Volume: 70%", "action": "volume", "type": "slider", "value": "volume"},
    {"text": "Difficulty: Normal", "action": "difficulty", "type": "selector",
     "options": ["Easy", "Normal", "Hard"], "value": "difficulty"},
    {"text": "Back", "action": "back"}
]

help_text = [
    "HOW TO PLAY:",
    "- Use LEFT/RIGHT arrows to move paddle",
    "- Destroy all blocks to win",
    "- Don't let the ball fall down",
    "- Press ESC to pause game",
    "",
    "CONTROLS:",
    "- ESC: Pause/Resume",
    "- F1: Show this help"
]

def draw_button(btn, x, y, width=300, height=50, is_hovered=False, is_active=False):
    btn_rect = pygame.Rect(x, y, width, height)
    color = ACTIVE_COLOR if is_active else (HOVER_COLOR if is_hovered else (30, 30, 60))
    pygame.draw.rect(screen, color, btn_rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, btn_rect, 2, border_radius=12)
    label = font.render(btn["text"], True, WHITE)
    screen.blit(label, (btn_rect.x + (width - label.get_width()) // 2,
                        btn_rect.y + (height - label.get_height()) // 2))
    return btn_rect

def draw_slider(x, y, width, value):
    track_rect = pygame.Rect(x, y, width, 10)
    thumb_pos = x + int(width * value)
    thumb_rect = pygame.Rect(thumb_pos - 10, y - 10, 20, 30)
    pygame.draw.rect(screen, (80, 80, 120), track_rect, border_radius=5)
    pygame.draw.rect(screen, WHITE, track_rect, 2, border_radius=5)
    pygame.draw.rect(screen, ACTIVE_COLOR, thumb_rect, border_radius=5)
    pygame.draw.rect(screen, WHITE, thumb_rect, 2, border_radius=5)
    return thumb_rect

def main_menu():
    while True:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)
        title = title_font.render("StarBreaker", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        mouse_pos = pygame.mouse.get_pos()
        for i, btn in enumerate(main_menu_buttons):
            is_hovered = "rect" in btn and btn["rect"].collidepoint(mouse_pos)
            btn_rect = draw_button(btn, WIDTH // 2 - 150, 200 + i * 70, 300, 50, is_hovered)
            btn["rect"] = btn_rect
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in main_menu_buttons:
                    if "rect" in btn and btn["rect"].collidepoint(event.pos):
                        return btn["action"]
        clock.tick(FPS)

def settings_menu():
    global game_settings
    dragging = None
    while True:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)
        title = title_font.render("Settings", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for i, btn in enumerate(settings_buttons):
            y_pos = 180 + i * 70
            if btn.get("type") == "toggle":
                btn["text"] = f"{btn['value'].capitalize()}: {'ON' if game_settings[btn['value']] else 'OFF'}"
                btn["rect"] = draw_button(btn, WIDTH // 2 - 150, y_pos, 300, 50,
                                           btn.get("rect", pygame.Rect(0, 0, 0, 0)).collidepoint(mouse_pos))
            elif btn.get("type") == "slider":
                btn["text"] = f"Volume: {int(game_settings['volume'] * 100)}%"
                label = font.render(btn["text"], True, WHITE)
                # Сдвигаем текст на 10 пикселей ниже (было y_pos - 30, стало y_pos - 20)
                screen.blit(label, (WIDTH // 2 - label.get_width() // 2, y_pos - 10))
                # Слайдер также сдвигаем ниже (было y_pos + 20, стало y_pos + 30)
                slider_rect = draw_slider(WIDTH // 2 - 150, y_pos + 20, 300, game_settings["volume"])
                btn["rect"] = slider_rect

                if mouse_pressed and slider_rect.collidepoint(mouse_pos):
                    dragging = btn["value"]
                elif dragging == btn["value"] and mouse_pressed:
                    new_value = (mouse_pos[0] - (WIDTH // 2 - 150)) / 300
                    game_settings["volume"] = max(0, min(1, new_value))
                elif not mouse_pressed:
                    dragging = None
            elif btn.get("type") == "selector":
                btn["text"] = f"Difficulty: {game_settings['difficulty'].capitalize()}"
                btn["rect"] = draw_button(btn, WIDTH // 2 - 150, y_pos, 300, 50,
                                           btn.get("rect", pygame.Rect(0, 0, 0, 0)).collidepoint(mouse_pos))
            else:
                btn["rect"] = draw_button(btn, WIDTH // 2 - 150, y_pos, 300, 50,
                                           btn.get("rect", pygame.Rect(0, 0, 0, 0)).collidepoint(mouse_pos))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in settings_buttons:
                    if "rect" in btn and btn["rect"].collidepoint(event.pos):
                        if btn["action"] == "back":
                            return
                        elif btn["action"] == "toggle_music":
                            game_settings["music"] = not game_settings["music"]
                            if game_settings["music"]:
                                pygame.mixer.music.play(-1)
                            else:
                                pygame.mixer.music.stop()
                        elif btn["action"] == "toggle_sound":
                            game_settings["sound"] = not game_settings["sound"]
                        elif btn["action"] == "difficulty":
                            diffs = ["easy", "normal", "hard"]
                            current = diffs.index(game_settings["difficulty"])
                            game_settings["difficulty"] = diffs[(current + 1) % len(diffs)]
        clock.tick(FPS)

def help_menu():
    while True:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)
        title = title_font.render("Help", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        for i, line in enumerate(help_text):
            text = font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 180 + i * 30))
        mouse_pos = pygame.mouse.get_pos()
        back_btn = {"text": "Back", "action": "back"}
        back_btn["rect"] = draw_button(back_btn, WIDTH // 2 - 150, HEIGHT - 100, 300, 50,
                                       back_btn.get("rect", pygame.Rect(0, 0, 0, 0)).collidepoint(mouse_pos))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if "rect" in back_btn and back_btn["rect"].collidepoint(event.pos):
                    return
        clock.tick(FPS)

def game_loop():
    apply_difficulty()
    select_rocket()
    countdown()
    # pygame.mixer.music.load("game_music.mp3")
    # pygame.mixer.music.play(-1)
    paddle = selected_rocket_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
    paddle_speed = 8
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
    ball_speed = [5, -5]
    blocks = [pygame.Rect(col * (WIDTH // 10) + 5, row * 30 + 5, 70, 20)
              for row in range(5) for col in range(10)]
    score, lives = 0, 3
    paused = False
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BG_COLOR)
        galaxy_pos[1] = math.sin(pygame.time.get_ticks() * 0.001) * 10
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_F1:
                    help_menu()
        if paused:
            pause_text = font.render("PAUSED - Press ESC to resume", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            continue
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] *= -1
        if ball.top <= 0:
            ball_speed[1] *= -1
        if ball.bottom >= HEIGHT:
            lives -= 1
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            ball_speed = [5 * random.choice([-1, 1]), -5]
        if ball.colliderect(paddle):
            ball_speed[1] *= -1
        for block in blocks[:]:
            if ball.colliderect(block):
                blocks.remove(block)
            if random.random() < 0.25:
                bonuses.append({'type': random.choice(bonus_types), 'rect': pygame.Rect(block.x, block.y, 20, 20)})
                ball_speed[1] *= -1
                score += 10
                break
        screen.blit(selected_rocket_img, paddle)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        for block in blocks:
            pygame.draw.rect(screen, BLOCK_COLOR, block)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 120, 10))
        if lives <= 0 or not blocks:
            end_text = "YOU WIN!" if not blocks else "GAME OVER"
            msg = font.render(end_text, True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            # pygame.mixer.music.load("menu_music.mp3")
            # pygame.mixer.music.play(-1)
            return
        pygame.display.flip()


# Загрузка изображений ракет (временно — цветные прямоугольники)
rocket_imgs = [
    pygame.Surface((80, 30)),  # Ракета 1
    pygame.Surface((100, 20)),  # Ракета 2
    pygame.Surface((60, 40)),  # Ракета 3
]
rocket_imgs[0].fill((255, 100, 100))   # красная
rocket_imgs[1].fill((100, 255, 100))   # зелёная
rocket_imgs[2].fill((100, 100, 255))   # синяя

selected_rocket_img = rocket_imgs[0]  # по умолчанию

def select_rocket():
    global selected_rocket_img
    selecting = True
    selected = 0

    while selecting:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)

        title = font.render("SELECT YOUR ROCKET", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        for i, rocket in enumerate(rocket_imgs):
            x = WIDTH // 2 - 150 + i * 100
            y = HEIGHT // 2
            border_color = (255, 255, 0) if i == selected else (100, 100, 100)
            pygame.draw.rect(screen, border_color, (x - 5, y - 5, rocket.get_width() + 10, rocket.get_height() + 10), 2)
            screen.blit(rocket, (x, y))

        instruction = font.render("Use LEFT / RIGHT, Enter to select", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 80))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    selected_rocket_img = rocket_imgs[selected]
                    selecting = False

        clock.tick(60)

def countdown():
    for i in [3, 2, 1, "START"]:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)

        count_text = title_font.render(str(i), True, WHITE)
        screen.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(1000)


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

def main():
    while True:
        action = main_menu()
        if action == "start":
            game_loop()
        elif action == "settings":
            settings_menu()
        elif action == "help":
            help_menu()
        elif action == "quit":
            pygame.quit()
            return

if __name__ == "__main__":
    main()
