import pygame
import random
import sys
import os
import vlc  # Импортируем библиотеку vlc для воспроизведения радио

# Инициализация Pygame
pygame.init()

# Размеры окна и ресурсы
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BG_COLOR = (20, 20, 20)  # Ярко выраженный темный фон
BTN_COLOR = (50, 50, 50)  # Цвет кнопок (металлик)
BTN_HOVER_COLOR = (80, 80, 80)  # Цвет кнопок при наведении
TEXT_COLOR = (255, 255, 255)  # Цвет текста на кнопках
ACTIVE_COLOR = (0, 255, 0)  # Цвет текста кнопки при активации

# Радио URL
RADIO_URL = "https://cast2.my-control-panel.com/proxy/vladas/stream"

# Иконка для окна
ICON_PATH = "R.ico"  # Иконка для окна (поменяйте на нужный путь к .ico файлу)


# Функция для получения пути к файлам
def resource_path(relative_path):
    """Определяет путь к ресурсам в зависимости от того, с какого места выполняется скрипт."""
    try:
        # Для скомпилированных приложений с PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Для режима разработки (обычный путь)
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

# Уменьшаем размер смайликов
guitar_emoji = pygame.transform.scale(guitar_emoji, (50, 50))
rock_on_emoji = pygame.transform.scale(rock_on_emoji, (50, 50))

# Координаты для смайликов
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
        emoji_positions[i][0] += emoji_directions[i][0] * 0.3  # Уменьшенная скорость
        emoji_positions[i][1] += emoji_directions[i][1] * 0.3
        if emoji_positions[i][0] <= 0 or emoji_positions[i][0] >= WINDOW_WIDTH - 50:
            emoji_directions[i][0] = -emoji_directions[i][0]
        if emoji_positions[i][1] <= 0 or emoji_positions[i][1] >= WINDOW_HEIGHT - 50:
            emoji_directions[i][1] = -emoji_directions[i][1]


# Градусы, которые бегают по экрану
degree_pos = [WINDOW_WIDTH // 2 - 30, 50]
degree_direction = [random.choice([-1, 1]), random.choice([-1, 1])]


def move_degrees():
    global degree_pos, degree_direction
    degree_pos[0] += degree_direction[0] * 0.1  # Скорость уменьшена до 0.1
    degree_pos[1] += degree_direction[1] * 0.1
    if degree_pos[0] <= 10 or degree_pos[0] >= WINDOW_WIDTH - 30:
        degree_direction[0] = -degree_direction[0]
    if degree_pos[1] <= 10 or degree_pos[1] >= WINDOW_HEIGHT - 30:
        degree_direction[1] = -degree_direction[1]


# Эффект осветления фона
def apply_light_effect(surface):
    num_spots = random.randint(1, 5)  # Количество пятен
    for _ in range(num_spots):
        spot_color = (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))  # Светлый цвет
        spot_radius = random.randint(50, 150)
        spot_position = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        pygame.draw.circle(surface, spot_color, spot_position, spot_radius, width=0)


# Эквалайзер
def draw_equalizer(surface):
    num_bars = 10
    bar_width = 15
    spacing = 10
    start_x = (WINDOW_WIDTH - (num_bars * (bar_width + spacing) - spacing)) // 2
    start_y = WINDOW_HEIGHT - 100

    for i in range(num_bars):
        height = random.randint(10, 100)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        pygame.draw.rect(surface, color, (start_x + i * (bar_width + spacing), start_y - height, bar_width, height))


# Переливающийся светопушечный шарик с RGB контуром и прозрачным центром
def draw_glowing_ball(surface, pos, size):
    ball_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    ball_surface.fill((0, 0, 0, 0))  # Прозрачный фон

    for i in range(10, 0, -1):
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        pygame.draw.circle(ball_surface, color, (size, size), size + i, width=3)

    surface.blit(ball_surface, (pos[0] - size, pos[1] - size))


# Загрузка кастомного шрифта
FONT_PATH = resource_path("custom_font.ttf")  # Укажите путь к вашему шрифту
custom_font = pygame.font.Font(FONT_PATH, 24)


# Рисуем текст с кастомным шрифтом
def draw_button_text(surface, text, x, y, color):
    text_surface = custom_font.render(text, True, color)
    surface.blit(text_surface, (x, y))


# Функция для рисования кнопок с округлыми углами
def draw_button(surface, text, x, y, width, height, color, hover_color, text_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height), border_radius=15)
    else:
        pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)

    draw_button_text(surface, text, x + (width - custom_font.size(text)[0]) // 2, y + (height - 24) // 2, text_color)


# Функция для обработки нажатий на кнопки
def handle_button_click(x, y, width, height, event, action):
    if x < event.pos[0] < x + width and y < event.pos[1] < y + height:
        action()


# Функция для воспроизведения радио
def play_radio():
    global player
    player = vlc.MediaPlayer(RADIO_URL)
    player.play()


# Функция для остановки радио
def stop_radio():
    global player
    player.stop()


# Главная функция игры
def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Radio Player")

    global player
    player = None
    running = True
    while running:
        screen.fill(BG_COLOR)
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        apply_light_effect(screen)
        draw_equalizer(screen)
        draw_glowing_ball(screen, (degree_pos[0], degree_pos[1]), 40)

        # Рисуем смайлики
        screen.blit(guitar_emoji, emoji_positions[0])
        screen.blit(rock_on_emoji, emoji_positions[1])

        move_emojis()
        move_degrees()

        # Центрирование кнопок
        button_width, button_height = 150, 50
        button_x1 = (WINDOW_WIDTH - button_width) // 2
        button_y1 = 350
        button_x2 = (WINDOW_WIDTH - button_width) // 2
        button_y2 = 420

        # Рисуем кнопки
        draw_button(screen, "Play Radio", button_x1, button_y1, button_width, button_height, BTN_COLOR, BTN_HOVER_COLOR,
                    TEXT_COLOR)
        draw_button(screen, "Stop Radio", button_x2, button_y2, button_width, button_height, BTN_COLOR, BTN_HOVER_COLOR,
                    TEXT_COLOR)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(button_x1, button_y1, button_width, button_height, event, play_radio)
                handle_button_click(button_x2, button_y2, button_width, button_height, event, stop_radio)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Запуск программы
if __name__ == "__main__":
    main()
