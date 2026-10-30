import os
from scapy.all import sniff, TCP, IP
import msvcrt
from stickempiresloginmessageextractor.StickEmpiresLoginMessageValidator import StickEmpiresLoginMessageValidator
from stickempiresloginmessageextractor.StickEmpiresServerConnector import StickEmpiresServerConnector
from stickempiresloginmessageextractor.LoginMessageSaver import LoginMessage
from stickempiresloginmessageextractor.utils import PORT, SERVER_IP

_is_done = False

_pending_logins: dict[int, bytes] = {}


def log(tag: str, message: str) -> None:
    print(f"[{tag:<6}] {message}")


def packet_analyze(packet):
    global _is_done
    if _is_done:
        return
    if not (packet.haslayer(IP) and packet.haslayer(TCP)):
        return

    ip = packet[IP]
    tcp = packet[TCP]

    data = bytes(tcp.payload)
    if not data:
        return

    if ip.dst == SERVER_IP and tcp.dport == PORT:
        log("SEND", f"{ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport} | {len(data)} bytes")

        if LoginMessage.is_login_message(data):
            log("LOGIN", f"Login message detected (local port {tcp.sport}). Waiting for the server's response...")
            _pending_logins[tcp.sport] = data
        return

    if ip.src == SERVER_IP and tcp.sport == PORT:
        pending = _pending_logins.pop(tcp.dport, None)
        if pending is None:
            return

        log("RECV", f"{ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport} | {len(data)} bytes")

        if StickEmpiresLoginMessageValidator.is_login_validated_by_server(data):
            log("OK", "Server accepted the login.")
            LoginMessage.save_login_message(pending)
            log("OK", f"Login message saved to {LoginMessage.FILE_PATH}.")
            _is_done = True
        else:
            log("FAIL", "Server rejected the login (wrong password?). Nothing saved.")
            log("INFO", "Still listening, try logging in again...")


def main():
    if os.path.exists(LoginMessage.FILE_PATH):
        os.remove(LoginMessage.FILE_PATH)

    log("INFO", "Listening for TCP traffic. Log in to Stick Empires now. (Ctrl+C to stop)")
    try:
        while not _is_done:
            sniff(
                filter=f"tcp and host {SERVER_IP} and port {PORT}",
                prn=packet_analyze,
                store=False,
                timeout=1,
                stop_filter=lambda _: _is_done,
            )
    except KeyboardInterrupt:
        print()
        log("INFO", "Stopped by user.")
        return

    print()
    log("INFO", f"Capture finished. Your login message is in {LoginMessage.FILE_PATH}.")
    log("INFO", "Log off from Stick Empires, then press 't' to start the test.")
    while msvcrt.getwch().lower() != "t":
        pass

    print()
    log("TEST", "Replaying the saved login message...")
    login_message = LoginMessage.extract_login_message()
    connector = None
    try:
        connector = StickEmpiresServerConnector()
        connector.connect()
        connector.send_login_message(login_message)
        login_response = connector.get_next_message()

        if StickEmpiresLoginMessageValidator.is_login_validated_by_server(login_response):
            log("OK", "Success!, the server accepted the saved login message.")
            log("INFO", "You can copy the login credentials and follow the instructions of the StickEmpiresDailyCoinCollector project.")
        else:
            raise RuntimeError(
                "Login validation failed. You can figure it out yourself, "
                "or try contacting the developer. If he hasn't found a job yet, "
                "he'll get back to you ¯\\_(ツ)_/¯"
            )
    except Exception as e:
        log("FAIL", str(e))

    finally:
        if connector:
            connector.close()