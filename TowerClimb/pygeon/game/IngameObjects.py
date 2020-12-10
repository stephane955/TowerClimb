import pygame

from pygeon.core.GameManager import GameHandle
from pygeon.core.misc.GameObject import GameObject
from pygeon.core.misc.GameObjectComponents import *


class Player(GameObject):

    def __init__(self, image_asset_id: str, position, name, active):
        super().__init__(position, name, active)

        self.add_component(RendererGameObjectComponent(image_asset_id, 2, (1, 1), "renderer_player", self, True))

        self.add_component(
            CollisionGameObjectComponent(pygame.Rect(0, 0, 33, 2), True, "collision_component_top", self, True))
        self.add_component(
            CollisionGameObjectComponent(pygame.Rect(33, 2, 2, 96), True, "collision_component_right", self, True))
        self.add_component(
            CollisionGameObjectComponent(pygame.Rect(0, 2, 2, 96), True, "collision_component_left", self, True))

        self.add_component(
            PhysicsGameObjectComponent(pygame.Rect(2, 92, 29, 10), True, 100, "physics_player", self, True))

    def handle_player_movement(self, delta_time):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            pass
        if key[pygame.K_s]:
            pass
        if key[pygame.K_a]:
            if not self.get_component_by_name("collision_component_left").get_active_collisions_count() > 0:
                if self.get_component_by_name("physics_player").grounded:
                    self.translate_movement(-200 * delta_time, 0)
                else:
                    self.translate_movement(-450 * delta_time, 0)
        if key[pygame.K_d]:
            if not self.get_component_by_name("collision_component_right").get_active_collisions_count() > 0:
                if self.get_component_by_name("physics_player").grounded:
                    self.translate_movement(200 * delta_time, 0)
                else:
                    self.translate_movement(450 * delta_time, 0)
        if key[pygame.K_SPACE]:
            if self.get_component_by_name("physics_player").grounded:
                self.get_component_by_name("physics_player").velocity.y = -1500

        if self.get_component_by_name("collision_component_top").get_active_collisions_count() > 0:
            if not self.get_component_by_name("physics_player").grounded and\
                    self.get_component_by_name("physics_player").velocity.y < 0:
                self.get_component_by_name("physics_player").velocity.y = 0

