import pygame
import random
import sys
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
HOVER_COLOR = (80, 80, 120)
ACTIVE_COLOR = (120, 120, 180)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarBreaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
title_font = pygame.font.SysFont("consolas", 64, bold=True)

# Музыка
pygame.mixer.music.load("menu_music.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

galaxy_img = pygame.image.load("galaxy.png").convert_alpha()
galaxy_img = pygame.transform.scale(galaxy_img, (600, 600))
galaxy_pos = [0, 0]

bounce_sound = pygame.mixer.Sound("bounce.mp3")
break_sound = pygame.mixer.Sound("break.mp3")
hover_sound = pygame.mixer.Sound("hover.mp3")
lose_sound = pygame.mixer.Sound("fail.mp3")
win_sound = pygame.mixer.Sound("win.mp3")
fail_sound = pygame.mixer.Sound("lose.mp3")

# Настройки игры
game_settings = {
    "music": True,
    "sound": True,
    "volume": 0.7,
    "difficulty": "Нормально"
}

for sound in [bounce_sound, break_sound, hover_sound, lose_sound, win_sound, fail_sound]:
    sound.set_volume(game_settings["volume"])

# Меню
main_menu_buttons = [
    {"text": "Начать игру", "action": "start"},
    {"text": "Настройки", "action": "settings"},
    {"text": "Статистика", "action": "stats"},
    {"text": "Помощь", "action": "help"},
    {"text": "Выход", "action": "quit"}
]

settings_buttons = [
    {"text": "Музыка: Включена", "action": "toggle_music", "type": "toggle", "value": "music"},
    {"text": "Звуки: Включены", "action": "toggle_sound", "type": "toggle", "value": "sound"},
    {"text": "Громкость: 70%", "action": "volume", "type": "slider", "value": "volume"},
    {"text": "Сложность: Нормально", "action": "difficulty", "type": "selector",
     "options": ["Легко", "Нормально", "Трудно"], "value": "difficulty"},
    {"text": "Назад", "action": "back"}
]

help_text = [
    "Правила игры:",
    "- Используйте для передвижения стрелки на клавиатуре: ← →",
    "- Разбей все преграды, чтобы выиграть",
    "- Не дайте снаряду упасть",
    "- Нажмите кнопку ESC для паузы",
    "",
    "Элементы управления:",
    "- ESC: Пауза/Продолжение игры",
    "- F1: Показать инструкцию по работе"
]

# Звезды
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.choice([1, 1, 2])
        self.speed = random.uniform(0.5, 2.5)  # Разные скорости для глубины
        self.color = (random.randint(200, 255),) * 3  # Более яркие звезды


    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Добавляем блики для более крупных звезд
        if self.radius > 1:
            highlight = min(255, self.color[0] + 40)
            pygame.draw.circle(surface, (highlight, highlight, highlight),
                             (int(self.x) - 1, int(self.y) - 1), 1)

stars = [Star() for _ in range(100)]

# Статистика
stats_file = "stats.json"

def load_stats():
    if os.path.exists(stats_file):
        with open(stats_file, "r") as f:
            return json.load(f)
    return {"Легко": {"побед": 0, "поражений": 0}, "Нормально": {"побед": 0, "поражений": 0}, "Трудно": {"побед": 0, "поражений": 0}}

def save_stats(stats):
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

stats = load_stats()


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
        title = title_font.render("Звездный удар", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        current_hovered = None

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
                        if game_settings["sound"]:
                            hover_sound.play()
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

        title = title_font.render("Настройки", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for i, btn in enumerate(settings_buttons):
            y_pos = 180 + i * 70
            if btn.get("type") == "toggle":
                btn["text"] = f"{btn['value'].capitalize()}: {'Включена' if game_settings[btn['value']] else 'Выключена'}"
                btn["rect"] = draw_button(btn, WIDTH // 2 - 150, y_pos, 300, 50,
                                           btn.get("rect", pygame.Rect(0, 0, 0, 0)).collidepoint(mouse_pos))
            elif btn.get("type") == "slider":
                btn["text"] = f"Громкость: {int(game_settings['volume'] * 100)}%"
                label = font.render(btn["text"], True, WHITE)
                screen.blit(label, (WIDTH // 2 - label.get_width() // 2, y_pos - 10))
                slider_rect = draw_slider(WIDTH // 2 - 150, y_pos + 20, 300, game_settings["volume"])
                btn["rect"] = slider_rect

                if mouse_pressed and slider_rect.collidepoint(mouse_pos):
                    dragging = btn["value"]
                elif dragging == btn["value"] and mouse_pressed:
                    new_value = (mouse_pos[0] - (WIDTH // 2 - 150)) / 300
                    game_settings["volume"] = max(0, min(1, new_value))
                    pygame.mixer.music.set_volume(game_settings["volume"])  # 👈 Важное добавление
                    hover_sound.set_volume(game_settings["volume"])  # 👈 И это
                    hover_sound.set_volume(game_settings["volume"])
                elif not mouse_pressed:
                    dragging = None
            elif btn.get("type") == "selector":
                btn["text"] = f"Сложность: {game_settings['difficulty'].capitalize()}"
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
                        if game_settings["sound"]:
                            hover_sound.play()
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
                            diffs = ["Легко", "Нормально", "Трудно"]
                            current = diffs.index(game_settings["difficulty"])
                            game_settings["difficulty"] = diffs[(current + 1) % len(diffs)]
        clock.tick(FPS)


def stats_menu():
    while True:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)

        title = title_font.render("Статистика", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        y = 180
        for level in ["Легко", "Нормально", "Трудно"]:
            line = f"{level}: Победы: {stats[level.lower()]['побед']} | Поражения: {stats[level.lower()]['поражений']}"
            line_surf = font.render(line, True, WHITE)
            screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, y))
            y += 50

        mouse_pos = pygame.mouse.get_pos()
        back_btn = {"text": "Назад", "action": "back"}
        is_hovered = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 300, 50).collidepoint(mouse_pos)
        back_btn["rect"] = draw_button(back_btn, WIDTH // 2 - 150, HEIGHT - 100, 300, 50, is_hovered)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_settings["sound"]:
                    hover_sound.play()
                if "rect" in back_btn and back_btn["rect"].collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(FPS)


def help_menu():
    while True:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)

        title = title_font.render("Помощь", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        for i, line in enumerate(help_text):
            text = font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 180 + i * 30))

        mouse_pos = pygame.mouse.get_pos()
        back_btn = {"text": "Back", "action": "back"}
        is_hovered = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 300, 50).collidepoint(mouse_pos)
        back_btn["rect"] = draw_button(back_btn, WIDTH // 2 - 150, HEIGHT - 100, 300, 50, is_hovered)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_settings["sound"]:
                    hover_sound.play()
                if "rect" in back_btn and back_btn["rect"].collidepoint(event.pos):
                    return

        clock.tick(FPS)


# Ракеты (временно — цветные прямоугольники)
rocket_imgs = [
    pygame.image.load("rocket_1.png").convert_alpha(),  # Широкая ракета
    pygame.image.load("rocket_2.png").convert_alpha(),  # Средняя ракета
    pygame.image.load("rocket_3.png").convert_alpha()  # Узкая ракета
]

# Масштабируем изображения к нужному размеру
rocket_imgs[0] = pygame.transform.scale(rocket_imgs[0], (120, 120))
rocket_imgs[1] = pygame.transform.scale(rocket_imgs[1], (120, 120))
rocket_imgs[2] = pygame.transform.scale(rocket_imgs[2], (120, 120))

selected_rocket_img = rocket_imgs[1]  # по умолчанию


def select_rocket():
    global selected_rocket_img
    selecting = True
    selected = 0
    rocket_rects = []  # Список для хранения прямоугольников ракет

    while selecting:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)

        title = font.render("SELECT YOUR ROCKET", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        rocket_rects = []  # Очищаем список каждый кадр
        for i, rocket in enumerate(rocket_imgs):
            x = WIDTH // 2 - 210 + i * 140
            y = HEIGHT // 2
            rocket_rect = pygame.Rect(x, y, rocket.get_width(), rocket.get_height())
            rocket_rects.append(rocket_rect)

            # Определяем цвет рамки (желтый для выбранной, серый для остальных)
            mouse_pos = pygame.mouse.get_pos()
            border_color = (255, 255, 0) if rocket_rect.collidepoint(mouse_pos) else (100, 100, 100)

            pygame.draw.rect(screen, border_color, (x - 5, y - 5, rocket.get_width() + 10, rocket.get_height() + 10), 2)
            screen.blit(rocket, (x, y))

        instruction = font.render("Выберите ракету", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(rocket_rects):
                        if rect.collidepoint(mouse_pos):
                            selected_rocket_img = rocket_imgs[i]
                            selecting = False
                            return

        clock.tick(60)


def countdown():
    for i in [3, 2, 1, "Поехалии!!"]:
        screen.fill(BG_COLOR)
        screen.blit(galaxy_img, galaxy_pos)
        for star in stars:
            star.move()
            star.draw(screen)

        count_text = title_font.render(str(i), True, WHITE)
        screen.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(1000)


difficulty = "Нормально"  # Easy / Normal / Hard


def apply_difficulty():
    global ball_speed, paddle_speed, base_ball_speed

    if game_settings["difficulty"] == "Легко":
        base_ball_speed = [3, -3]
        paddle_speed = 6
    elif game_settings["difficulty"] == "Нормально":
        base_ball_speed = [5, -5]
        paddle_speed = 8
    elif game_settings["difficulty"] == "Трудно":
        base_ball_speed = [7, -7]
        paddle_speed = 10

    ball_speed = base_ball_speed.copy()



def game_loop():
    global stats
    global ball_speed

    # Применяем настройки сложности
    apply_difficulty()

    # Выбор ракеты
    rocket_result = select_rocket()
    if rocket_result == "back":
        return

    # Обратный отсчет
    countdown()

    # pygame.mixer.music.load("game_music.mp3")
    # pygame.mixer.music.play(-1)

    # Инициализация игры
    paddle = selected_rocket_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
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

        # Управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # Движение мяча
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Отскок от стен
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] *= -1
        if ball.top <= 0:
            ball_speed[1] *= -1


        # Проверка на проигрыш
        if ball.bottom >= HEIGHT:
            lives -= 1
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            ball_speed = [base_ball_speed[0] * random.choice([-1, 1]), base_ball_speed[1]]

        # Отскок от платформы
        if ball.colliderect(paddle):
            ball_speed[1] *= -1
            if game_settings["sound"]:
                bounce_sound.play()

        # Проверка столкновений с блоками
        for block in blocks[:]:
            if ball.colliderect(block):
                blocks.remove(block)
                ball_speed[1] *= -1
                score += 10
                if game_settings["sound"]:
                    break_sound.play()
                break

        # Отрисовка объектов
        screen.blit(selected_rocket_img, paddle)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        for block in blocks:
            pygame.draw.rect(screen, BLOCK_COLOR, block)

        # Отрисовка счета и жизней
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 120, 10))

        # Проверка условий окончания игры
        if lives <= 0:
            if game_settings["sound"]:
                fail_sound.play()
            stats[game_settings["difficulty"]]["поражений"] += 1
            save_stats(stats)
            end_text = "GAME OVER"
            msg = font.render(end_text, True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            return
        elif not blocks:
            if game_settings["sound"]:
                win_sound.play()
            stats[game_settings["difficulty"]]["побед"] += 1
            save_stats(stats)
            end_text = "YOU WIN!"
            msg = font.render(end_text, True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        pygame.display.flip()


def main():
    while True:
        action = main_menu()
        if action == "start":
            game_loop()
        elif action == "settings":
            settings_menu()
        elif action == "stats":
            stats_menu()
        elif action == "help":
            help_menu()
        elif action == "quit":
            pygame.quit()
            return


if __name__ == "__main__":
    main()


























