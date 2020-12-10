import json

from pygeon.core.DebugTextHandler import *
from pygeon.core.GameManager import GameHandle
from pygeon.core.data.SerializationHelper import Serializer
from pygeon.core.misc.GameObject import *
from pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent

game_handle = GameHandle("C:/Users/malte/Desktop/texture_missing.png")

game_handle.asset_manager.load_image("C:/Users/malte/Desktop/goofy.png", "goofy")
GameObject(pygame.Vector2(game_handle.window_width/2-278, game_handle.window_height/2-328), "Goofy", True)\
    .add_component(RendererGameObjectComponent("goofy", 0, (1, 1), "goofy_renderer", None, True))
debug_text_handler = DebugTextHandler()

game_handle.multiplayer_manager.connect()
game_handle.multiplayer_manager.create_lobby("LOBBY_NAME", 10)

while game_handle.running:

    game_handle.begin()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                game_handle.multiplayer_manager.join_lobby("abcde", "WKFA4WcqxOypgZQK")
            if key[pygame.K_s]:
                game_handle.multiplayer_manager.init_get_all_objects()

    game_handle.multiplayer_manager.listen()

    game_handle.physics_update()
    game_handle.clear_screen()
    game_handle.animations_tick()

    game_handle.render()

    #
    debug_text_handler.render_text((0, 0), "net_last: "+game_handle.multiplayer_manager.debug_last_network_message, (255, 0, 0), game_handle)
    #

    game_handle.debug_draw_collider_outlines()

    game_handle.update_screen()

    game_handle.end()

pygame.quit()