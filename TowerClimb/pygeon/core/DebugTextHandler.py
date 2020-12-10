import pygame


class DebugTextHandler:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 20)
        self.texts = {}

    def create_text(self, position: (int, int), text, color, id):
        self.texts[id] = DebugText(position, self.font.render(text, True, color))

    def render_text(self, position: (int, int), text, color, game_handle):
        game_handle.screen.blit(self.font.render(text, True, color), position)


class DebugText:

    def __init__(self, position, image):
        self.position = position
        self.image = image
