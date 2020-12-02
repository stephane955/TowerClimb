import pygame

from pygeon.core.GameManager import GameHandle
from pygeon.core.misc.Camera import Camera
from pygeon.core.misc.GameObject import GameObject
from pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent, \
    PhysicsGameObjectComponent

game_handle = GameHandle("C:/Users/malte/Desktop/texture_missing.png")

# Tests
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/customImage1.png", "a_id")
game_handle.asset_manager.load_image("C:/Users/malte/Desktop/customImage2.png", "b_id")
a = GameObject(pygame.Vector2(0, 0), "a", True)
a.add_component(RendererGameObjectComponent("a_id", 0, (1, 1), "renderer", a, True))
b = GameObject(pygame.Vector2(150, 200), "b", True)
b.add_component(RendererGameObjectComponent("b_id", 1, (1, 1), "rendererb", b, True))
c = GameObject(pygame.Vector2(0, 150), "c", True)
c.add_component(RendererGameObjectComponent("b_id", 1, (1, 1), "rendererc", c, True))
a_dyn = True
a.add_component(CollisionGameObjectComponent(pygame.Rect(0, 0, 128, 128), a_dyn, "collider", a, True))
a.add_component(PhysicsGameObjectComponent(pygame.Rect(0, 127, 128, 2), a_dyn, "collider_grav", a, True))
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
# --- TESTS !!!
mode = True
prev_pressed = False
# ---

cam2 = Camera(pygame.Vector2(game_handle.window_width/2, 0), "cam2", True)

print(dir(a))

while game_handle.running:
    game_handle.begin()  # Tells the game handle that the game is at the beginning of a new frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_handle.running = False

    game_handle.physics_update()  # Update all physics (collisions)

    #game_handle.force_physics_update()

    game_handle.clear_screen()  # Clear the screen to display changes

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
