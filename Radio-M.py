import pygame
import random
import sys
import os
import vlc
import shutil
import ctypes
from configparser import ConfigParser
from math import sin, cos

# ========== КОНФИГУРАЦИЯ ==========
APP_NAME = "M Radio"
APP_VERSION = "2.0"
APP_SIZE = (1280, 720)
APP_ICON = "R.ico"
RADIO_URL = "https://cast2.my-control-panel.com/proxy/vladas/stream"
FPS = 60
FONT_PATH = "Roboto-Italic-VariableFont_wdth,wght.ttf"

# ========== WINDOWS APP ID ==========
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("RadioPlayer.Company.2.0")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ========== ЦВЕТОВАЯ СХЕМА ==========
def load_colors():
    config = ConfigParser()
    config.read(resource_path('colors.ini'), encoding='utf-8')

    return {
        'background': tuple(map(int, config.get('Colors', 'background').split(','))),
        'text': tuple(map(int, config.get('Colors', 'text_primary').split(','))),
        'accent': tuple(map(int, config.get('Colors', 'accent').split(','))),
        'btn_primary': tuple(map(int, config.get('Buttons', 'primary').split(','))),
        'btn_secondary': tuple(map(int, config.get('Buttons', 'secondary').split(','))),
        'btn_danger': tuple(map(int, config.get('Buttons', 'danger').split(','))),
        'btn_volume': tuple(map(int, config.get('Buttons', 'volume').split(','))),
        'hover_modifier': 40
    }


# ========== ПРОВЕРКА РЕСУРСОВ ==========
REQUIRED_FILES = [
    'WL.jpg', 'guitar_emoji.png', 'rock_on_emoji.png',
    'R.ico', FONT_PATH, 'button_click.wav', 'colors.ini'
]

for file in REQUIRED_FILES:
    src = resource_path(file)
    if not os.path.exists(src):
        if os.path.exists(file):
            shutil.copy(file, os.path.dirname(sys.argv[0]))
        else:
            raise FileNotFoundError(f"Отсутствует файл: {file}")


# ========== АУДИОПЛЕЕР ==========
class RadioPlayer:
    def __init__(self):
        self.player = None
        self.volume = 80
        self.is_playing = False
        self.eq = vlc.AudioEqualizer()

    def play(self, url):
        self.stop()
        try:
            self.player = vlc.MediaPlayer(url)
            self.player.audio_set_volume(self.volume)
            self.player.set_equalizer(self.eq)
            self.player.play()
            self.is_playing = True
        except Exception as e:
            print(f"Ошибка воспроизведения: {str(e)}")

    def stop(self):
        if self.player:
            self.player.stop()
            self.is_playing = False

    def set_volume(self, delta):
        self.volume = max(0, min(100, self.volume + delta))
        if self.player:
            self.player.audio_set_volume(self.volume)

    def boost_audio(self):
        self.eq.set_preamp(25.0)
        if self.player:
            self.player.set_equalizer(self.eq)


