from TowerClimb.game.Player import Player
from TowerClimb.pygeon.core.GameManager import GameHandle
from TowerClimb.pygeon.core.misc.GameObject import GameObject
from TowerClimb.pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent,\
    PhysicsGameObjectComponent
from TowerClimb.game.Settings import *

path = "C:/Users/tegui/OneDrive/Dokumente/GitHub/TowerClimb/TowerClimb/game"
Idle = [path+"/papi/Idle (1).hero", path+"/papi/Idle (2).hero",
            path+"/papi/Idle (3).hero", path+"/papi/Idle (4).hero",
            path+"/papi/Idle (5).hero", path+"/papi/Idle (6).hero",
            path+"/papi/Idle (7).hero", path+"/papi/Idle (8).hero",
            path+"/papi/Idle (9).hero", path+"/papi/Idle (10).hero",
            path+"/papi/Idle (11).hero", path+"/papi/Idle (12).hero",
            path+"/papi/Idle (13).hero", path+"/papi/Idle (14).hero",
            path+"/papi/Idle (15).hero", path+"/papi/Idle (16).hero"]

game_handle = GameHandle("C:/Users/tegui/Downloads/earth-from-space-13.jpg")


game_handle.asset_manager.create_internal_image(game_handle.window_width, 30, GREEN, "ground")
for plat in Platforms:
    game_handle.asset_manager.create_internal_image(100, 30, GREEN, plat[1])
    platf = GameObject(*plat)
    platf.add_component(RendererGameObjectComponent(plat[1], 1, (0, 0), "platforms", plat, False))
    platf.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 100, -10), False, plat[1]+"t", platf, True)) #top
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 30, 100, 1), False, plat[1]+"b", platf, True))  # bottom
    platf.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 30), False, plat[1]+"l", platf, True))  # left
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(100, 0, 1, 30), False, plat[1]+"r", platf, True))  # right


player = Player(vec(game_handle.window_width / 2, game_handle.window_height / 2), "player", True)

player.add_component(RendererGameObjectComponent("player", 1, (0, 0), "player", player, True))

player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 40, 1), True, "playert", player, True))  # top
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 80, 40, 1), True, "playerb", player, True))  # bottom
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 75), True, "playerl", player, True))  # left
player.add_component(CollisionGameObjectComponent(pygame.Rect(40, 0, 1, 75), True, "playerr", player, True))  # right
player.add_component(PhysicsGameObjectComponent(pygame.Rect(0, 80, 40, 1), True, 80, "playerphysics", player, True))

ground = GameObject(vec(0, game_handle.window_height - 30), "ground", True)
ground.add_component(RendererGameObjectComponent("ground", 1, (0, 0), "hero", ground, True))
ground.add_component(
    CollisionGameObjectComponent(pygame.Rect(0, 0, game_handle.window_width, -10), False, "groundcomp", ground, True))


while game_handle.running:
    game_handle.begin()  # Tells the game handle that the game is at the beginning of a new frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False

    count = 0
    if count > 59:
        count = 0

    game_handle.asset_manager.load_image(Idle[count//4], "player")
    count += 1


    keys = pygame.key.get_pressed()

    player.controls(pygame.K_q, pygame.K_d, game_handle)

    if keys[pygame.K_SPACE]:
        if player.get_component_by_name("playerphysics").grounded:
            player.get_component_by_name("playerphysics").velocity.y -= 300



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
