import pygame
import random
import sys
import os
import vlc
import shutil


# Функция для получения корректных путей к ресурсам
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Проверка и копирование необходимых файлов
required_files = [
    "WL.jpg",
    "guitar_emoji.png",
    "rock_on_emoji.png",
    "R.ico",
    "custom_font.ttf",
    "button_click.wav"
]

for file in required_files:
    src = resource_path(file)
    dst = os.path.join(os.path.dirname(sys.argv[0]), file)
    if not os.path.exists(src):
        if os.path.exists(file):
            shutil.copy(file, os.path.dirname(sys.argv[0]))
        else:
            raise FileNotFoundError(f"Missing required file: {file}")

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Конфигурация окна
WINDOW_SIZE = (600, 500)
BG_COLOR = (20, 20, 20)

# Цветовая схема кнопок
COLORS = {
    'play': {'normal': (50, 200, 50), 'hover': (30, 170, 30)},
    'stop': {'normal': (200, 50, 50), 'hover': (170, 30, 30)},
    'fx': {'normal': (240, 200, 0), 'hover': (200, 160, 0)},
    'default': {'normal': (50, 150, 200), 'hover': (30, 120, 170)}
}

# Настройки радио
RADIO_URL = "https://cast2.my-control-panel.com/proxy/vladas/stream"


class RadioPlayer:
    def __init__(self):
        self.player = None
        self.volume = 100
        self.is_playing = False
        self.eq = vlc.AudioEqualizer()

    def play(self):
        self.stop()
        try:
            self.player = vlc.MediaPlayer(RADIO_URL)
            self.apply_settings()
            self.player.play()
            self.is_playing = True
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")

    def stop(self):
        if self.player:
            try:
                self.player.stop()
                self.is_playing = False
            except Exception as e:
                print(f"Ошибка остановки: {e}")

    def apply_settings(self):
        if self.player:
            self.player.audio_set_volume(self.volume)
            self.player.set_equalizer(self.eq)

    def set_volume(self, delta):
        self.volume = max(0, min(150, self.volume + delta))
        self.apply_settings()

    def boost_volume(self):
        self.volume = min(150, int(self.volume * 1.2))
        self.eq.set_preamp(20.0)
        self.apply_settings()


class GUI:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Radio Player")
        self.clock = pygame.time.Clock()
        self.radio = RadioPlayer()

        # Загрузка ресурсов
        self.font = pygame.font.Font(resource_path("custom_font.ttf"), 16)
        self.bg_image = pygame.image.load(resource_path("WL.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, WINDOW_SIZE)
        self.button_sound = pygame.mixer.Sound(resource_path("button_click.wav"))

        # Настройка анимированных элементов
        self.load_emojis()
        self.setup_emojis()
        self.init_equalizer()

    def load_emojis(self):
        self.guitar_emoji = pygame.image.load(resource_path("guitar_emoji.png"))
        self.rock_on_emoji = pygame.image.load(resource_path("rock_on_emoji.png"))
        self.guitar_emoji = pygame.transform.scale(self.guitar_emoji, (60, 60))
        self.rock_on_emoji = pygame.transform.scale(self.rock_on_emoji, (60, 60))

    def setup_emojis(self):
        self.emoji_positions = [
            [random.uniform(0, WINDOW_SIZE[0] - 60), random.uniform(0, WINDOW_SIZE[1] - 60)],
            [random.uniform(0, WINDOW_SIZE[0] - 60), random.uniform(0, WINDOW_SIZE[1] - 60)]
        ]
        self.emoji_speeds = [
            [random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)],
            [random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)]
        ]

    def init_equalizer(self):
        self.bar_width = 8
        self.bar_gap = 2
        self.bars = [random.randint(10, 40) for _ in range(25)]
        self.eq_area = (50, 330, 500, 60)

    def move_emojis(self):
        for i in range(2):
            self.emoji_positions[i][0] += self.emoji_speeds[i][0]
            self.emoji_positions[i][1] += self.emoji_speeds[i][1]

            # Обработка столкновений с границами
            if self.emoji_positions[i][0] <= 0 or self.emoji_positions[i][0] >= WINDOW_SIZE[0] - 60:
                self.emoji_speeds[i][0] *= -1
            if self.emoji_positions[i][1] <= 0 or self.emoji_positions[i][1] >= WINDOW_SIZE[1] - 60:
                self.emoji_speeds[i][1] *= -1

    def draw_equalizer(self):
        base_x, base_y, area_width, area_height = self.eq_area
        max_height = area_height - 10

        for i, height in enumerate(self.bars):
            bar_height = min(height, max_height)
            x = base_x + i * (self.bar_width + self.bar_gap)
            y = base_y + (max_height - bar_height)

            pygame.draw.rect(
                self.screen,
                (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                (x, y, self.bar_width, bar_height),
                border_radius=2
            )

        self.bars = [min(max_height, h + random.randint(-3, 3)) for h in self.bars]

    def draw_button(self, text, position, btn_type='default'):
        button_rect = pygame.Rect(position[0], position[1], 90, 40)
        mouse_pos = pygame.mouse.get_pos()
        colors = COLORS.get(btn_type, COLORS['default'])
        color = colors['hover'] if button_rect.collidepoint(mouse_pos) else colors['normal']

        # Определение цвета текста
        text_color = (255, 255, 255)
        if btn_type == 'fx':
            text_color = (30, 30, 30)

        pygame.draw.rect(self.screen, color, button_rect, border_radius=15)
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)
        return button_rect

    def handle_events(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.collidepoint(event.pos):
                            self.button_sound.play()
                            self.handle_button_click(button)

            self.update_display()
            self.clock.tick(60)
        pygame.quit()

    def update_display(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.draw_equalizer()
        self.move_emojis()
        self.screen.blit(self.guitar_emoji, self.emoji_positions[0])
        self.screen.blit(self.rock_on_emoji, self.emoji_positions[1])

        # Отрисовка кнопок
        self.buttons = [
            self.draw_button("PLAY", (60, 340), 'play'),
            self.draw_button("STOP", (160, 340), 'stop'),
            self.draw_button("FX 120%", (260, 340), 'fx'),
            self.draw_button("VOL+", (360, 340), 'default'),
            self.draw_button("VOL-", (460, 340), 'default')
        ]

        # Статусная строка
        status_text = f"ГРОМКОСТЬ: {self.radio.volume}% | СТАТУС: {'ВОСПРОИЗВЕДЕНИЕ' if self.radio.is_playing else 'ПАУЗА'}"
        status_color = (0, 200, 0) if self.radio.is_playing else (200, 0, 0)
        status_surf = self.font.render(status_text, True, status_color)
        self.screen.blit(status_surf, (30, 460))

        pygame.display.flip()

    def handle_button_click(self, button_rect):
        x_pos = button_rect.x
        if x_pos == 60:
            self.radio.play()
        elif x_pos == 160:
            self.radio.stop()
        elif x_pos == 260:
            self.radio.boost_volume()
        elif x_pos == 360:
            self.radio.set_volume(10)
        elif x_pos == 460:
            self.radio.set_volume(-10)


if __name__ == "__main__":
    app = GUI()
    app.handle_events()