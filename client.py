import socket
import threading

from utils.prompt_utils import PromptUtility
from utils.message_utils import MessageHandler


class ChatClient:
    def __init__(self, bind_host="127.0.0.1", bind_port=0):
        self.message_handler = MessageHandler()
        self.prompt_util = PromptUtility()
        self.address = (bind_host, bind_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __connect_to(self, connect_address, blocking=False):
        self.client_socket.bind(self.address)
        self.client_socket.connect(connect_address)
        self.client_socket.setblocking(blocking)

    def start(self, connect_address):
        self.__connect_to(connect_address)

        while True:
            message_send = input(self.prompt_util.prompt)
            self.message_handler.send_handle(self.client_socket, message_send)

            message_receive = self.message_handler.receive_handle(self.client_socket)

            if message_receive:
                print(message_receive.data)