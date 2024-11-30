import pygame
import random
import sys
import os

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

# Эффект осветления фона
def apply_light_effect(surface):
    num_spots = random.randint(1, 5)  # Количество пятен
    for _ in range(num_spots):
        spot_color = (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))  # Светлый цвет
        spot_radius = random.randint(50, 150)
        spot_position = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        pygame.draw.circle(surface, spot_color, spot_position, spot_radius, width=0)

# Эффект сияющих звездочек
def draw_stars(surface):
    for _ in range(50):  # Рисуем 50 случайных звездочек
        star_size = random.randint(2, 5)
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        color = (255, random.randint(200, 255), random.randint(200, 255))  # Мягкие светлые цвета
        pygame.draw.circle(surface, color, (x, y), star_size)

# Класс кнопки
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BTN_COLOR
        self.hover_color = BTN_HOVER_COLOR
        self.active_color = ACTIVE_COLOR
        self.text_color = TEXT_COLOR
        self.action = action
        self.is_active = False

    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
            text_color = self.active_color
        else:
            color = self.color
            text_color = self.text_color

        pygame.draw.rect(surface, color, self.rect, border_radius=25)
        font = pygame.font.SysFont("comicsansms", 30)
        shadow_font = pygame.font.SysFont("comicsansms", 30)
        shadow_text = shadow_font.render(self.text, True, (0, 0, 0))
        text_surf = font.render(self.text, True, text_color)
        surface.blit(shadow_text, (self.rect.x + 3, self.rect.y + 3))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                self.is_active = not self.is_active


# Управление радио
player = None

def play_radio():
    global player
    if not player:
        player = vlc.MediaPlayer(RADIO_URL)
    player.play()

def stop_radio():
    global player
    if player:
        player.stop()
        player = None

def pause_radio():
    global player
    if player:
        player.pause()


# Градусы, которые бегают по экрану
degree_pos = [WINDOW_WIDTH // 2 - 30, 50]
degree_direction = [random.choice([-1, 1]), random.choice([-1, 1])]

def move_degrees():
    global degree_pos, degree_direction
    degree_pos[0] += degree_direction[0] * random.randint(1, 3)
    degree_pos[1] += degree_direction[1] * random.randint(1, 3)
    if degree_pos[0] <= 10 or degree_pos[0] >= WINDOW_WIDTH - 30:
        degree_direction[0] = -degree_direction[0]
    if degree_pos[1] <= 10 or degree_pos[1] >= WINDOW_HEIGHT - 30:
        degree_direction[1] = -degree_direction[1]


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
    # Создаем поверхность с прозрачным фоном
    ball_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    ball_surface.fill((0, 0, 0, 0))  # Прозрачный фон

    # Эффект контуров с переливанием цветов
    for i in range(10, 0, -1):  # Уменьшаем размер ореола с каждым кругом
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        pygame.draw.circle(ball_surface, color, (size, size), size + i, width=3)  # Контур с растягивающимся ореолом

    # Рисуем саму поверхность на экране
    surface.blit(ball_surface, (pos[0] - size, pos[1] - size))


# Отображение изображений смайликов
def draw_rock_n_roll_emojis(surface):
    # Отображаем смайлик "гитара" в левом верхнем углу
    guitar_rect = guitar_emoji.get_rect(topleft=(50, 20))
    surface.blit(guitar_emoji, guitar_rect)

    # Отображаем смайлик "рок" в правом верхнем углу
    rock_rect = rock_on_emoji.get_rect(topright=(WINDOW_WIDTH - 50, 20))
    surface.blit(rock_on_emoji, rock_rect)


# Главная функция игры
def main():
    global player
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Radio Player")

    # Загрузка кнопок
    play_button = Button("Play", 50, WINDOW_HEIGHT - 100, 150, 50, play_radio)
    stop_button = Button("Stop", 210, WINDOW_HEIGHT - 100, 150, 50, stop_radio)
    pause_button = Button("Pause", 370, WINDOW_HEIGHT - 100, 150, 50, pause_radio)

    running = True
    while running:
        screen.fill(BG_COLOR)
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Применяем эффект осветления
        apply_light_effect(screen)

        # Рисуем звезды
        draw_stars(screen)

        # Рисуем эквалайзер
        draw_equalizer(screen)

        # Рисуем смайлики
        draw_rock_n_roll_emojis(screen)

        # Переливающийся шарик
        draw_glowing_ball(screen, (degree_pos[0], degree_pos[1]), 40)

        # Отображаем кнопки
        play_button.draw(screen)
        stop_button.draw(screen)
        pause_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            play_button.check_click(event)
            stop_button.check_click(event)
            pause_button.check_click(event)

        # Перемещаем градусы
        move_degrees()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
