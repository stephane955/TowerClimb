import pygame

from TowerClimb.pygeon.core.misc.GameObject import GameObject


class Camera(GameObject):
    """A class used to represent a Camera, derives from GameObject

    The Camera is used to render other GameObjects relative to the Cameras position

    ...

    Attributes
    ----------
    position : pygame.Vector2
        The position of the camera represented as a vector (default [0, 0])
    name : str
        The name of the camera
    active : bool
        A boolean to control whether the camera is active or not (default true)
    Methods
    -------
    follow(game_object=GameObject, offset=(int, int)
        Follows the object with the given offset
    """

    def __init__(self, position: pygame.Vector2, name, active=True):
        super().__init__(position, name, active)

    def follow(self, game_object: GameObject, offset: (int, int)):
        """Follows the object with the given offset

        Parameters
        ----------
        game_object : GameObject
            The GameObject which the camera should follow
        offset : (int, int)
            The offset to the followed object
        """

        self.position.x = game_object.position.x - offset[0]
        self.position.y = game_object.position.y - offset[1]
