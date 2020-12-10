from os import *
from os.path import *

from pygeon.core.GameObjectSaveManager import GameObjectSaveManager, GameObjectManager, Camera, pygame
from pygeon.game.IngameObjects import Player


class Level:

    def __init__(self, level_name, level_directory_path):
        self.level_name = level_name
        self.content = LevelLoader(level_directory_path).get_level_content(level_name)

    def set(self):
        GameObjectManager().game_objects = self.content
        print("Loaded everything.")

        return Player("player_image", pygame.Vector2(400-int(33/2), 100), "Player", True)


class LevelLoader:

    def __init__(self, level_directory_path):
        self.save_manager = GameObjectSaveManager()
        self.__levels = [(level_directory_path + file) for file in listdir(level_directory_path)]
        self.__level_data = {basename(file).replace(".txt", ""): self.save_manager.load_return(file) for file in
                             self.__levels}

    def get_level_content(self, level_name):
        return self.__level_data[level_name]
