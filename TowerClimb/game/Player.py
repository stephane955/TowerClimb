from TowerClimb.pygeon.core.misc.GameObject import *
from TowerClimb.pygeon.core.GameManager import *


class Player(GameObject):

    def __init__(self, position: pygame.Vector2, name, active=True):
        super().__init__(position, name, active)
        self.vel = pygame.Vector2(0, 0)

    def controls(self, left, right, game_handle):
        keys = pygame.key.get_pressed()
        if keys[left]:
            self.vel.x += - 1 * game_handle.delta_time
        if keys[right]:
            self.vel.x += 1 * game_handle.delta_time

        self.translate_movement(self.vel.x, self.vel.y)
        if self.vel.x >= 0:
            self.vel.x += -0.5 * game_handle.delta_time
        elif self.vel.x <= 0:
            self.vel.x += 0.5 * game_handle.delta_time
