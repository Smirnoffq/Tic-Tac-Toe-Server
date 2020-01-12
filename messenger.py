import base64
import json

class Messenger:
    MSG_LEN = 4096

    @staticmethod
    def encode_data(data):
        if not isinstance(data, dict):
            raise Exception("Wrong input data")

        json_data = json.dumps(data).encode("utf-8")
        base64_data = base64.b64encode(json_data) + b';'
        
        return base64_data + (b'0' * (Messenger.MSG_LEN - len(base64_data)))

    @staticmethod
    def decode_data(data):
        if b';' not in data:
            raise Exception("Wrong input data: missing ';'")

        data = data.split(b';')[0]
        json_data = base64.b64decode(data)
        decoded_data = json.loads(json_data)
        
        return decoded_data