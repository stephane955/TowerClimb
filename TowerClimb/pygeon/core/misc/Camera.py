import pygame

from pygeon.core.misc.GameObject import GameObject


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
    """

    def __init__(self, position: pygame.Vector2, name, active=True):
        super().__init__(position, name, active)
