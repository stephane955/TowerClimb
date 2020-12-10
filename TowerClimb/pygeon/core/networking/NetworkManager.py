# https://docs.python.org/3/howto/sockets.html
import json
import select
import pygame
import requests
import socket
import uuid

from enum import Enum

from pygeon.core.data.SerializationHelper import Serializer
from pygeon.core.misc.GameObjectManager import GameObjectManager
from pygeon.core.misc.GameObject import GameObject
from pygeon.core.misc.GameObjectComponents import RendererGameObjectComponent
from pygeon.core.networking.NetworkingProtocol import NetworkingProtocol


class NetworkManager:
    __socket = None

    def __init__(self, multiplayer_manager):
        self.multiplayer_manager = multiplayer_manager
        # print(self.web_query("https://www.alphagoofy.de/python/test.php", {"arg": "tests"}))

    def web_query(self, host, arguments: dict):
        q = requests.post(host, arguments)
        return q.text

    def __send(self, data: str):
        e_data = data.encode("utf-8")
        length_str = "0" * (4 - len(str(len(e_data)))) + str(len(e_data))
        self.__socket.send(length_str.encode("utf-8") + e_data)

    def __handle_message(self, message):

        self.multiplayer_manager.debug_last_network_message = message
        self.multiplayer_manager.server_log.insert(1, message)

        print(message)

        if message.__contains__(" "):
            received_array = message.split(" ")

            if received_array[0] == NetworkingProtocol().created_lobby_response():
                if received_array[1] == NetworkingProtocol().success_response():
                    lobby_id = received_array[2]
                    self.multiplayer_manager.set_state(MultiplayerState.IN_LOBBY)
                    self.multiplayer_manager.set_lobby_id(lobby_id)
                    print("lobby created - id:", lobby_id)
            elif received_array[0] == NetworkingProtocol().lobby_list_reponse():
                lobby_count = int((len(received_array) - 1) / 2)
                print("lobby count", lobby_count)
            elif received_array[0] == NetworkingProtocol().join_lobby_response():
                if received_array[1] == NetworkingProtocol().success_response():
                    self.multiplayer_manager.set_state(MultiplayerState.IN_LOBBY)
                    self.multiplayer_manager.set_lobby_id(received_array[2])
                    print("joined lobby", received_array[2])
                elif received_array[1] == NetworkingProtocol().failure_response():
                    print("join failed -", received_array[2])
            elif received_array[0] == NetworkingProtocol().add_synchronised_action():
                test = GameObject(pygame.Vector2(100, 100), "name", True)
                test.add_component(RendererGameObjectComponent("a_id", 3, (1, 1), "renderer", test, True))
            elif received_array[0] == NetworkingProtocol().get_all_objects_response():
                data = []
                ser = Serializer()
                for obj in GameObjectManager().game_objects:
                    data.append(ser.serialize(obj))
                self.__send("send_update all_objects " + received_array[1] + " " + received_array[2] + " "
                            + json.dumps(data))
            elif received_array[0] == NetworkingProtocol().update_response():
                received_objects_data = ""
                for i in range(1, len(received_array)):
                    received_objects_data = received_objects_data + received_array[i]
                data_list = json.loads(received_objects_data)
        else:
            pass

    def connect_to_server(self, host, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((host, port))

            conn_check = uuid.uuid1()

            self.__send(NetworkingProtocol().server_connect_game(conn_check))

            buffer_size = int(self.__socket.recv(4).decode("utf-8"))
            conn_check_recv = self.__socket.recv(buffer_size).decode("utf-8")

            if str(conn_check) != str(conn_check_recv):
                print("error in connection")
                self.multiplayer_manager.server_log.insert(1, "CONNECTION FAILED -> AUTHENTICATION")
                return False
            self.multiplayer_manager.server_log.insert(1, "CONNECTED")
            return True
        except ConnectionRefusedError as e:
            self.multiplayer_manager.server_log.insert(1, "CONNECTION FAILED")
            self.multiplayer_manager.server_log.insert(1, e.strerror)
            return False

    def listen(self):
        ready_to_read, ready_to_write, in_error = select.select([self.__socket], [], [], 0)
        for s in ready_to_read:
            buffer_size = int(s.recv(4).decode("utf-8"))
            self.__handle_message(s.recv(buffer_size).decode("utf-8"))

    def create_lobby(self, lobby_name, lobby_size, player_id):
        self.__send(NetworkingProtocol().server_create_lobby(lobby_name, lobby_size, player_id))

    def get_lobbys(self):
        self.__send(NetworkingProtocol().get_lobbys())

    def join_lobby(self, lobby_id, player_name, player_id):
        self.__send(NetworkingProtocol().join_lobby(lobby_id, player_name, player_id))

    def add_synchronised_object_to_lobby(self, object_data):
        self.__send(NetworkingProtocol().send_to_lobby(NetworkingProtocol().add_synchronised_action(),
                                                       object_data, self.multiplayer_manager.get_lobby_id(),
                                                       self.multiplayer_manager.get_player_id()))

    def get_all_objects_from_host(self, lobby_id, player_id):
        self.__send(NetworkingProtocol().get_all_host_objects(lobby_id, player_id))


class MultiplayerState(Enum):
    NONE = -1
    IN_LOBBY = 0
    IN_GAME = 1


class MultiplayerManager:
    __connected = False
    __player_id = str(uuid.uuid1())
    __player_name = ""
    __state = MultiplayerState.NONE
    __lobby_id = ""

    debug_last_network_message = ""

    def __init__(self):
        self.__network_manager = NetworkManager(self)
        self.server_log = ["Server-Client - Log"]

    def connect(self):
        self.__connected = self.__network_manager.connect_to_server("127.0.0.1", 25563)

        self.debug_last_network_message = "connected" if self.__connected else "connection-error"

    def listen(self):
        if self.__connected:
            self.__network_manager.listen()

    def create_lobby(self, lobby_name, lobby_size):
        self.__network_manager.create_lobby(lobby_name, lobby_size, self.__player_id)

    def set_state(self, state: MultiplayerState):
        self.__state = state

    def set_lobby_id(self, lobby_id):
        self.__lobby_id = lobby_id

    def update_lobby_list(self):
        self.__network_manager.get_lobbys()

    def join_lobby(self, player_name, lobby_id):
        self.__player_name = player_name
        self.__network_manager.join_lobby(lobby_id, self.__player_name, self.__player_id)

    def create_synchronised_object(self, object_data):
        self.__network_manager.add_synchronised_object_to_lobby(object_data)

    def init_get_all_objects(self):
        self.__network_manager.get_all_objects_from_host(self.__lobby_id, self.__player_id)

    def get_player_id(self):
        return self.__player_id

    def get_lobby_id(self):
        return self.__lobby_id

    def is_connected(self):
        return self.__connected
