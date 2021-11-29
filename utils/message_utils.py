class Header:
    """ For now Header is just a data length pointer """
    LENGTH = 10


class MessageContent:
    """ header ::: tells the message length with padding
        data ::: the message itself"""

    def __init__(self, header, data):
        self.header = header
        self.data = data.decode("utf-8")


class MessageHandler:
    def __init__(self, header_length=10):
        self.header_length = header_length

    def receive_handle(self, receiver_socket):
        try:

            message_header = receiver_socket.recv(self.header_length)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())
            return MessageContent(message_header, receiver_socket.recv(message_length))
        except:
            return False

    def send_handle(self, recipient_socket, message):
        try:
            message_header = f"{len(message):<{self.header_length}}"
            recipient_socket.send((message_header + message).encode("utf-8"))

        except:
            return False
