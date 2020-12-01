class GameObjectManager(object):  # https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
    """A class to keep track of all active GameObjects

    ...

    Used as a singleton

    Attributes
    ----------
    game_objects : list
        A list of all created GameObjects

    Methods
    -------
    add_game_object(game_object=GameObject)
        Adds a GameObject to the list
    """

    __instance = None
    __current_game_object_id = 0  # A counter for unique ids - every time an object is created this int is increased
    game_objects = []  # A list of all created game placeholder

    def __new__(cls):  # Create a new instance and assign/copy the old values
        if GameObjectManager.__instance is None:
            GameObjectManager.__instance = object.__new__(cls)
            GameObjectManager.__instance.__current_game_object_id = cls.__current_game_object_id
            GameObjectManager.__instance.game_objects = cls.game_objects
        return GameObjectManager.__instance

    def add_game_object(self, game_object):
        """Adds a GameObject to the list - is called by each newly created GameObject

        Parameters
        ----------
        game_object : GameObject
            The GameObject which should be added to the list of all GameObjects

        Returns
        -------
        int
            The id which has beed created for the GameObject
        """

        self.game_objects.append(game_object)
        self.__current_game_object_id += 1
        return self.__current_game_object_id - 1

    def debug_total_objects_count(self):  # For debugging
        """Prints the current number of GameObjects

        Returns
        -------
        int
            The number of all currently initialized GameObjects
        """

        return len(self.game_objects)