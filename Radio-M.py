import pygame
import vlc
import os
import sys
import random

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
ICON_PATH = "R.ico"  # Иконка для окна
if hasattr(sys, "_MEIPASS"):  # Если запущено из PyInstaller
    ICON_PATH = os.path.join(sys._MEIPASS, ICON_PATH)
pygame.display.set_icon(pygame.image.load(ICON_PATH))

# Загрузка фона
if hasattr(sys, "_MEIPASS"):  # Если запущено из PyInstaller
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.abspath(".")

BACKGROUND_IMAGE_PATH = os.path.join(BASE_PATH, "WL.jpg")
BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGE_PATH)
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Эффект осветления фона
def apply_light_effect(surface):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((255, 255, 255))  # Белый цвет для осветления
    overlay.set_alpha(50)  # Уровень прозрачности, можно настроить
    surface.blit(overlay, (0, 0))  # Наложение на экран

# Эффект сияющих звездочек
def draw_stars(surface):
    for _ in range(50):  # Рисуем 50 случайных звездочек
        star_size = random.randint(2, 5)
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        color = (255, random.randint(200, 255), random.randint(200, 255))  # Мягкие светлые цвета
        pygame.draw.circle(surface, color, (x, y), star_size)

# Создаем окно
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("M-Radio Player")

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
        # Подсветка текста
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
            text_color = self.active_color
        else:
            color = self.color
            text_color = self.text_color

        # Отрисовка кнопки (скругленные углы без рамки)
        pygame.draw.rect(surface, color, self.rect, border_radius=25)

        # Отрисовка текста
        font = pygame.font.SysFont("comicsansms", 30)  # Используем более интересный шрифт Comic Sans MS
        shadow_font = pygame.font.SysFont("comicsansms", 30)  # Шрифт для тени
        shadow_text = shadow_font.render(self.text, True, (0, 0, 0))  # Черная тень
        text_surf = font.render(self.text, True, text_color)  # Основной текст

        # Отрисовка тени
        surface.blit(shadow_text, (self.rect.x + 3, self.rect.y + 3))  # Тень немного смещена

        # Отрисовка основного текста
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                self.is_active = not self.is_active  # Переключение статуса кнопки

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

# Создаем градусы, которые бегают по экрану
degree_pos = [WINDOW_WIDTH // 2 - 30, 50]
degree_direction = [random.choice([-1, 1]), random.choice([-1, 1])]  # Направление движения градуса

def move_degrees():
    global degree_pos, degree_direction
    # Изменение позиции градуса для "бега"
    degree_pos[0] += degree_direction[0] * random.randint(1, 3)  # Замедлил движение
    degree_pos[1] += degree_direction[1] * random.randint(1, 3)  # Замедлил движение

    # Отражение от границ экрана
    if degree_pos[0] <= 10 or degree_pos[0] >= WINDOW_WIDTH - 30:
        degree_direction[0] = -degree_direction[0]
    if degree_pos[1] <= 10 or degree_pos[1] >= WINDOW_HEIGHT - 30:
        degree_direction[1] = -degree_direction[1]

# Эквалайзер с меняющимися цветами
def draw_eq(surface):
    num_bars = 4  # Меньше полос
    bar_width = 40
    bar_height_max = 80
    for i in range(num_bars):
        bar_height = random.randint(20, bar_height_max)  # Случайная высота для каждого бара
        bar_color = random.choice([(0, 255, 255), (255, 105, 180), (144, 238, 144), (255, 255, 224)])  # Мягкие цвета
        pygame.draw.rect(surface, bar_color, pygame.Rect(i * 60 + 70, 20, bar_width, bar_height))

# Создаем кнопки
buttons = [
    Button("Play", (WINDOW_WIDTH - 150) // 2, 200, 150, 50, action=play_radio),
    Button("Pause", (WINDOW_WIDTH - 150) // 2, 275, 150, 50, action=pause_radio),
    Button("Stop", (WINDOW_WIDTH - 150) // 2, 350, 150, 50, action=stop_radio)
]

# Основной цикл приложения
def main():
    running = True
    while running:
        screen.fill(BG_COLOR)  # Применяем ярко выраженный темный фон для окна
        screen.blit(BACKGROUND_IMAGE, (0, 0))  # Отображаем фоновое изображение

        # Применяем эффект осветления фона
        apply_light_effect(screen)

        # Рисуем сияющие звездочки
        draw_stars(screen)

        # Перемещаем и рисуем градусы
        move_degrees()
        font = pygame.font.Font(None, 150)
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)])  # Разноцветные градусы
        text = font.render("°", True, color)  # Создание градуса с случайным цветом
        screen.blit(text, (degree_pos[0], degree_pos[1]))  # Рисуем градус

        # Рисуем эквалайзер
        draw_eq(screen)

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.check_click(event)

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    if player:
        player.stop()

if __name__ == "__main__":
    main()
