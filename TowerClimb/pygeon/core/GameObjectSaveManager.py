import pickle
import re
from pygeon.core.GameManager import *
from pygeon.core.misc.GameObject import *


class GameObjectSaveManager:

    def load(self):
        file = open("C:/Users/malte/Desktop/test_save.txt", "rb")

        for line in file.readlines():
            print(type(line))
            GameObjectManager().game_objects.append(pickle.loads(line))

        file.close()

    def save(self):
        current_id = GameObjectManager().get_current_id()

        print(current_id)

        all_objects_data = []

        for game_object in GameObjectManager().game_objects:
            all_objects_data.append(pickle.dumps(game_object))

        save_file = open("C:/Users/malte/Desktop/test_save.txt", "wb")

        for data in all_objects_data:
            save_file.write(data)
        save_file.flush()
        save_file.close()
