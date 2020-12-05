import pygame

from pygeon.core.GameManager import GameHandle
from pygeon.core.GameObjectSaveManager import GameObjectSaveManager
from pygeon.core.misc.Camera import Camera
from pygeon.core.misc.GameObject import GameObject
from pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent, \
    PhysicsGameObjectComponent, ImageAnimationGameObjectComponent
from pygeon.core.misc.GameObjectManager import GameObjectManager

game_handle = GameHandle("C:/Users/malte/Desktop/texture_missing.hero")

# Tests
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/customImage1.hero", "a_id")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/customImage2.hero", "b_id")

game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-00.hero", "c_0")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-01.hero", "c_1")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-02.hero", "c_2")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-03.hero", "c_3")
#---
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-2-00.hero", "d_0")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-2-01.hero", "d_1")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-2-02.hero", "d_2")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-idle-2-03.hero", "d_3")

game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-attack3-00.hero", "f_0")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-attack3-01.hero", "f_1")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-attack3-02.hero", "f_2")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-attack3-03.hero", "f_3")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-attack3-04.hero", "f_4")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-attack3-05.hero", "f_5")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-air-attack3-loop-00.hero", "f_6")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/Individual Sprites/adventurer-air-attack3-loop-01.hero", "f_7")

"""
a = GameObject(pygame.Vector2(0, 0), "a", True)
a.add_component(RendererGameObjectComponent("a_id", 0, (1, 1), "renderer", a, True))
b = GameObject(pygame.Vector2(150, 200), "b", True)
b.add_component(RendererGameObjectComponent("b_id", 1, (1, 1), "rendererb", b, True))
c = GameObject(pygame.Vector2(0, 150), "c", True)
c.add_component(RendererGameObjectComponent("b_id", 1, (1, 1), "rendererc", c, True))
a_dyn = True
a.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 128, 128), a_dyn, "collider", a, True))
a.add_component(PhysicsGameObjectComponent(pygame.Rect(0, 127, 128, 2), a_dyn, 128, "collider_grav", a, True))
#
c_dyn = True
c.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 1, 128), c_dyn, "left", c, True))
c.add_component(CollisionGameObjectComponent(pygame.Rect(128, 0, 1, 128), c_dyn, "right", c, True))
c.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 128, 1), c_dyn, "bottom", c, True))
c.add_component(CollisionGameObjectComponent(pygame.Rect(0, 128, 128, 1), c_dyn, "top", c, True))
#
d = GameObject(pygame.Vector2(0, 590), "d", True)
#game_handle.asset_manager.create_internal_image(128, 128, (134, 123, 184), "d_id")
#d.add_component(RendererGameObjectComponent("d_id", 0, (1, 1), "renderer", d, True))
d.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 800, 10), False, "coll", d, True))

c.add_child(b)
"""

# --- Auch TESTS !!!
save_mgr = GameObjectSaveManager()
#save_mgr.save()
save_mgr.load("C:/Users/malte/Desktop/test_save.txt")
a = GameObjectManager().get_object_by_name("a")
b = GameObjectManager().get_object_by_name("b")
c = GameObjectManager().get_object_by_name("c")
d = GameObjectManager().get_object_by_name("d")

e = GameObject(pygame.Vector2(500, 300), "e", True)
#e.add_component(RendererGameObjectComponent("b_id", 0, (1, 1), "renderer", e, True))
e.add_component(ImageAnimationGameObjectComponent(["c_0", "c_1", "c_2", "c_3"], 4, "c_0", 0, (1, 1), "renderer", e, True))
f = GameObject(pygame.Vector2(500, 500), "f", True)
f.add_component(ImageAnimationGameObjectComponent(["d_0", "d_1", "d_2", "d_3"], 4, "d_0", 0, (1, 1), "renderer", f, True))

g = GameObject(pygame.Vector2(500, 100), "g", True)
g.add_component(ImageAnimationGameObjectComponent(["f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7"], 4, "g_0", 0, (1, 1), "renderer", g, True))

# --- TESTS !!!
mode = True
prev_pressed = False
# ---

cam2 = Camera(pygame.Vector2(game_handle.window_width/2, 0), "cam2", True)

clock = pygame.time.Clock()

while game_handle.running:
    game_handle.begin()  # Tells the game handle that the game is at the beginning of a new frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False

    game_handle.physics_update()  # Update all physics (collisions)

    #game_handle.force_physics_update()

    game_handle.clear_screen()  # Clear the screen to display changes

    game_handle.animations_tick()

    if not mode:  # TESTS !!! (Nur die If)
        game_handle.render()  # Render all objects

    # -------------------
    # TESTS !!!

    if mode:
        game_handle.render_split_screen(cam2)

    game_handle.debug_draw_collider_outlines()

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        game_handle.camera.translate_movement(0, -150 * game_handle.delta_time)
    if key[pygame.K_s]:
        game_handle.camera.translate_movement(0, 150 * game_handle.delta_time)
    if key[pygame.K_a]:
        game_handle.camera.translate_movement(-150 * game_handle.delta_time, 0)
    if key[pygame.K_d]:
        game_handle.camera.translate_movement(150 * game_handle.delta_time, 0)

    if key[pygame.K_DOWN]:
        if c.get_component_by_name("top").has_no_collisions():
            c.translate_movement(0, 150 * game_handle.delta_time)
    if key[pygame.K_UP]:
        if c.get_component_by_name("bottom").has_no_collisions():
            c.translate_movement(0, -150 * game_handle.delta_time)
    if key[pygame.K_RIGHT]:
        if c.get_component_by_name("right").has_no_collisions():
            c.translate_movement(150 * game_handle.delta_time, 0)
    if key[pygame.K_LEFT]:
        if c.get_component_by_name("left").has_no_collisions():
            c.translate_movement(-150 * game_handle.delta_time, 0)

    if key[pygame.K_t]:
        cam2.translate_movement(0, -150 * game_handle.delta_time)
    if key[pygame.K_g]:
        cam2.translate_movement(0, 150 * game_handle.delta_time)
    if key[pygame.K_f]:
        cam2.translate_movement(-150 * game_handle.delta_time, 0)
    if key[pygame.K_h]:
        cam2.translate_movement(150 * game_handle.delta_time, 0)

    if key[pygame.K_i]:
        a.translate_movement(0, -300 * game_handle.delta_time)
    if key[pygame.K_k]:
        a.translate_movement(0, 300 * game_handle.delta_time)
    if key[pygame.K_j]:
        a.translate_movement(-300 * game_handle.delta_time, 0)
    if key[pygame.K_l]:
        a.translate_movement(300 * game_handle.delta_time, 0)

    if key[pygame.K_SPACE]:
        if a.get_component(PhysicsGameObjectComponent)[0].grounded:
            a.get_component(PhysicsGameObjectComponent)[0].velocity.y = -1500

    if key[pygame.K_m] and not prev_pressed:
        mode = not mode

        prev_pressed = True
    if not key[pygame.K_m]:
        prev_pressed = False

    # ----------------------------

    game_handle.update_screen()

    game_handle.end()  # Finishes everything for the current frame

pygame.quit()  # Exit the program
