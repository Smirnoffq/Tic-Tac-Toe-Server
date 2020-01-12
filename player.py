from db_connection import Db_connection as db

class Player:
    def __init__(self, name):
        self.name = name
        self.status = "Online"
        self.mmr = int(1000)
        self.id = 0
        
        self.load_info()

    def __del__(self):
        db.query('UPDATE players SET mmr = {} WHERE name = "{}"'.format(self.mmr, self.name.lower()))

    def load_info(self):
        result = db.query('SELECT id, mmr FROM players WHERE name = "{}"'.format(self.name.lower()))

        if len(result) > 0:
            self.id = int(result[0][0]) # bo results to lista
            self.mmr = int(result[0][1]) # bo results to lista
        else:
            db.query('INSERT INTO players (name) VALUES ("{}")'.format(self.name.lower()))

    def set_mmr(self, mmr):
        self.mmr = int(mmr)

    def get_mmr(self):
        return self.mmr
        
    def get_id(self):
        return self.id

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_name(self):
        return self.name