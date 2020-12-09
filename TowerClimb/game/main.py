from TowerClimb.game.Player import Player
from TowerClimb.pygeon.core.GameManager import GameHandle
from TowerClimb.pygeon.core.misc.GameObject import GameObject
from TowerClimb.pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent, \
    PhysicsGameObjectComponent, ImageAnimationGameObjectComponent
from TowerClimb.game.Settings import *
import keyboard

# storing paths for my character images
path = "C:/Users/tegui/OneDrive/Dokumente/GitHub/TowerClimb/TowerClimb/game/adventurer_new_sizes/"
path2 = "C:/Users/tegui/OneDrive/Dokumente/GitHub/TowerClimb/TowerClimb/game/adventurer_new_sizes/run_left/"
path3 = "C:/Users/tegui/OneDrive/Dokumente/GitHub/TowerClimb/TowerClimb/game/adventurer_new_sizes/idle_left/"

idle_right = [path + "Idle__000.png", path + "Idle__001.png", path + "Idle__002.png", path + "Idle__003.png",
              path + "Idle__004.png", path + "Idle__005.png", path + "Idle__006.png",
              path + "Idle__007.png", path + "Idle__008.png", path + "idle__009.png"]
idle_left = [path3 + "Idle__000.png", path3 + "Idle__001.png", path3 + "Idle__002.png", path3 + "Idle__003.png",
             path3 + "Idle__004.png", path3 + "Idle__005.png", path3 + "Idle__006.png",
             path3 + "Idle__007.png", path3 + "Idle__008.png", path3 + "idle__009.png"]
jump = [path + "Jump__000.png", path + "Jump__001.png", path + "Jump__002.png", path + "Jump__003.png",
        path + "Jump__004.png", path + "Jump__005.png", path + "Jump__006.png",
        path + "Jump__007.png", path + "Jump__008.png", path + "Jump__009.png"]
run_right = [path + "run__000.png", path + "run__001.png", path + "run__002.png", path + "run__003.png",
             path + "run__004.png", path + "run__005.png", path + "run__006.png",
             path + "run__007.png", path + "run__008.png", path + "run__009.png"]
run_left = [path2 + "Run__000.png", path2 + "Run__001.png", path2 + "Run__002.png", path2 + "run__003.png",
            path2 + "Run__004.png", path2 + "Run__005.png", path2 + "Run__006.png",
            path2 + "Run__007.png", path2 + "Run__008.png", path2 + "Run__009.png"]

# create an instance of the game manager
game_handle = GameHandle("C:/Users/tegui/OneDrive/Python/earth.jpg")

# set abitrary ids for the loaded images
asset_id = "i"
asset_id_left = "l"
asset_id_right = "r"

# list for storing the paths and image's ids
path_ids_idle_right = []
path_ids_left = []
path_ids_right = []
path_ids_idle_left = []
dict_all_paths = {}

# different images from the player will are been loaded
for path in idle_right:
    game_handle.asset_manager.load_image(path, asset_id)
    path_ids_idle_right.append(asset_id)
    asset_id += "i"

for path in run_right:
    game_handle.asset_manager.load_image(path, asset_id)
    path_ids_right.append(asset_id)
    asset_id += "a"

for path in run_left:
    game_handle.asset_manager.load_image(path, asset_id)
    path_ids_left.append(asset_id)
    asset_id += "x"

for path in idle_left:
    game_handle.asset_manager.load_image(path, asset_id)
    path_ids_idle_left.append(asset_id)
    asset_id += "p"

# loaded images are been stored in a dictionary. It will be needed to render animation.
dict_all_paths["idle_right"] = path_ids_idle_right
dict_all_paths["run_right"] = path_ids_right
dict_all_paths["run_left"] = path_ids_left
dict_all_paths["idle_left"] = path_ids_idle_left

# Platforms are been drawn
for plat in Platforms:
    game_handle.asset_manager.create_internal_image(100, 30, GREEN, plat[1])
    platf = GameObject(*plat)
    platf.add_component(RendererGameObjectComponent(plat[1], 1, (0, 0), "platforms", plat, True))
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 0, 100, -5), False, plat[1] + "t", platf, True))  # top
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 30, 100, 1), False, plat[1] + "b", platf, True))  # bottom
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 30), False, plat[1] + "l", platf, True))  # left
    platf.add_component(
        CollisionGameObjectComponent(pygame.Rect(100, 0, 1, 30), False, plat[1] + "r", platf, True))  # right

# Player and components

player = Player(pygame.Vector2(game_handle.window_width / 2 - 50, game_handle.window_height / 2 - 100), "player", True)
player.add_component(
    ImageAnimationGameObjectComponent(dict_all_paths, "idle_right", 1, "player", 1, (1, 1), "anim_idle", player, True))
player.add_component(
    CollisionGameObjectComponent(pygame.Rect(-10, -10, 60, -10), True, "player_t", player, True))  # top
player.add_component(CollisionGameObjectComponent(pygame.Rect(0, 100, 50, 1), True, "player_b", player, True))  # bottom
player.add_component(
    CollisionGameObjectComponent(pygame.Rect(-10, -20, 12, 120), True, "player_l", player, True))  # left
player.add_component(
    CollisionGameObjectComponent(pygame.Rect(40, -20, 12, 120), True, "player_r", player, True))  # right

# player physics components
player.add_component(PhysicsGameObjectComponent(pygame.Rect(-12, 100, 62, 1), True, 80, "player_physics_bottom", player,
                                                True))  # component for gravity
player.add_component(
    PhysicsGameObjectComponent(pygame.Rect(-10, -10, 60, -10), True, 80, "player_physics_top", player, True))  # top
player.add_component(
    PhysicsGameObjectComponent(pygame.Rect(40, -20, 12, 115), True, 80, "player_physics_right", player, True))  # right
player.add_component(
    PhysicsGameObjectComponent(pygame.Rect(-14, -20, 15, 115), True, 80, "player_physics_left", player, True))  # left


# Ground and components
game_handle.asset_manager.create_internal_image(game_handle.window_width, 30, GREEN, "ground")
ground = GameObject(vec(0, game_handle.window_height - 30), "ground", True)
ground.add_component(RendererGameObjectComponent("ground", 1, (0, 0), "hero", ground, True))
ground.add_component(
    CollisionGameObjectComponent(pygame.Rect(0, 0, game_handle.window_width, -5), False, "groundcomp", ground, True))

while game_handle.running:
    game_handle.begin()  # Tells the game handle that the game is at the beginning of a new frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False

    keys = pygame.key.get_pressed()

    player.controls(pygame.K_q, pygame.K_d, game_handle)

    # change camera position
    if player.position.y < 0:
        game_handle.camera.position.y = player.position.y - 80
    else:
        game_handle.camera.position = pygame.Vector2(0, 0)

    if keys[pygame.K_SPACE]:
        if player.get_component_by_name("player_physics_bottom").grounded:
            player.get_component_by_name("player_physics_bottom").velocity.y -= 300

    # check if player collides with anything on the top
    if not player.get_component_by_name("player_physics_top").has_no_collisions():
        player.get_component_by_name("player_physics_bottom").velocity.y = 120

    game_handle.animations_tick()

    game_handle.physics_update()  # Update all physics (collisions)

    game_handle.clear_screen()  # Clear the screen to display changes

    game_handle.render()  # Render all placeholder

    # Debug
    # if draw_debug:
    # game_handle.debug_draw_collider_outlines()

    game_handle.update_screen()

    game_handle.end()  # Finishes everything for the current frame

pygame.quit()  # Exit the program
