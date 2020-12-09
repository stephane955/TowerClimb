from TowerClimb.pygeon.core.misc.GameObject import *
from TowerClimb.pygeon.core.GameManager import *


class Player(GameObject):

    def __init__(self, position: pygame.Vector2, name, active=True):
        super().__init__(position, name, active)
        self.vel = pygame.Vector2(0, 0)
        self.right = False
        self.left = False

    # set controls for the player instance
    def controls(self, left, right, game_handle):

        keys = pygame.key.get_pressed()
        if keys[left]:
            # list for image to be drawn changes according to pressed key
            self.left = True
            self.right = False
            self.get_component(ImageAnimationGameObjectComponent)[0].current_animation_id = "run_left"
            self.vel.x += - 1 * game_handle.delta_time
        elif keys[right] and self.position.x + 80 < game_handle.window_width:
            self.get_component(ImageAnimationGameObjectComponent)[0].current_animation_id = "run_right"
            self.left = False
            self.right = True
            self.vel.x += 1 * game_handle.delta_time

        elif not keys[left] and self.left:
            self.get_component(ImageAnimationGameObjectComponent)[0].current_animation_id = "idle_left"
        elif not keys[right] and self.right:
            self.get_component(ImageAnimationGameObjectComponent)[0].current_animation_id = "idle_right"

        #makes player move
        self.translate_movement(self.vel.x, self.vel.y)

        # player cannot cross the screen boundaries
        if self.position.x + 50 > game_handle.window_width and not keys[left]:
            self.vel.x = 0
        if self.position.x - 10 < 0 and not keys[right]:
            self.vel.x = 0

        # avoids collisions
        if not self.get_component_by_name("player_physics_left").has_no_collisions() and not keys[right]:
            self.vel.x = 0
        if not self.get_component_by_name("player_physics_right").has_no_collisions() and not keys[left]:
            self.vel.x = 0
        if self.vel.x >= 0:
            self.vel.x += self.vel.x * -0.002
        elif self.vel.x <= 0:
            self.vel.x += self.vel.x * -0.002
