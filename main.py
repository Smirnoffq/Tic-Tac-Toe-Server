import sys
import sqlite3
import socket
from connection import Connection
from information_container import InformationContainer

def main(args):
    port = 9999
    host = '127.0.0.1'
    info_container = InformationContainer()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(10)

    print("Listening on port %s..." % port)
    while True:
        (clientsocket, address) = server_socket.accept()
        ct = Connection(clientsocket, info_container)
        info_container.add_connection(ct)
        ct.start()

if __name__ == "__main__":
    main(sys.argv)