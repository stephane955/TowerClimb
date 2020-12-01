import pygame

from TowerClimb.Settings import *
from TowerClimb.core.GameManager import GameHandle
from TowerClimb.core.placeholder.GameObject import GameObject
from TowerClimb.core.placeholder.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent
vec = pygame.math.Vector2


game_handle = GameHandle("C:/Users/tegui/Downloads/earth-from-space-13.jpg")
game_handle.asset_manager.create_internal_image(40, 80, RED, "hero")
game_handle.asset_manager.create_internal_image(game_handle.window_width, 30, GREEN, "ground")
for plat in Platforms:
    game_handle.asset_manager.create_internal_image(75, 30, BLUE, plat[1])

player = GameObject(vec(game_handle.window_width / 2, game_handle.window_height / 2), "hero", True)
player.add_component(RendererGameObjectComponent("hero", 1, True, "hero", player, True))

player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 40, 1), True, "hero", player, True))  # top
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 80, 40, 10), True, "hero", player, True))  # bottom
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 80), True, "hero", player, True))  # left
player.add_component(CollisionGameObjectComponent(pygame.Rect(40, 0, 1, 80), True, "hero", player, True))  # right

ground = GameObject(vec(0, game_handle.window_height - 30), "ground", True)
ground.add_component(RendererGameObjectComponent("ground", 1, False, "hero", ground, True))
ground.add_component(
    CollisionGameObjectComponent(pygame.Rect(0, 0, game_handle.window_width, 3), False, "ground", ground, True))

# platforms
for plat in Platforms:
    platf = GameObject(*plat)
    platf.add_component(RendererGameObjectComponent(plat[1], 1, False, "platforms", plat, False))

value = player.get_component(CollisionGameObjectComponent)[1].has_no_collisions()
print(value)

vel = vec(0, 0)
pos = vec(game_handle.window_width / 2, game_handle.window_height - 100)
grav = 0
jumping = False
while game_handle.running:
    game_handle.begin()  # Tells the game handle that the game is at the beginning of a new frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        vel.x += - 1 * game_handle.delta_time
    if keys[pygame.K_d]:
        vel.x += 1 * game_handle.delta_time

    player.position.x += vel.x
    if vel.x >= 0:
        vel.x += -0.5 * game_handle.delta_time
    elif vel.x <= 0:
        vel.x += 0.5 * game_handle.delta_time

    if keys[pygame.K_SPACE]:
        player.position.y -= 5

    if player.position.x < 0:
        player.position.x = game_handle.window_width
    if player.position.x > game_handle.window_width:
        player.position.x = 0

    if player.position.y > game_handle.window_height:
        player.position.y = 0

    grav += game_handle.gravity

    if player.get_component(CollisionGameObjectComponent)[3].has_no_collisions():
        player.translate_movement(0, grav)
    else:
        player.translate_movement(0, 0)

    game_handle.physics_update()  # Update all physics (collisions)

    game_handle.clear_screen()  # Clear the screen to display changes

    game_handle.render()  # Render all placeholder

    # Debug
    # if draw_debug:
    game_handle.debug_draw_collider_outlines()

    game_handle.update_screen()

    game_handle.end()  # Finishes everything for the current frame

pygame.quit()  # Exit the program
