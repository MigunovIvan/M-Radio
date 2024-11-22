import vlc
import pygame
import sys
import os

# URL радиостанции
RADIO_URL = "https://cast2.my-control-panel.com/proxy/vladas/stream"


class RadioPlayerApp:
    def __init__(self):
        pygame.init()
        self.width, self.height = 500, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎵 Радио-плеер")

        # Загрузка обложки
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_path, "WL.jpg")
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Цветовая палитра
        self.button_color = (0, 150, 255)
        self.hover_color = (0, 200, 255)
        self.active_color = (0, 100, 200)
        self.text_color = (255, 255, 255)

        # Инициализация VLC
        self.player = vlc.MediaPlayer(RADIO_URL)
        self.is_playing = False

        # Шрифты
        self.font_large = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 24)

        # Кнопки
        self.buttons = {
            "play": pygame.Rect(200, 150, 100, 50),
            "pause": pygame.Rect(200, 220, 100, 50),
            "stop": pygame.Rect(200, 290, 100, 50),
        }

        # Состояние кнопок
        self.button_states = {key: False for key in self.buttons}

    def draw_background(self):
        """Рисует фон."""
        self.screen.blit(self.background, (0, 0))

    def draw_buttons(self):
        """Рисует кнопки управления."""
        for name, rect in self.buttons.items():
            mouse_pos = pygame.mouse.get_pos()
            if self.button_states[name]:
                color = self.active_color
            elif rect.collidepoint(mouse_pos):
                color = self.hover_color
            else:
                color = self.button_color

            pygame.draw.rect(self.screen, color, rect, border_radius=10)

            text = self.font_small.render(name.capitalize(), True, self.text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_title(self):
        """Рисует заголовок."""
        title_text = self.font_large.render("🎶 Radio Player 🎶", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)

    def play_radio(self):
        self.player.play()
        self.is_playing = True

    def pause_radio(self):
        self.player.pause()
        self.is_playing = False

    def stop_radio(self):
        self.player.stop()
        self.is_playing = False

    def run(self):
        """Основной цикл приложения."""
        running = True
        while running:
            self.draw_background()
            self.draw_title()
            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for name, rect in self.buttons.items():
                        if rect.collidepoint(mouse_pos):
                            self.button_states[name] = True
                            if name == "play":
                                self.play_radio()
                            elif name == "pause":
                                self.pause_radio()
                            elif name == "stop":
                                self.stop_radio()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for name in self.buttons:
                        self.button_states[name] = False

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = RadioPlayerApp()
    app.run()
