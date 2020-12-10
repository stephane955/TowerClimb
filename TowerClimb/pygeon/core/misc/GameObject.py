import math

import pygame

from pygeon.core.misc.GameObjectComponents import GameObjectComponent, RendererGameObjectComponent
from pygeon.core.misc.GameObjectManager import GameObjectManager


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
    parent: GameObject
        A reference to the parent GameObject
    __children : list
        A list of the names of child GameObjects
    __component_container: list
        A list for all components which have been added to the GameObject
    __id : int
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
    add_child(game_object=GameObject)
        Adds a child to the GameObject
    has_component_of_type(component_type=GameObjectComponent)
        Returns whether the GameObject has a component of the given type or not
    get_component_by_name(name=str)
        Will try to get a component by its name
    """

    # All attribute names, used for serialization by reflection
    __attributes = ["position",  "name", "active", "parent", "__children", "__component_container", "__id"]

    def __init__(self, position: pygame.Vector2, name, active=True):
        """
        Parameters
        ----------
        position : pygame.Vector2
            The position of the GameObject represented as a vector (default [0,0])
        name : str
            The name of the GameObject
        active : bool
            A boolean to control whether the GameObject is active or not (default is true)
        """

        self.position = position
        self.name = name
        self.active = active
        self.parent = ""

        self.__children = []

        self.__component_container = []

        self.__id = GameObjectManager().add_game_object(self)

    def add_child(self, game_object):
        """Adds a child to the GameObject

        Parameters
        ----------
        game_object : GameObject
            The GameObject which will be added as a child
        """

        self.__children.append(game_object.name)
        game_object.parent = self.name

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

    def get_component_by_name(self, name):
        """Try to get a component from the GameObject with the given name

                Will return None if there is no matched Component

                Parameters
                ----------
                name : str
                    The name of the component which should be returned

                Returns
                -------
                GameObjectComponent
                    The Component with the specified names
                """

        for component in self.__component_container:  # Iterate through all components
            if component.name == name:  # If the component has the required name
                return component
        return None

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

        # All child objects need to be moved as well
        # TODO Use delta time for child movement
        for child in self.__children:
            GameObjectManager().get_object_by_name(child).translate_movement(x, y)

    def has_component_of_type(self, component_type):
        """Checks of the GameObject has a component of the given type

        Parameters
        ----------
        component_type : GameObjectComponent
            The type which is looked for
        Returns
        -------
        Whether the GameObject has a component of that type or not
        """

        for component in self.__component_container:  # Iterate through all components
            if isinstance(component, component_type):  # Check for the type
                return True
        return False
