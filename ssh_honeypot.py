#libraries
import logging  
from  logging.handlers import RotatingFileHandler
import os
import socket
import threading
import paramiko
import sys
#constants 
logging_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#SSH_BANNER = "SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8"
SSH_BANNER ="SSH-2.0-MySSHServer_1.0"
#host_key = paramko.RSAKey(filename='server.key')
host_key = 'server key'

#loggers & logging files 
funnel = logging.getLogger('funnel')
funnel.setLevel(logging.INFO)
funnnel_handler = RotatingFileHandler('audits.log', maxBytes=1000000, backupCount=5)
handler = logging.FileHandler('funnel.log')
funnnel_handler.setFormatter(logging_format)
funnel.addHandler(funnnel_handler)

creds_logger = logging.getLogger('creds')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('credentials.log', maxBytes=1000000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)

#socket server


# Emulated shell
def  emulated_shell(channel, client_address):
    channel.send(b'Phantom coperate -jumpbox2$\n')
    command = b"" # creating a shell environment that is looping through commands
    while True:
        char = channel.recv(1)
        channel.send(char)
        if not char :
            channel.close()
            break
        command += char

        if char == b'\r':
            if command.strip() == b'exit':
                response = b'Goodbye\n'
                #channel.send(response)
                channel.close()
                break
            elif command.strip() == b'pwd':
                response = b'\n\\usr\\local\\'+ b'\r\n'
            elif command.strip() == b'whoami':
                response = b"\n" +b"corpuser" + b"\r\n"
            elif command.strip() == b'ls':
                response = b"\n" +b"jumbox1.conf" + b"\r\n"
            elif command.strip() == b'cat jumbox1.conf':
                response = b"\n" +b"dus doom.com. " + b"\r\n"
            else:
                response = b'\n' +bytes(command.strip()) + b': command not found\n' + b'\r\n'   
                #channel.send(response)
        """if b'\n' in command:
            funnel.info(f'Command: {command.strip()} from {client_address}')
            command = b"" 
            """
        channel.send(response)
        channel.send(b'Phantom coperate -jumpbox2$\n')
        command = b""
        #channel.close()
        
# SSH server + Sockets

class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_address,input_username = None, input_password = None):
        self.client_address = client_address
        self.inpur_username = input_username
        self.input_password = input_password
        #self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def get_allowed_auths(self, username):
        return 'password'
    def check_auth_password(self, username, password):
        if self.input_username == username and self.input_password == password:
            funnel.info(f'Credentials: {username} : {password} from {self.client_address}')
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    def check_channel_exec_request(self, channel, command):
        command = str(command)

        return True


def client_handle(client ,addr, username , password):
    client_address = addr[0]
    funnel.info(f'Connection from {client_address}')
    print()

    
    try:
        transport = paramiko.Transport()
        transport.local_version = SSH_BANNER
        server = SSHServer(client_address, username, password)
        transport.add_server_key(host_key)
        transport.start_server(server=server)

        channel = transport.accept(100)
        if channel is None:
            funnel.info('No channel')
            return
        #funnel.info(f'Channel opened from {client_address}')
        standard_banner = f'Welcome to Phantom coperate\n'
        channel.send(standard_banner)
        emulated_shell(channel, client_address)
    except Exception as e:
        funnel.error(f'Error: {e} from {client_address}')
    finally:
        try :
            transport.close()
            funnel.info(f'Connection closed from {client_address}')
            client.close()
        except Exception as e:
            funnel.error(f'Error: {e} from {client_address}') 
            client.close()   
        """transport.close()
        funnel.info(f'Connection closed from {client_address}')
        client.close()
"""


# Sockets


#Provison SSH-Based honeypot
def honeypot(address, port, username, password):
   socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
   
   
   
   """ funnel.info(f'Starting SSH honeypot on {address}:{port}')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((address, port))
    server.listen(5)
    funnel.info('Waiting for connection')
    while True:
        client, addr = server.accept()
        client_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))
        client_thread.start()
    server.close()"""