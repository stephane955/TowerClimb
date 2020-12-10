import asyncio
import threading

import pygame

from pygeon.core.AssetManager import AssetManager
from pygeon.core.misc.Camera import Camera
from pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent, CollisionGameObjectComponent, \
    PhysicsGameObjectComponent, ImageAnimationGameObjectComponent
from pygeon.core.misc.GameObjectManager import GameObjectManager
from pygeon.core.networking.NetworkManager import MultiplayerManager


class GameHandle:
    """A class which manages important tasks for the game in the background

    ...

    Attributes
    ----------
    delta_time : float
        The time passed since the last frame
    missing_image_file_path : str
        The path to the image which replaces missing images
    window_width : int
        The width of the game window (default 800)
    window_height : int
        The height of the game window (default 600)
    running : bool
        A boolean to control the main loop of the game
    RENDER_LAYERS : dict
        A dictionary of layers which are used for rendering
    clear_color : (int, int, int)
        The color which is used to clear the screen
    physics_update_frequency_ticks : int
        The frequency of which all GameObjects are checked for physical interactions
    gravity : float
        The value which is used for gravity
    camera : Camera
        The default Camera for the game
    asset_manager : AssetManager
        The AssetManager of the current game
    screen : pygame.display
        A reference to a pygame module to control the screen

    Methods
    -------
    render()
        Renders all drawable GameObjects considering their layers
    debug_render_layer(layer=int)
        Only renders the specified layer
    debug_draw_collider_outlines()
        Renders the outlines of all GameObjects with hit boxes
    physics_update()
        Updates physical things for all relevant GameObjects
    __overlapping_split_screen(x=float, width=int, side=int, camera=Camera):
        Checks if a GameObject is overlapping into another side of the split screen
    __render_intern_split_screen(side=int, camera=Camera)
        Renders one side of the split screen
    __clear_screen_split(side=int)
        Clears a specific side of the screen
    render_split_screen(camera_other=Camera):
        Runs all necessary methods to render in split screen
    clear_screen()
        Clears the screen with the specified clear_color
    update_screen()
        Updates the screen
    begin()
        Tells the GameHandle to begin a new frame
    end()
        Tells the GameHandle that the current frame is over
    """

    delta_time: float = 0.0
    __last_frame_ticks: float = 0.0
    __last_physics_update: float = 0.0
    __last_animation_update: float = 0.0

    def __init__(self, missing_image_file_path, window_width: int = 800, window_height: int = 600):
        """
        Parameters
        ----------
        missing_image_file_path : str
            The path to the image which replaces missing images
        window_width : int
            The width of the game window (default 800)
        window_height : int
            The height of the game window (default 600)
        """

        self.missing_image_file_path = missing_image_file_path
        self.window_width = window_width
        self.window_height = window_height
        self.running = True
        self.RENDER_LAYERS = {0: 'Default Layer 1', 1: 'Default Layer 2', 2: 'Default Layer 3', 3: 'Default Layer 4'}
        self.clear_color = (255, 255, 255)
        self.physics_update_frequency_ticks = 0  # lower value needs more performance #TODO test for good value
        self.gravity = 98.1 ** 1.75  # 9.81 is too low
        # This is the fastest speed an animation can have
        self.animation_speed = 60  # All animation speeds depend on that, they can't be faster than this, only slower
        # Create a camera
        self.camera = Camera(pygame.Vector2(0, 0), "Camera", True)
        # Create the asset manager
        self.asset_manager = AssetManager(pygame.image.load(missing_image_file_path))
        #
        self.multiplayer_manager = MultiplayerManager()
        # Init Pygame
        pygame.init()
        # Create the screen
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    def render(self):
        """Renders all drawable GameObjects considering their layers

        Will iterate through all GameObjects which are stored in the GameObjectManager and draws them
        if they have a RendererGameObjectComponent attached to them
        """

        current_layer = 0  # The layer which is currently drawn
        max_layer = len(self.RENDER_LAYERS)  # The maximum defined layer

        for layer in range(0, max_layer):  # Loop through all layers
            for game_object in GameObjectManager().game_objects:  # Loop through all objects
                if not game_object.active:  # Only active objects should be drawn
                    continue
                if len(game_object.get_component(RendererGameObjectComponent)) <= 0:  # Object needs component
                    continue

                render_components = game_object.get_component(RendererGameObjectComponent)  # All render components

                for r_component in render_components:
                    if r_component.render_layer == current_layer:  # Only draw if the layer is correct
                        # Draw everything relative to the current camera position
                        self.screen.blit(self.asset_manager.get_image(r_component.image_asset_id),
                                         (game_object.get_x() - self.camera.get_x(),
                                          game_object.get_y() - self.camera.get_y()))

            current_layer += 1  # Increase the layer which is currently drawn

    def debug_render_layer(self, layer):
        """Only renders the specified layer

        Parameters
        ----------
        layer : int
            The layer which should be rendered
        """

        for game_object in GameObjectManager().game_objects:  # All comments from 'render' apply
            if not game_object.active:  # Only active objects should be drawn
                continue
            if len(game_object.get_component(RendererGameObjectComponent)) <= 0:
                continue

            render_components = game_object.get_component(RendererGameObjectComponent)

            for r_component in render_components:
                if r_component.render_layer == layer:
                    self.screen.blit(self.asset_manager.get_image(r_component.image_asset_id),
                                     game_object.position.x - self.camera.get_x(),
                                     game_object.position.y - self.camera.get_y())

    def debug_draw_collider_outlines(self):
        """Renders the outlines of all GameObjects with hit boxes
        """

        for game_object in GameObjectManager().game_objects:  # All comments from 'render' apply
            if not game_object.active:  # Only active objects should be drawn
                continue
            if len(game_object.get_component(CollisionGameObjectComponent)) <= 0:
                continue

            render_components = game_object.get_component(CollisionGameObjectComponent)

            for r_component in render_components:
                r_component.debug_draw_outline(self.camera, (255, 255, 0), 2)

    def animations_tick(self):
        if pygame.time.get_ticks() < (self.__last_animation_update + self.animation_speed):
            return

        self.__last_animation_update = pygame.time.get_ticks()

        for game_object in GameObjectManager().game_objects:
            if game_object.has_component_of_type(ImageAnimationGameObjectComponent):
                if not game_object.get_component(ImageAnimationGameObjectComponent)[0].active:
                    continue
                game_object.get_component(ImageAnimationGameObjectComponent)[0].step_animation()

    def physics_update(self):
        """Updates physical things for all relevant GameObjects
        """

        # If x ticks have passed, the method will be executed
        if pygame.time.get_ticks() >= (self.__last_physics_update + self.physics_update_frequency_ticks):
            self.__last_physics_update = pygame.time.get_ticks()

            dynamic_collision_objects = []
            static_collision_objects = []

            for game_object in GameObjectManager().game_objects:  # Loop through all game objects
                if not game_object.active:
                    continue
                if len(game_object.get_component(CollisionGameObjectComponent)) <= 0:  # Collision needs component
                    continue

                # Tell the GameObjects that they have to recalculate their physics
                # because of the newly calculated collisions
                if not len(game_object.get_component(PhysicsGameObjectComponent)) <= 0:
                    game_object.get_component(PhysicsGameObjectComponent)[0].recalculate = True

                # A GameObject can't be dynamic and static at the same time, so only the first element has to be checked
                if game_object.get_component(CollisionGameObjectComponent)[0].dynamic:
                    dynamic_collision_objects.append(game_object)  # Add the game object to the list
                else:
                    static_collision_objects.append(game_object)

            # Only dynamic GameObjects need to be upated
            for game_object in dynamic_collision_objects:  # Reset all collision data and update position
                for physics_component in game_object.get_component(CollisionGameObjectComponent):
                    physics_component.collisions = []
                    physics_component.update_position()

            # Check collisions: dynamic with static
            for game_object in dynamic_collision_objects:
                for other_game_object in static_collision_objects:
                    if game_object == other_game_object:  # No self collisions, but should not be possible anyway
                        continue

                    # Only check for dynamic objects if they collide with any other object
                    for phy_cmp in game_object.get_component(CollisionGameObjectComponent):
                        # All static objects are checked by the dynamic object
                        for o_phy_cmp in other_game_object.get_component(CollisionGameObjectComponent):
                            if phy_cmp.collider.colliderect(o_phy_cmp.collider):  # Colliders collide?
                                # Only the dynamic object needs to register the collision
                                if o_phy_cmp not in phy_cmp.collisions:
                                    phy_cmp.collisions.append(o_phy_cmp)  # Add active collision

            # Check collisions: dynamic with dynamic
            for game_object in dynamic_collision_objects:
                for other_game_object in dynamic_collision_objects:
                    if game_object == other_game_object:  # No self collisions
                        continue

                    for phy_cmp in game_object.get_component(CollisionGameObjectComponent):
                        for o_phy_cmp in other_game_object.get_component(CollisionGameObjectComponent):
                            if phy_cmp.collider.colliderect(o_phy_cmp.collider):  # Colliders collide?
                                if o_phy_cmp not in phy_cmp.collisions:
                                    phy_cmp.collisions.append(o_phy_cmp)  # Add active collision

        # Update all GameObjects regarding physics like gravity
        # Will execute every frame not only x ticks
        for game_object in GameObjectManager().game_objects:
            if not game_object.active:  # Only active objects should be drawn
                continue
            if len(game_object.get_component(PhysicsGameObjectComponent)) <= 0:
                continue
            # Update the GameObject
            game_object.get_component(PhysicsGameObjectComponent)[0].perform_physic(self)

    def __overlapping_split_screen(self, x, width, side, camera):
        """Checks if a GameObject is overlapping into another side of the split screen

        Parameters
        ----------
        x : float
            The x position
        width : int
            The width of the GameObject
        side : int
            The side for which the method should check
        camera : Camera
            The current camera which is used for the split screen

        Returns
        -------
        bool
            Whether the GameObject is overlapping the split screen or not
        """

        middle_line = int(camera.get_x() + self.window_width / 2)
        if side == 0:
            if width + x > middle_line:
                return True
        else:
            if x < middle_line:
                return True
        return False

    def __render_intern_split_screen(self, side: int, camera: Camera):
        """Renders one side of the split screen

        Parameters
        ----------
        side : int
            The side which should be rendered
        camera : Camera
            The camera which should be used for this render call
        """

        pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), (self.window_width / 2 - 1, 0),
                         (self.window_width / 2 - 1, self.window_height), 2)

        # Left
        if side == 0:
            current_layer = 0
            max_layer = len(self.RENDER_LAYERS)

            for layer in range(0, max_layer):
                for game_object in GameObjectManager().game_objects:
                    if not game_object.active:
                        continue
                    if len(game_object.get_component(RendererGameObjectComponent)) <= 0:
                        continue

                    render_components = game_object.get_component(RendererGameObjectComponent)

                    for r_component in render_components:
                        if r_component.render_layer == current_layer:
                            # ---
                            image_width = self.asset_manager.get_image(r_component.image_asset_id).get_width()
                            image_height = self.asset_manager.get_image(r_component.image_asset_id).get_height()
                            middle_line = int(camera.get_x() + self.window_width / 2)
                            image_orig = self.asset_manager.get_image(r_component.image_asset_id)
                            if self.__overlapping_split_screen(game_object.get_x(), image_width, 0, camera):
                                if image_width - (
                                        image_width - middle_line) - game_object.get_x() <= 0:  # Nichts mehr auf sichtbarer Seite übrig
                                    continue
                                image_new = pygame.Surface(
                                    (image_width - (image_width - middle_line) - game_object.get_x(), image_height))

                                for x in range(image_new.get_width()):
                                    for y in range(image_height):
                                        image_new.set_at((x, y), image_orig.get_at((x, y)))

                                self.screen.blit(image_new,
                                                 (game_object.get_x() - camera.get_x(),
                                                  game_object.get_y() - camera.get_y()))

                            else:
                                self.screen.blit(self.asset_manager.get_image(r_component.image_asset_id),
                                                 (game_object.get_x() - camera.get_x(),
                                                  game_object.get_y() - camera.get_y()))
                            # ---

                current_layer += 1  # Increase the layer which is currently drawn
        else:  # Right
            current_layer = 0
            max_layer = len(self.RENDER_LAYERS)

            for layer in range(0, max_layer):
                for game_object in GameObjectManager().game_objects:
                    if not game_object.active:
                        continue
                    if len(game_object.get_component(RendererGameObjectComponent)) <= 0:
                        continue

                    render_components = game_object.get_component(RendererGameObjectComponent)

                    for r_component in render_components:
                        if r_component.render_layer == current_layer:
                            self.screen.blit(self.asset_manager.get_image(r_component.image_asset_id),
                                             (
                                                 game_object.get_x() + int(
                                                     self.window_width / 2) - camera.get_x(),
                                                 game_object.get_y() - camera.get_y()))
                current_layer += 1

    def __clear_screen_split(self, side):
        """Clears a specific side of the screen
        """

        surf = pygame.Surface((self.window_width / 2, self.window_height))
        surf.fill(self.clear_color)
        if side == 0:
            self.screen.blit(surf, (0, 0))
        else:
            self.screen.blit(surf, (self.window_width / 2, 0))

    def render_split_screen(self, camera_other=None):
        """Runs all necessary methods to render in split screen
        """

        self.__render_intern_split_screen(1, self.camera if camera_other is None else camera_other)
        self.__clear_screen_split(0)
        self.__render_intern_split_screen(0, self.camera)

    def clear_screen(self):
        """Clears the screen with the clear_color
        """

        self.screen.fill(self.clear_color)  # Clear the whole screen with this color to display changes after rendering

    def update_screen(self):
        """Updates the screen
        """

        pygame.display.update()

    def begin(self):
        """Tells the GameHandle that a new frame has started

        Used to calculate the delta time
        """

        self.__last_frame_ticks = pygame.time.get_ticks()

    def end(self):
        """Tells the GameHandle that the current frame has ended

        Used to calculate the delta time
        """

        self.delta_time = (pygame.time.get_ticks() - self.__last_frame_ticks) / 1000
