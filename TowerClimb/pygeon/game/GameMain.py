from pygeon.core.DebugTextHandler import DebugTextHandler
from pygeon.core.GameObjectSaveManager import GameObjectSaveManager
from pygeon.game.GameLevel import LevelLoader, Level
from pygeon.game.IngameObjects import *

game_handle = GameHandle("C:/Users/malte/Desktop/texture_missing.png")

GAME_STATES = {0 : "MENU", 1 : "PLAYING", 2 : "NONE"}
game_state = 0
level_name = ""

debug_text_handler = DebugTextHandler()

game_handle.asset_manager.create_internal_image(33, 100, (255, 0, 0), "player_image")
game_handle.asset_manager.create_internal_image(300, 50, (220, 220, 220), "box_image")
game_handle.asset_manager.create_internal_image(798, 50, (220, 100, 220), "box_image2")

#player = Player("player_image", pygame.Vector2(100, 100), "Player", True)
player = None
"""
a = GameObject(pygame.Vector2(0, 550), "GROUND", True)
a.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 798, 50), False, "NAME", a, True))
a.add_component(RendererGameObjectComponent("box_image2", 0, (1, 0), "NAME", a, True))

for i in range(-1, 30):
    b = GameObject(pygame.Vector2(game_handle.window_width/2-150, i * -350), "BOX", True)
    b.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 300, 50), False, "NAME", b, True))
    b.add_component(RendererGameObjectComponent("box_image", 0, (1, 0), "NAME", b, True))

for i in range(-1, 30):
    b = GameObject(pygame.Vector2(0, i * -350), "BOX", True)
    b.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 300, 50), False, "NAME", b, True))
    b.add_component(RendererGameObjectComponent("box_image", 0, (1, 0), "NAME", b, True))
for i in range(-1, 30):
    b = GameObject(pygame.Vector2(500, i * -350), "BOX", True)
    b.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 300, 50), False, "NAME", b, True))
    b.add_component(RendererGameObjectComponent("box_image", 0, (1, 0), "NAME", b, True))

save = GameObjectSaveManager()
save.save("C:/Users/malte/Desktop/pygame/Level_Test_03.txt")
"""

while game_handle.running:

    game_handle.begin()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_x]:
                player = Level("Level_Test_01", "C:/Users/malte/Desktop/pygame/").set()
                level_name = "Level_Test_01"
                game_state = 1
            if key[pygame.K_y]:
                player = Level("Level_Test_02", "C:/Users/malte/Desktop/pygame/").set()
                level_name = "Level_Test_02"
                game_state = 1
            if key[pygame.K_z]:
                player = Level("Level_Test_03", "C:/Users/malte/Desktop/pygame/").set()
                level_name = "Level_Test_03"
                game_state = 1
            if key[pygame.K_c]:
                game_handle.multiplayer_manager.connect()

    game_handle.multiplayer_manager.listen()

    # ---
    if game_state == 1:
        player.handle_player_movement(game_handle.delta_time)

        game_handle.camera.follow(player, (game_handle.window_width/2, game_handle.window_height/2))
    # ---

    game_handle.physics_update()
    game_handle.clear_screen()
    game_handle.animations_tick()

    game_handle.render()

    # ---
    debug_text_handler.render_text((0, 0), "STATE: " + GAME_STATES[game_state], (255, 0, 0), game_handle)
    debug_text_handler.render_text((0, 20), "LEVEL: " + level_name, (255, 0, 0), game_handle)
    debug_text_handler.render_text((0, 40), "SERVER: " +
                                   ("CONNECTED" if game_handle.multiplayer_manager.is_connected() else "NOT CONNECTED"),
                                   (255, 0, 0), game_handle)

    debug_text_handler.render_text((540, 0), "PRESS [X], [Y] OR [Z] TO LOAD A LEVEL ", (255, 125, 125), game_handle)
    debug_text_handler.render_text((540, 20), "PRESS [C] TO CONNECT", (255, 125, 125), game_handle)

    for i in range(len(game_handle.multiplayer_manager.server_log)):
        debug_text_handler.render_text((0, 560+i*20), game_handle.multiplayer_manager.server_log[i], (153, 153, 0), game_handle)

    if player is not None:
        debug_text_handler.render_text((0, 60), "PLAYER: " + "[" + str(player.get_x())+"|"+str(player.get_y())+"]", (255, 0, 255), game_handle)
        debug_text_handler.render_text((0, 80),
                                       "GROUNDED: " + str(player.get_component(PhysicsGameObjectComponent)[0].grounded),
                                       (255, 0, 255), game_handle)
        debug_text_handler.render_text((0, 100),
                                       "VELOCITY: " + str(player.get_component(PhysicsGameObjectComponent)[0].velocity),
                                       (255, 0, 255), game_handle)

        debug_text_handler.render_text((player.get_x() - game_handle.camera.get_x()-15, player.get_y() - 20 - game_handle.camera.get_y()), "SPIELER",(0, 0, 0), game_handle)
    # ---

    #game_handle.debug_draw_collider_outlines()

    key = pygame.key.get_pressed()

    game_handle.update_screen()

    game_handle.end()

pygame.quit()