from db_connection import Db_connection as db

class Game:
    def __init__(self, player1, player2, _name):
        self.players = [player1, player2]
        self.turn = int(-1)
        self.name = ""
        self.winner = int(-1)
        self.id = int(-1)
        self.board = [
            [-1,-1,-1],
            [-1,-1,-1],
            [-1,-1,-1],
        ]

    def get_id(self):
        return self.id

    def set_winner_id(self, winnerId):
        self.winner = int(winnerId)

    def save_game_score(self):
        if self.winner != -1 and self.id != -1:
            db.query('UPDATE games SET winnerId = {} WHERE id = "{}"'.format(self.winner, self.id))

    def start_game(self):
        if self.players[0] != None and self.players[1] != None:
            result = db.query('INSERT INTO games (player1Id, player2Id, winnerId) VALUES ({}, {}, {})'.format(player1.get_id(), player2.get_id(), self.winner))
            self.id = result[0][0]
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
        for i in range(3):
            if self.board[0][i] == -1:
                continue
            elif self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        
        for i in range(3):
            if self.board[i][0] == -1:
                continue
            elif self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]

        if self.board[0][0] != -1 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]

        if self.board[0][2] != -1 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

        if int(-1) not in self.board:
            return 2 # draw

        return -1
    
    def make_move(self, player, positionX, positionY):
        if self.id == int(-1):
            raise Exception("Game is not started yet")

        if positionX > 2 or positionX < 0 or positionY > 2 or positionY < 0:
            raise Exception("Wrong position")

        if player not in self.players:
            raise Exception("Wrong player")

        if self.board[positionY][positionX] != -1:
            raise Exception("Position is taken")

        if self.turn != self.players.index(player):
            raise Exception("Not your turn")

        self.board[positionY][positionX] = self.players.index(player)
        self.turn = int(not self.turn)