import pygame

from pygeon.core.GameManager import GameHandle

game_handle = GameHandle("C:/Users/malte/Desktop/texture_missing.png")

while game_handle.running:

    game_handle.begin()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False

    game_handle.multiplayer_manager.listen()

    game_handle.physics_update()
    game_handle.clear_screen()
    game_handle.animations_tick()

    game_handle.render()

    game_handle.debug_draw_collider_outlines()

    key = pygame.key.get_pressed()

    game_handle.update_screen()

    game_handle.end()

pygame.quit()