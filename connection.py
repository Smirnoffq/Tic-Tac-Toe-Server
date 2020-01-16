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
                message = Messenger.receive(self.socket)
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

            Messenger.send(response_encoded, self.socket)
            print("Response sent: ", response)

        self.__del__() # call destructor

    def __del__(self):
        self.info_container.remove_connection(self) # remove from clients list
        self.send_players_list()

    def get_socket(self):
        return self.socket

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
        if message["sub_operation"] == 0: # login
            if self.player != None:
                raise Exception("Already logged in")
            if len(message["name"]) > 0:
                if self.info_container.find_player_by_name(message["name"]) is not None:
                    raise Exception("Player with this name already logged in")

                self.player = Player(message["name"], self.socket)
                self.send_players_list()

                return "Logged in"
        elif message["sub_operation"] == 1: # logout 
            # remove from games
            game = self.info_container.find_player_game(self.player)
            if game == None:
                raise Exception("Player not in game")

            game.remove_player(self.player)
            self.check_win_condition(user_game)
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
            self.send_games_list()

            return "Created"
        elif message["sub_operation"] == 1: # join game
            if self.info_container.find_player_game(self.player) != None:
                raise Exception("Player already in game")

            game = self.info_container.find_game_by_id(message["id"])

            if game == None:
                raise Exception("Game does not exist")

            game.add_player(self.player)
            self.send_game_board(game)
            self.send_games_list()

            return "Joined"
        elif message["sub_operation"] == 2: # leave game
            game = self.info_container.find_player_game(self.player)
            if game == None:
                raise Exception("Player not in game")

            game.remove_player(self.player)
            self.check_win_condition(user_game)
            self.info_container.remove_game(game)

        else:
            raise Exception("Wrong sub operation")

    def handle_game_move(self, message):
        if message["sub_operation"] == 0:
            user_game = self.info_container.find_player_game(self.player)
            if user_game != None:
                user_game.make_move(self.player, message["posX"], message["posY"])

                self.send_game_board(user_game)
                self.check_win_condition(user_game)
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

    def check_and_send_win_condition(self, game):
        result = game.check_winning_condition()

        if result == int(-1):
            return 0
        else: # send win info
            msg = {}
            msg["operation"] = 1,
            msg["sub_operation"] = 0,
            msg["winner"] = game.get_winner()
            msg["loser"] = game.get_loser()

            encoded_msg = Messenger.encode_data(msg)
            players = game.get_players()

            for p in players:
                if p is not None:
                    Messenger.send(encoded_msg, p.get_socket())
                    print("Score sent: ", msg)

    def send_game_board(self, game):
        board = game.get_board()

        msg = {}
        msg["operation"] = 2
        msg["sub_operation"] = 0
        msg["board"] = board

        encoded_msg = Messenger.encode_data(msg)
        players = game.get_players()

        for p in players:
            if p is not None:
                Messenger.send(encoded_msg, p.get_socket())
                print("Board sent: ", msg)

    def send_games_list(self):
        games = self.info_container.get_games_info()
        msg = {}
        msg["operation"] = 3
        msg["sub_operation"] = 0
        msg["games"] = games

        encoded_msg = Messenger.encode_data(msg)
        connections = self.info_container.get_connections()

        for c in connections:
            Messenger.send(encoded_msg, c.get_socket())
            print("Games list sent: ", msg)

    def send_players_list(self):
        players = self.info_container.get_players_info()
        msg = {}
        msg["operation"] = 3
        msg["sub_operation"] = 1
        msg["players"] = players

        encoded_msg = Messenger.encode_data(msg)
        connections = self.info_container.get_connections()

        for c in connections:
            Messenger.send(encoded_msg, c.get_socket())
            print("Players list sent: ", msg)
