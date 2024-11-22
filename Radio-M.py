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

        # Цветовая палитра для тёмной темы
        self.button_color = (60, 60, 60)
        self.hover_color = (80, 80, 80)
        self.active_color = (30, 144, 255)
        self.text_color = (255, 255, 255)

        # Инициализация VLC
        self.player = vlc.MediaPlayer(RADIO_URL)
        self.is_playing = False

        # Шрифты
        base_font_path = pygame.font.match_font('segoeui', bold=True)
        self.font_large = pygame.font.Font(base_font_path, 36)
        self.font_small = pygame.font.Font(base_font_path, 24)

        # Кнопки
        self.buttons = {
            "play": {"rect": pygame.Rect(200, 150, 100, 50), "active": False},
            "pause": {"rect": pygame.Rect(200, 220, 100, 50), "active": False},
            "stop": {"rect": pygame.Rect(200, 290, 100, 50), "active": False},
        }

        # Анимация увеличения
        self.hover_scale = 10  # Насколько увеличивается кнопка при наведении

    def draw_background(self):
        """Рисует фон."""
        # Затемняем обложку для тёмной темы
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # Полупрозрачный чёрный
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(overlay, (0, 0))

    def draw_buttons(self):
        """Рисует кнопки управления."""
        mouse_pos = pygame.mouse.get_pos()

        for name, button in self.buttons.items():
            rect = button["rect"]
            is_hovered = rect.collidepoint(mouse_pos)
            is_active = button["active"]

            # Определяем цвет кнопки
            if is_active:
                color = self.active_color
            elif is_hovered:
                color = self.hover_color
            else:
                color = self.button_color

            # Увеличиваем кнопку при наведении
            draw_rect = rect.inflate(
                self.hover_scale if is_hovered else 0,
                self.hover_scale if is_hovered else 0
            )
            pygame.draw.rect(self.screen, color, draw_rect, border_radius=10)

            # Рисуем текст на кнопке
            text = self.font_small.render(name.capitalize(), True, self.text_color)
            text_rect = text.get_rect(center=draw_rect.center)
            self.screen.blit(text, text_rect)

    def draw_title(self):
        """Рисует заголовок."""
        title_text = self.font_large.render("🎶 Radio Player 🎶", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)

    def play_radio(self):
        self.player.play()
        self.is_playing = True
        self.set_button_state("play")

    def pause_radio(self):
        self.player.pause()
        self.is_playing = False
        self.set_button_state("pause")

    def stop_radio(self):
        self.player.stop()
        self.is_playing = False
        self.set_button_state("stop")

    def set_button_state(self, active_button):
        """Обновляет состояние кнопок."""
        for name in self.buttons:
            self.buttons[name]["active"] = (name == active_button)

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
                    for name, button in self.buttons.items():
                        if button["rect"].collidepoint(mouse_pos):
                            if name == "play":
                                self.play_radio()
                            elif name == "pause":
                                self.pause_radio()
                            elif name == "stop":
                                self.stop_radio()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = RadioPlayerApp()
    app.run()
