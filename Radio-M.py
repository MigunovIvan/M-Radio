import pygame
import random
import sys
import os
import vlc  # Импортируем библиотеку vlc для воспроизведения радио

# Инициализация Pygame
pygame.init()

# Размеры окна и ресурсы
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BG_COLOR = (20, 20, 20)  # Темный фон
BTN_COLOR = (50, 50, 50)  # Цвет кнопок (металлик)
BTN_HOVER_COLOR = (80, 80, 80)  # Цвет кнопок при наведении
TEXT_COLOR = (255, 255, 255)  # Цвет текста на кнопках

# Радио URL
RADIO_URL = "https://cast2.my-control-panel.com/proxy/vladas/stream"

# Иконка для окна
ICON_PATH = "R.ico"  # Иконка для окна (укажите путь)

# Функция для получения пути к файлам
def resource_path(relative_path):
    """Определяет путь к ресурсам в зависимости от того, с какого места выполняется скрипт."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Установка иконки для окна
pygame.display.set_icon(pygame.image.load(resource_path(ICON_PATH)))

# Загрузка фона
BACKGROUND_IMAGE_PATH = resource_path("WL.jpg")
BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGE_PATH)
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Загрузка изображений смайликов
guitar_emoji = pygame.image.load(resource_path("guitar_emoji.png"))
rock_on_emoji = pygame.image.load(resource_path("rock_on_emoji.png"))
guitar_emoji = pygame.transform.scale(guitar_emoji, (50, 50))
rock_on_emoji = pygame.transform.scale(rock_on_emoji, (50, 50))

# Координаты и направления для смайликов
emoji_positions = [
    [random.randint(0, WINDOW_WIDTH - 50), random.randint(0, WINDOW_HEIGHT - 50)],
    [random.randint(0, WINDOW_WIDTH - 50), random.randint(0, WINDOW_HEIGHT - 50)]
]
emoji_directions = [
    [random.choice([-1, 1]), random.choice([-1, 1])],
    [random.choice([-1, 1]), random.choice([-1, 1])]
]

# Функция для движения смайликов
def move_emojis():
    for i in range(len(emoji_positions)):
        emoji_positions[i][0] += emoji_directions[i][0] * 0.3
        emoji_positions[i][1] += emoji_directions[i][1] * 0.3
        if emoji_positions[i][0] <= 0 or emoji_positions[i][0] >= WINDOW_WIDTH - 50:
            emoji_directions[i][0] = -emoji_directions[i][0]
        if emoji_positions[i][1] <= 0 or emoji_positions[i][1] >= WINDOW_HEIGHT - 50:
            emoji_directions[i][1] = -emoji_directions[i][1]

# Звёзды
stars = [{"x": random.randint(0, WINDOW_WIDTH), "y": random.randint(0, WINDOW_HEIGHT), "radius": random.randint(1, 3)} for _ in range(100)]

# Эквалайзер
bar_width = 10
bars = [{"x": i * (bar_width + 2), "height": random.randint(10, 100), "color": (255, 255, 255)} for i in range(WINDOW_WIDTH // (bar_width + 2))]

# Плавное изменение эквалайзера
def update_bars():
    for bar in bars:
        target_height = random.randint(10, 150)
        if bar["height"] < target_height:
            bar["height"] += 5
        elif bar["height"] > target_height:
            bar["height"] -= 5
        bar["color"] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

def draw_equalizer(surface):
    for bar in bars:
        pygame.draw.rect(surface, bar["color"], (bar["x"], WINDOW_HEIGHT - bar["height"], bar_width, bar["height"]))

# Кнопки
FONT_PATH = resource_path("custom_font.ttf")
custom_font = pygame.font.Font(FONT_PATH, 24)

def draw_button_text(surface, text, x, y, color):
    text_surface = custom_font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_button(surface, text, x, y, width, height, color, hover_color, text_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height), border_radius=15)
    else:
        pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    draw_button_text(surface, text, x + (width - custom_font.size(text)[0]) // 2, y + (height - 24) // 2, text_color)

def play_radio():
    global player
    player = vlc.MediaPlayer(RADIO_URL)
    player.play()

def stop_radio():
    global player
    if player:
        player.stop()

# Главная функция
def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Radio Player")

    global player
    player = None
    running = True

    button_width, button_height = 150, 50
    button_x1 = (WINDOW_WIDTH - button_width) // 2
    button_y1 = 350
    button_x2 = (WINDOW_WIDTH - button_width) // 2
    button_y2 = 420

    while running:
        screen.fill(BG_COLOR)
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        for star in stars:
            pygame.draw.circle(screen, (255, 255, 100), (star["x"], star["y"]), star["radius"])

        update_bars()
        draw_equalizer(screen)

        screen.blit(guitar_emoji, emoji_positions[0])
        screen.blit(rock_on_emoji, emoji_positions[1])
        move_emojis()

        draw_button(screen, "Play Radio", button_x1, button_y1, button_width, button_height, BTN_COLOR, BTN_HOVER_COLOR, TEXT_COLOR)
        draw_button(screen, "Stop Radio", button_x2, button_y2, button_width, button_height, BTN_COLOR, BTN_HOVER_COLOR, TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x1 < event.pos[0] < button_x1 + button_width and button_y1 < event.pos[1] < button_y1 + button_height:
                    play_radio()
                if button_x2 < event.pos[0] < button_x2 + button_width and button_y2 < event.pos[1] < button_y2 + button_height:
                    stop_radio()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
