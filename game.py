from db_connection import Db_connection as db

class Game:
    def __init__(self, player1, player2, _name):
        self.players = [player1, player2]
        self.turn = int(-1)
        self.name = _name
        self.winner = None
        self.loser = None
        self.id = int(-1)
        self.board = [[-1]*3 for i in range(3)]
        self.is_finished = False

        result = db.query('INSERT INTO games (player1Id) VALUES ({})'.format(player1.get_id()))
        self.id = result[0][0]

    def __del__(self):
        for p in self.players:
            if p != None:
                self.players.remove(p)

        if self.winner != None:
            self.save_game_score()

    def get_winner(self):
        return self.winner
    
    def get_loser(self):
        return self.loser

    def get_id(self):
        return self.id

    def get_board(self):
        return self.board

    def get_name(self):
        return self.name

    def get_players_info(self):
        players = []

        for player in self.players:
            if player != None:
                p = {}
                p["id"] = player.get_id()
                p["name"] = player.get_name()
                p["mmr"] = player.get_mmr()
                players.append(p)

        return players

    def save_game_score(self):
        if self.winner == None and self.loser == None:
            return

        pw = 0
        pl = 0

        if self.winner == self.players[0].get_id():
            pw = self.players[0]
            pl = self.players[1]
        else:
            pw = self.players[1]
            pl = self.players[0]

        db.query('UPDATE games SET winnerId = {} WHERE id = "{}"'.format(pw.get_id(), self.id))
        db.query('UPDATE players SET mmr = (mmr + 10) WHERE id = "{}"'.format(pw.get_id()))
        db.query('UPDATE players SET mmr = (mmr - 10) WHERE id = "{}"'.format(pl.get_id()))
        pl.set_mmr(pl.get_mmr() - 10)
        pw.set_mmr(pw.get_mmr() + 10)
        self.is_finished = True

    def start_game(self):
        if self.players[0] != None and self.players[1] != None:
            result = db.query('UPDATE games SET player1Id = {}, player2Id = {} WHERE id = {}'.format(self.players[0].get_id(), self.players[1].get_id(), self.id))
            self.turn = 0
        else:
            raise Exception("Not enough players to start a game")
    
    def add_player(self, _player):
        if _player in self.players:
            raise Exception("Player already in game")

        if self.players[0] == None:
            self.players[0] = _player
        elif self.players[1] == None:
            self.players[1] = _player
        else:
            raise Exception("Game is full")

        if self.players[0] != None and self.players[1] != None:
            self.start_game()

    def remove_player(self, _player):
        if _player not in self.players:
            raise Exception("Player not in this game")
        
        if self.turn != int(-1):
            self.is_finished = True
            if self.players[0] != _player:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
            self.loser = _player

    def get_players(self):
        return self.players

    ''' 
        returns:
        -1 if no winner yet
        0 if first player won
        1 if second player won
        2 if draw
    '''
    def check_winning_condition(self):
        if self.is_finished:
            return self.winner

        for i in range(3):
            if self.board[0][i] == -1:
                continue
            elif self.board[0][i] == self.board[1][i] == self.board[2][i]:
                self.winner = self.board[0][i]
        
        for i in range(3):
            if self.board[i][0] == -1:
                continue
            elif self.board[i][0] == self.board[i][1] == self.board[i][2]:
                self.winner = self.board[i][0]

        if self.board[0][0] != -1 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            self.winner = self.board[0][0]

        if self.board[0][2] != -1 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            self.winner = self.board[0][2]

        if self.winner != None:
            if self.players[0].get_id() == self.winner:
                self.loser = self.players[1].get_id()
            else:
                self.loser = self.players[0].get_id()
            self.is_finished = True
            return self.winner

        counter = 0
        for row in self.board:
            counter += row.count(-1)

        if counter == 0:
            self.winner = None
            self.loser = None
            return -2

        return -1
    
    def make_move(self, player, positionX, positionY):
        if self.id == int(-1):
            raise Exception("Game is not started yet")

        if positionX > 2 or positionX < 0 or positionY > 2 or positionY < 0:
            raise Exception("Wrong position")

        if player not in self.players:
            raise Exception("Wrong player")

        if self.board[positionX][positionY] != -1:
            raise Exception("Position is taken")

        if self.turn != self.players.index(player):
            raise Exception("Not your turn")

        self.board[positionX][positionY] = player.get_id()
        self.turn = int(not self.turn)
        self.print_board()

    def print_board(self):
        for row in self.board:
            print(row)