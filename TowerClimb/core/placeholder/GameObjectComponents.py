import pygame
from TowerClimb.core.GameManager import *


class GameObjectComponent:
    """The base class for all components which can be added to GameObjects

    ...

    Attributes
    ----------
    name : str
        The name of the component
    game_object : GameObject
        The GameObject which the component is added to
    active : bool
        Whether the component is active or not (default is true)
    """

    def __init__(self, name, game_object, active=True):
        """
        Parameters
        ----------
        name : str
            The name of the component
        game_object : GameObject
            The GameObject which the component is added to
        active : bool
            Whether the component is active or not (default is true)
        """

        self.name = name
        self.game_object = game_object
        self.active = active


class RendererGameObjectComponent(GameObjectComponent):
    """A component which is used to draw images onto the screen

    ...

    Attributes
    ----------
    image_asset_id : str
        The id of the associated image with the component
    render_layer : int
        The layer on which the image should be drawn
    scale : (int, int)
        The scale of the image
    name : str
        The name of the component
    game_object : GameObject
        The GameObject which the component is added to
    active : bool
        Whether the component is active or not (default is true)
    """

    def __init__(self, image_asset_id: str, render_layer: int, scale: (int, int), name, game_object, active=True):
        """
        Parameters
        ----------
        image_asset_id : str
            The id of the associated image with the component
        render_layer : int
            The layer on which the image should be drawn
        scale : (int, int)
            The scale of the image
        name : str
            The name of the component
        game_object : GameObject
            The GameObject which the component is added to
        active : bool
            Whether the component is active or not (default is true)
        """

        super().__init__(name, game_object, active)

        self.image_asset_id = image_asset_id
        self.render_layer = render_layer
        self.scale = scale


class CollisionGameObjectComponent(GameObjectComponent):
    """A component for detecting collisions

    ...

    Attributes
    ----------
    collider : pygame.Rect
        The rectangular hit box of the component
    dynamic : bool
        Set to true if the object will not change its position
        If an GameObject has dynamic and non dynamic colliders the collisions won't work properly!
    name : str
        The name of the component
    game_object : GameObject
            The GameObject which the component is added to
    active : bool
        Whether the component is active or not (default is true)

    Methods
    -------
    has_no_collisions()
        Checks if the whether the component has active collisions
    all_components_no_collision()
        Checks if all components on game_object have no active collisions
    update_position()
        Updates the position of the rect according to the GameObjects position
    debug_draw_outlines()
        Draws the outlines of the hit box on the screen
    """

    def __init__(self, collider: pygame.Rect, dynamic, name, game_object, active=True):
        """
        Parameters
        ----------
        collider : pygame.Rect
           The rectangular hit box of the component
        dynamic : bool
            Set to true if the object will not change its position
        name : str
            The name of the component
        game_object : GameObject
            The GameObject which the component is added to
        active : bool
            Whether the component is active or not (default is true)
        """

        super().__init__(name, game_object, active)

        self.collider = collider  # The objects collider

        self.dynamic = dynamic

        # Save the original offset to position the collider correctly
        self.offset_x = self.collider.x
        self.offset_y = self.collider.y
        # Update the position
        self.collider.x += self.game_object.position.x
        self.collider.y += self.game_object.position.y

        self.collisions = []  # All active collisions

    def has_no_collisions(self):
        """Checks if there are any active collisions
        """

        return len(self.collisions) <= 0

    def all_components_no_collision(self):
        """Checks if there are any active collisions for all components on the GameObject

        Returns
        -------
        bool
            Whether any component on this components GameObject has active collisions or not
        """

        # Iterate through all components of this type
        for physics_component in self.game_object.get_component(CollisionGameObjectComponent):
            if not physics_component.has_no_collisions():
                return False
        return True

    def update_position(self):
        """Updates the position of the component according to the GameObject
        """

        self.collider.x = self.game_object.position.x + self.offset_x
        self.collider.y = self.game_object.position.y + self.offset_y

    def debug_draw_outline(self, camera, color: (int, int, int), line_thickness: int):
        """Draws the outlines of the rect

        For debugging only

        Parameters
        ----------
        camera : Camera
            The active camera, used to calculate the relative position
        color : (int, int, int)
            The color of the outlines
        line_thickness : int
            The thickness of the outlines
        """

        pygame.draw.polygon(pygame.display.get_surface(), color,
                            ((self.collider.x - camera.get_x(), self.collider.y - camera.get_y()),
                             (self.collider.x - camera.get_x() + self.collider.width,
                              self.collider.y - camera.get_y()),
                             (
                                 self.collider.x - camera.get_x() + self.collider.width,
                                 self.collider.y - camera.get_y() + self.collider.height),
                             (self.collider.x - camera.get_x(),
                              self.collider.y - camera.get_y() + self.collider.height)), line_thickness)


class PhysicsGameObjectComponent(CollisionGameObjectComponent):
    """A component for physical behaviour

        Needs at least one hit box to detect whether the GameObject is grounded or not
        Has to be dynamic!

        ...

        Attributes
        ----------
        grounded : bool
            The boolean to control if gravity needs to be applied to the GameObject
        collider : pygame.Rect
            The rectangular hit box of the component
        dynamic : bool
            Set to true if the object will not change its position
            If an GameObject has dynamic and non dynamic colliders the collisions won't work properly!
        name : str
            The name of the component
        game_object : GameObject
                The GameObject which the component is added to
        active : bool
            Whether the component is active or not (default is true)
        velocity: pygame.Vector2
            The current velocity of the GameObject

        Methods
        -------
        has_no_collisions()
            Checks if the whether the component has active collisions
        all_components_no_collision()
            Checks if all components on game_object have no active collisions
        update_position()
            Updates the position of the rect according to the GameObjects position
        debug_draw_outlines()
            Draws the outlines of the hit box on the screen
        perform_physic()
            Performs all the necessary tasks to simulate the required physical effects
        """

    def __init__(self, collider: pygame.Rect, dynamic, name, game_object, active=True):
        """
        Parameters
        ----------
        collider : pygame.Rect
           The rectangular hit box of the component
        dynamic : bool
            Set to true if the object will not change its position
        name : str
            The name of the component
        game_object : GameObject
            The GameObject which the component is added to
        active : bool
            Whether the component is active or not (default is true)
        """

        super().__init__(collider, dynamic, name, game_object, active)

        self.grounded = False
        self.recalculate = False
        self.velocity = pygame.Vector2(0, 0)

    def perform_physic(self, game_handle):
        """Performs all the necessary tasks to simulate the required physical effects
        """

        if not self.grounded:
            self.velocity.y += game_handle.gravity
            # Apply the velocity
            self.game_object.translate_movement(self.velocity.x * game_handle.delta_time,
                                                self.velocity.y * game_handle.delta_time)

        if self.recalculate:
            if len(self.collisions) <= 0:
                self.grounded = False
                return

            valid_collision = False
            for coll in self.collisions:
                if coll.dynamic:
                    valid_collision = True
                    # Only reset the y of the velocity if the object has a "falling" velocity, otherwise jumping would
                    # be removed too
                    self.velocity = pygame.Vector2(self.velocity.x, 0 if self.velocity.y >= 0 else self.velocity.y)
                    break
            self.grounded = valid_collision


