from TowerClimb.game.Player import Player
from TowerClimb.pygeon.core.GameManager import GameHandle
from TowerClimb.pygeon.core.misc.GameObject import GameObject
from TowerClimb.pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent, \
    PhysicsGameObjectComponent, ImageAnimationGameObjectComponent
from TowerClimb.game.Settings import *

path = "C:/Users/tegui/OneDrive/Dokumente/GitHub Desktop/TowerClimb/TowerClimb/game/Individual Sprites/"
idle = [path+"aventurer-idle-00.png", path+"aventurer-idle-01.png", path+"aventurer-idle-2-00.png", path+"aventurer-idle-2-01.png",
        path+"aventurer-idle-2-02.png", path+"aventurer-idle-2-03.png", path+"aventurer-idle-02.png", path+"aventurer-idle-03.png"]

"""for image in idle:
    pla"""

game_handle = GameHandle("C:/Users/tegui/OneDrive/Python/earth.jpg")


#Platforms are been drawn
for plat in Platforms:
    game_handle.asset_manager.create_internal_image(100, 30, GREEN, plat[1])
    platf = GameObject(*plat)
    platf.add_component(RendererGameObjectComponent(plat[1], 1, (0, 0), "platforms", plat, False))
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 0, 100, -10), False, plat[1] + "t", platf, True))  # top
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 30, 100, 1), False, plat[1] + "b", platf, True))  # bottom
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 30), False, plat[1] + "l", platf, True))  # left
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(100, 0, 1, 30), False, plat[1] + "r", platf, True))  # right

#Player and components
game_handle.asset_manager.create_internal_image(40, 80, RED, "player")
player = Player(pygame.Vector2(game_handle.window_width / 2, game_handle.window_height / 2), "player", True)
player.add_component(ImageAnimationGameObjectComponent(idle, 2, "player", 1, (1,1), "hero", player, True))
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 40, 1), True, "playert", player, True))  # top
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 80, 40, 1), True, "playerb", player, True))  # bottom
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 80), True, "playerl", player, True))  # left
player.add_component(CollisionGameObjectComponent(pygame.Rect(40, 0, 1, 80), True, "playerr", player, True))  # right
player.add_component(PhysicsGameObjectComponent(pygame.Rect(0, 80, 40, 1), True, 80, "playerphysics", player, True))

#Ground and components
game_handle.asset_manager.create_internal_image(game_handle.window_width, 30, GREEN, "ground")
ground = GameObject(vec(0, game_handle.window_height - 30), "ground", True)
ground.add_component(RendererGameObjectComponent("ground", 1, (0, 0), "hero", ground, True))
ground.add_component(
    CollisionGameObjectComponent(pygame.Rect(0, 0, game_handle.window_width, -10), False, "groundcomp", ground, True))



while game_handle.running:
    game_handle.begin()  # Tells the game handle that the game is at the beginning of a new frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False

    keys = pygame.key.get_pressed()

    player.controls(pygame.K_q, pygame.K_d, game_handle)

    #change camera position
    if player.position.y < 0:
        game_handle.camera.position.y = player.position.y - 80
    else:
        game_handle.camera.position = pygame.Vector2(0, 0)



    if keys[pygame.K_SPACE]:
        if player.get_component_by_name("playerphysics").grounded:
            player.get_component_by_name("playerphysics").velocity.y -= 300
    player.get_component_by_name("playert").collisions[0].position.y

    if player.position.x < 0:
        player.position.x = game_handle.window_width
    if player.position.x > game_handle.window_width:
        player.position.x = 0

    if player.position.y > game_handle.window_height:
        player.position.y = 0

    game_handle.physics_update()  # Update all physics (collisions)

    game_handle.clear_screen()  # Clear the screen to display changes

    game_handle.render()  # Render all placeholder

    # Debug
    # if draw_debug:
    game_handle.debug_draw_collider_outlines()

    game_handle.update_screen()

    game_handle.end()  # Finishes everything for the current frame

pygame.quit()  # Exit the program
