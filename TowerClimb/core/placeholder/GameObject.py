import pygame
import math
from TowerClimb.core.placeholder.GameObjectComponents import *
from TowerClimb.core.placeholder.GameObjectComponents import GameObjectComponent
from TowerClimb.core.placeholder.GameObjectManager import *
vec = pygame.Vector2

class GameObject:
    """
    The base class for all objects in the game

    ...

    Attributes
    ----------
    position : pygame.Vector2
        The position of the GameObject represented as a vector (default [0, 0])
    name : str
        The name of the camera
    active : bool
        A boolean to control whether the GameObject is active or not (default is true)
    __component_container: list
        A list for all components which have been added to the GameObject
    __id: int
        A unique id for the GameObject given by the GameObjectManager

    Methods
    -------
    add_component(component_type=GameObjectComponent)
        Adds a component of the given type to the GameObject
    get_component(component=GameObjectComponent)
        Try to get a component from the GameObject of the specified type
    get_x()
        Returns the floored X position
    get_y()
        Returns the floored Y position
    translate_movement(x=float, y=float)
        Moves the GameObjects position by the specified x and y
    """

    def __init__(self, position: pygame.Vector2, name, active=True):
        """
        Parameters
        ----------
        position : pygame.Vector2
            The position of the GameObject represented as a vector (default [0,0])
        name : str
            The name of the GameObject
        active : bool
            A boolean to control wheter the GameObject is active or not (default is true)
        """

        self.position = position
        self.name = name
        self.active = active

        self.__component_container = []

        self.__id = GameObjectManager().add_game_object(self)

    def add_component(self, component: GameObjectComponent):
        """Adds a component of the given type to the GameObject

        Parameters
        ----------
        component : GameObjectComponent
            The component to add to the GameObject
        """

        self.__component_container.append(component)

    def get_component(self, component_type):
        """Try to get a component from the GameObject of the specified type

        Will return an empty list if no component is found

        Parameters
        ----------
        component_type : GameObjectComponent
            The component type which should be returned

        Returns
        -------
        list
            A list of all components which are of the required type
        """

        components = []
        for component in self.__component_container:  # Iterate through all components
            if isinstance(component, component_type):  # If the component is of the required type add it to the list
                components.append(component)
        return components  # Return the list

    def get_x(self):
        """Returns the floored X position

        Returns
        -------
        int
            The floored X position of the GameObject
        """

        return math.floor(self.position.x)

    def get_y(self):
        """Returns the floored Y position

                Returns
                -------
                int
                    The floored Y position of the GameObject
                """

        return math.floor(self.position.y)

    def translate_movement(self, x: float, y: float):
        """Moves the GameObjects position by the specified x and y

        """

        self.position.x += x
        self.position.y += y