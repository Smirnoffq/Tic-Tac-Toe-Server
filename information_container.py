
class InformationContainer:
    def __init__(self):
        self.connections = []
        self.games = []

    def get_games(self):
        return self.games
    
    def get_games_info(self):
        games = []

        for game in self.games:
            info = {}
            info["id"] = game.get_id()
            info["name"] = game.get_name()
            info["players_count"] = 0

            for player in game.get_players():
                if player != None:
                    info["players_count"] = info["players_count"] + 1

            games.append(info)

        return games

    def find_player_game(self, player):
        for game in self.games:
            players = game.get_players()
            if player in players:
                return game

        return None

    def find_game_by_id(self, game_id):
        for game in self.games:
            if game.get_id() == int(game_id):
                return game
        
        return None

    def get_connections(self):
        return self.connections

    def get_players(self):
        players = []

        for connection in self.connections:
            tmp_player = connection.get_player()
            if tmp_player is not None:
                players.append(tmp_player)

        return players

    def get_players_info(self):
        players = []

        for connection in self.connections:
            tmp_player = connection.get_player()
            if tmp_player is not None:
                info = {}
                info["name"] = tmp_player.get_name()
                info["status"] = tmp_player.get_status()
                info["mmr"] = tmp_player.get_mmr()
                players.append(info)

        return players

    def find_player_by_name(self, name):
        players = self.get_players()
        
        for player in players:
            if player.get_name() == name:
                return player
        
        return None

    def add_connection(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)
    
    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)


    def add_game(self, game):
        if game not in self.games:
            self.games.append(game)

    def remove_game(self, game):
        if game in self.games:
            self.games.remove(game)