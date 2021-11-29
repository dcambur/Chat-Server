import socket
import select

from utils.message_utils import MessageHandler
from utils.prompt_utils import PromptUtility


class SocketServer:
    def __init__(self, bind_host="127.0.0.1", bind_port=7777):
        """ bind_host ::: contains host part of address
            bind_port ::: contains port part of address """

        self.message_handler = MessageHandler()

        self.address = (bind_host, bind_port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_list = [self.server_socket]
        self.clients = {}

    def __setup_listen(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen()

    def start(self):
        self.__setup_listen()
        print("SERVER IS RUNNING!")
        while True:
            read_sockets, _, exception_sockets = select.select(self.socket_list, [], self.socket_list)

            for read_socket in read_sockets:
                if read_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    client_socket.send("Welcome".encode("utf-8"))
                    message = self.message_handler.receive_handle(client_socket)

                    if message is False:
                        continue

                    self.socket_list.append(client_socket)
                    self.clients[client_socket] = client_address

                    print(f'Accepted new connection from: {client_address}')

                else:
                    message = self.message_handler.receive_handle(read_socket)
                    if message is False:
                        print(f"Closed connection from: {self.clients[read_socket]}")
                        self.socket_list.remove(read_socket)
                        del self.clients[read_socket]
                        continue

                    for broadcast_socket in self.socket_list:
                        if broadcast_socket != read_socket:
                            self.message_handler.send_handle(broadcast_socket, message)