# ========== ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ==========
class RadioApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Настройка окна
        self.screen = pygame.display.set_mode(APP_SIZE)
        pygame.display.set_caption(f"{APP_NAME} {APP_VERSION}")
        self.set_window_icon()

        # Ресурсы
        self.colors = load_colors()
        self.font = self.load_font()
        self.button_sound = pygame.mixer.Sound(resource_path('button_click.wav'))
        self.radio = RadioPlayer()

        # Графика и анимация
        self.load_assets()
        self.init_animation()
        self.init_ui()

    def set_window_icon(self):
        try:
            icon = pygame.image.load(resource_path(APP_ICON))
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Ошибка иконки: {str(e)}")

    def load_font(self):
        try:
            return pygame.font.Font(resource_path(FONT_PATH), 28)
        except Exception as e:
            print(f"Ошибка шрифта: {str(e)}")
            return pygame.font.SysFont("Arial", 28)

    def load_assets(self):
        self.background = pygame.transform.scale(
            pygame.image.load(resource_path('WL.jpg')), APP_SIZE)

        self.emojis = {
            'guitar': pygame.image.load(resource_path('guitar_emoji.png')).convert_alpha(),
            'rock': pygame.image.load(resource_path('rock_on_emoji.png')).convert_alpha()
        }
        self.emojis = {k: pygame.transform.smoothscale(v, (160, 160)) for k, v in self.emojis.items()}

    def init_animation(self):
        self.animation_time = 0.0
        self.emoji_positions = {
            'guitar': [200, 200],
            'rock': [1000, 300]
        }

    def init_ui(self):
        self.button_layout = [
            {"text": "ВКЛЮЧИТЬ", "type": "primary", "pos": (50, 650)},
            {"text": "СТОП", "type": "danger", "pos": (250, 650)},
            {"text": "УСИЛИТЬ", "type": "secondary", "pos": (450, 650)},
            {"text": "+", "type": "volume", "pos": (650, 650)},
            {"text": "-", "type": "volume", "pos": (750, 650)}
        ]

        self.eq_bars = [{
            'height': random.randint(20, 80),
            'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
            'speed': random.uniform(1.0, 2.0),
            'target': 50
        } for _ in range(25)]

    def update_emojis(self, delta_time):
        self.animation_time += delta_time * 1.5

        # Анимация гитары
        self.emoji_positions['guitar'][0] = 200 + cos(self.animation_time * 1.2) * 120
        self.emoji_positions['guitar'][1] = 200 + sin(self.animation_time * 1.5) * 80

        # Анимация рок-жеста
        self.emoji_positions['rock'][1] = 300 + sin(self.animation_time * 2.0) * 60

    def draw_button(self, text, pos, btn_type):
        btn_width = 160 if len(text) > 4 else 80
        btn_rect = pygame.Rect(pos[0], pos[1], btn_width, 60)

        # Цвета
        base_color = self.colors[f'btn_{btn_type}']
        border_color = tuple(min(c + 80, 255) for c in base_color)
        is_hovered = btn_rect.collidepoint(pygame.mouse.get_pos())

        # Отрисовка
        pygame.draw.rect(self.screen,
                         tuple(min(c + 40, 255) for c in base_color) if is_hovered else base_color,
                         btn_rect,
                         border_radius=18
                         )
        pygame.draw.rect(self.screen, border_color, btn_rect, 3, border_radius=18)

        # Текст
        text_surf = self.font.render(text, True, self.colors['text'])
        text_rect = text_surf.get_rect(center=btn_rect.center)
        self.screen.blit(text_surf, text_rect)

        return btn_rect

    def draw_equalizer(self, delta_time):
        base_x, base_y = 100, 500
        max_height = 120

        for i, bar in enumerate(self.eq_bars):
            # Динамическое изменение целей
            if random.random() < 0.02:
                bar['target'] = random.randint(20, max_height)

            # Плавное движение
            bar['height'] += (bar['target'] - bar['height']) * delta_time * bar['speed']

            # Отрисовка
            x = base_x + i * (40 + 5)
            y = base_y + (max_height - min(bar['height'], max_height))

            # Градиент цвета
            color = (
                max(0, min(255, bar['color'][0] + int(bar['height']))),
                max(0, min(255, bar['color'][1] - int(bar['height'] / 2))),
                max(0, min(255, bar['color'][2]))
            )

            pygame.draw.rect(
                self.screen,
                color,
                (x, y, 40, min(bar['height'], max_height)),
                border_radius=5
            )

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            delta_time = clock.tick(FPS) / 1000.0

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for btn in self.button_layout:
                        btn_rect = pygame.Rect(btn['pos'][0], btn['pos'][1], 160 if len(btn['text']) > 4 else 80, 60)
                        if btn_rect.collidepoint(mouse_pos):
                            self.handle_click(btn['type'])

            # Обновление анимаций
            self.update_emojis(delta_time)

            # Отрисовка
            self.screen.blit(self.background, (0, 0))

            # Смайлы
            self.screen.blit(self.emojis['guitar'], self.emoji_positions['guitar'])
            self.screen.blit(self.emojis['rock'], self.emoji_positions['rock'])

            # Кнопки
            for btn in self.button_layout:
                self.draw_button(btn['text'], btn['pos'], btn['type'])

            # Эквалайзер
            self.draw_equalizer(delta_time)

            pygame.display.flip()

        pygame.quit()

    def handle_click(self, btn_type):
        self.button_sound.play()
        if btn_type == 'primary':
            self.radio.play(RADIO_URL)
        elif btn_type == 'danger':
            self.radio.stop()
        elif btn_type == 'secondary':
            self.radio.boost_audio()
        elif btn_type == 'volume':
            self.radio.set_volume(
                5 if '+' in [b['text'] for b in self.button_layout if b['type'] == 'volume'][0] else -5)


if __name__ == "__main__":
    app = RadioApp()
    app.run()