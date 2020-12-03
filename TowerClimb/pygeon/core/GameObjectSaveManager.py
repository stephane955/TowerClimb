import pickle
import re
from pygeon.core.GameManager import *
from pygeon.core.misc.GameObject import *


class GameObjectSaveManager:

    def load(self, path):
        file = open(path, "rb")

        data = pickle.load(file)

        GameObjectManager().game_objects = data

        file.close()

    def save(self, path):
        current_id = GameObjectManager().get_current_id()
        save_file = open(path, "wb")

        pickle.dump(GameObjectManager().game_objects, save_file)

        save_file.flush()
        save_file.close()