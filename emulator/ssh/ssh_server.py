import paramiko
import threading

from logger import logger


class SSHServer(paramiko.ServerInterface):
    def __init__(self, login: str = '', password: str = ''):
        self.login = login
        self.password = password

        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        logger.info(f'Bot uses username: {username}, password: {password}')

        if not self.login or not self.password:
            return paramiko.AUTH_SUCCESSFUL

        if self.login == username and self.password == password:
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True