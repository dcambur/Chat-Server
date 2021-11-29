from client import ChatClient

if __name__ == "__main__":
    client = ChatClient()
    client.start(("127.0.0.1", 7777))
