import socket
import threading

from game import Game
from player import Player
from messenger import Messenger

class Connection (threading.Thread):

    def __init__(self, _socket, _info_container):
        threading.Thread.__init__(self)
        self.socket = _socket
        self.info_container = _info_container
        self.player = None
        self.delete_self = False

    def run(self):
        while True:
            if self.delete_self:
                break

            try:
                message = self.receive()
                message = Messenger.decode_data(message)
                print("New message: ", message)
            except RuntimeError as re:
                print(re)
                self.delete_self = True
                break # user disconnected

            try:
                response = self.handle_message(message)
                response_encoded = Messenger.encode_data(response)
            except Exception as e:
                print("Error in encoding data: ", e)
                continue

            self.send(response_encoded)
            print("Response sent: ", response)

        self.__del__() # call destructor

    def __del__(self):
        self.info_container.remove_connection(self) # remove from clients list

    def receive(self):
        msg = b''
        while b';' not in msg and len(msg) < Messenger.MSG_LEN:
            
            chunk = self.socket.recv(min(Messenger.MSG_LEN - len(msg), Messenger.MSG_LEN))
            if chunk == b'':
                raise RuntimeError("Socket disconnected")
            msg = msg + chunk
        return msg

    def send(self, data):
        sent_count = 0
        while sent_count < Messenger.MSG_LEN:
            sent = self.socket.send(data[sent_count:])
            if sent == 0:
                raise RuntimeError("Socket disconnected")
            sent_count = sent_count + sent

    def get_player(self):
        return self.player

    def handle_message(self, message):
        handlers = [self.handle_login_logout, self.handle_game_managment, 
                    self.handle_game_move, self.handle_lists]
        result = False
        response = {}
        response["operation"] = message["operation"]
        response["sub_operation"] = message["sub_operation"]

        try:
            if self.player == None and message["operation"] != 0:
                raise Exception("User not logged in")
            result = handlers[message["operation"]](message)
        except Exception as e:
            print("Error in message handler: ", e)
            response["status"] = False
            response["message"] = str(e)

        if result != False:
            response["status"] = True
            response["message"] = result
        
        return response

    def handle_login_logout(self, message):
        if message["sub_operation"] == 0:
            if self.player != None:
                raise Exception("Already logged in")
            if len(message["name"]) > 0:
                if self.info_container.find_player_by_name(message["name"]) is not None:
                    raise Exception("Player with this name already logged in")

                self.player = Player(message["name"])

                return "Logged in"
        elif message["sub_operation"] == 1:
            # remove from games
            game = self.info_container.find_player_game(self.player)
            if game == None:
                raise Exception("Player not in game")

            game.remove_player(self.player)
            self.info_container.remove_game(game)

            self.delete_self = True #exit request loop
        else:
            raise Exception("Wrong sub operation")

    def handle_game_managment(self, message):
        if message["sub_operation"] == 0: # create game
            if self.info_container.find_player_game(self.player) != None:
                raise Exception("Player already in game")

            game = Game(self.player, None, message["name"])
            self.info_container.add_game(game)

            return "Created"
        elif message["sub_operation"] == 1: # join game
            if self.info_container.find_player_game(self.player) != None:
                raise Exception("Player already in game")

            game = self.info_container.find_game_by_id(message["id"])

            if game == None:
                raise Exception("Game does not exist")

            game.add_player(self.player)

            return "Joined"
        elif message["sub_operation"] == 2: # leave game
            game = self.info_container.find_player_game(self.player)
            if game == None:
                raise Exception("Player not in game")

            game.remove_player(self.player)
            self.info_container.remove_game(game)

        else:
            raise Exception("Wrong sub operation")

    def handle_game_move(self, message):
        if message["sub_operation"] == 0:
            user_game = self.info_container.find_player_game(self.player)
            if user_game != None:
                user_game.make_move(self.player, message["posX"], message["posY"])

                return "Moved"
            else:
                raise Exception("Player not in game")
        else:
            raise Exception("Wrong sub operation")

    def handle_lists(self, message):
        if message["sub_operation"] == 0:
            return self.info_container.get_games_info()
        elif message["sub_operation"] == 1:
            return self.info_container.get_players_info()
        else:
            raise Exception("Wrong sub operation")
