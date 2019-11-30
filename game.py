from db_connection import Db_connection as db

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.winner = int(-1)
        self.board = [
            [-1,-1,-1],
            [-1,-1,-1],
            [-1,-1,-1],
        ]

        result = db.query('INSERT INTO games (player1Id, player2Id, winnerId) VALUES ({}, {}, {})'.format(player1.get_id(), player2.get_id(), self.winner))
        
        self.id = result[0][0]

    def get_id(self):
        return self.id

    def set_winner_id(self, winnerId):
        self.winner = int(winnerId)

    def save_game_score(self):
        if self.winner != -1 and self.id != -1:
            db.query('UPDATE games SET winnerId = {} WHERE id = "{}"'.format(self.winner, self.id))

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

        return -1
    
    def make_move(self, player, positionX, positionY):
        if positionX > 2 or positionX < 0 or positionY > 2 or positionY < 0:
            raise Exception("Wrong position")
    
        if player not in self.players:
            raise Exception("Wrong player")

        if self.board[positionY][positionX] != -1:
            raise Exception("Position is taken")

        self.board[positionY][positionX] = self.players.index(player)