class NetworkingProtocol:

    def server_connect_game(self, test_str):
        return "connect "+str(test_str)

    def server_create_lobby(self,lobby_name, lobby_size, player_id):
        return "create_lobby " + lobby_name + " " + str(lobby_size) + " " + player_id

    def created_lobby_response(self):
        return "create_lobby"

    def success_response(self):
        return "success"

    def failure_response(self):
        return "failure"

    def lobby_list_reponse(self):
        return "lobby_list"

    def get_lobbys(self):
        return "list_lobbys"

    def join_lobby_response(self):
        return "join_lobby"

    def join_lobby(self, lobby_id, player_name, player_id):
        return "join_lobby "+lobby_id+" "+player_name+" "+player_id

    def send_to_lobby(self, action, data, lobby_id, player_id):
        return "send_lobby "+action+" "+player_id+" "+lobby_id+" "+str(data)

    def add_synchronised_action(self):
        return "add_synchronised_object"

    def get_all_host_objects(self, lobby_id, player_id):
        return "get_all_objects_host "+lobby_id+" "+player_id

    def get_all_objects_response(self):
        return "request_all_objects"

    def update_response(self):
        return "update"
