import socket
from stickempiresloginmessageextractor.utils import SERVER_IP, PORT


class StickEmpiresServerConnector:
    def __init__(self, server_ip: str = SERVER_IP, port: int = PORT):
        self.server_ip = server_ip
        self.port = port
        self.client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_login_message(self, login_message: bytes):
        try:
            self.client.sendall(login_message)
        except Exception as e:
            print(f"Error sending login message: {e}")
            raise


    def connect(self):
        try:
            self.client.connect((self.server_ip, self.port))
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise

    def get_next_message(self, buffer_size: int = 10240) -> bytes:
        try:
            return self.client.recv(buffer_size)
        except Exception as e:
            print(f"Error receiving message: {e}")
            raise

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
            raise