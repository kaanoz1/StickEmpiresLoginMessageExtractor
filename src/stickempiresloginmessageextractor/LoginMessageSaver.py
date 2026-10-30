class LoginMessage:
    FILE_PATH = "login_messages.txt"

    @staticmethod
    def save_login_message(message: bytes | str) -> None:
        data = bytes.fromhex(message) if isinstance(message, str) else message
        with open(LoginMessage.FILE_PATH, "w") as file:
            file.write(data.hex())

    @staticmethod
    def extract_login_message() -> bytes:
        with open(LoginMessage.FILE_PATH, "r") as file:
            first_line = file.readline().strip()
        return bytes.fromhex(first_line)

    @staticmethod
    def is_login_message(message: bytes) -> bool:
        required = (b"version", b"password", b"fuid", b"isFacebook", b"stickwar")
        return all(key in message for key in required)