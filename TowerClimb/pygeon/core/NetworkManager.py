import requests
from pygeon.core.GameManager import GameHandle

# !--- NICHTS ÄNDERN CODE UNVOLLSTÄNDIG - RICHTIGE VERSION LOKAL IN ARBEIT ---!
class NetworkManager:

    def __init__(self, game_handle: GameHandle):
        self.game_handle = game_handle
        a = self.query("https://www.alphagoofy.de/python/test.php", {"arg": "tests"})
        print(a)

    def query(self, host, arguments: dict):
        q = requests.post(host, arguments)
        return q.text


NetworkManager(None)
