from starter import Starter 
from server.ssh import SSHServer
from output import FileOutHandler
from executor import SimpleExecutor, LocalExecutor
from emulate_terminal import EmulateSSHTerminal


emul_term = EmulateSSHTerminal()
executor = LocalExecutor()
out = FileOutHandler()
ssh_server = SSHServer("server/ssh/ssh_keys/fake_ssh_host_key", emul_term, executor, out)

starter = Starter(ssh_server)
starter.start_server(listen_number=1)



















# # from output import FileOutHandler

# # f = FileOutHandler()
# # f.log_ip('124.53.222.123')
# # f.log_ip('133.53.252.123')
# # f.notify('testim')

# import socket
# import paramiko
# import threading
# import logging

# from server import SSHServerInterface


# host_key = paramiko.RSAKey(filename="server/ssh/ssh_keys/fake_ssh_host_key")

# def handle_client(client):
#     transport = paramiko.Transport(client)
#     transport.add_server_key(host_key)

#     server = SSHServerInterface()
#     transport.start_server(server=server)

#     channel = transport.accept(20)  # Ожидание клиента
#     if channel is None:
#         return

#     server.event.wait(10)  # Ожидание shell
#     if not server.event.is_set():
#         return

#     channel.send("Добро пожаловать в фальшивую систему!\n")

#     while True:
#         #переделать отдельным классом emulterminal
#         #отдельным классом сделать выполнение команд
#         channel.send("honeypot$ ")
#         command = channel.recv(1024).decode().strip()
#         print(command)

#         if command.lower() in ["exit", "quit"]:
#             channel.send("Пока!\n")
#             break
#         elif command.startswith("ls"):
#             channel.send("file1.txt  file2.log  secrets\n")
#         elif command.startswith("cat secrets"):
#             channel.send("admin:password123\n")
#         else:
#             channel.send("Команда не найдена.\n")

#     channel.close()

# def start_server(host="0.0.0.0", port=2222):
#     # будет методом в общем классе для всех
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind((host, port))
#     server_socket.listen(100)

#     print(f"SSH Honeypot запущен на {host}:{port}") # заменить для каждого своё (можно методом вызывать)

#     while True:
#         client, addr = server_socket.accept()
#         print(client, addr)
#         print(f"Новое соединение: {addr[0]}:{addr[1]}")
#         threading.Thread(target=handle_client, args=(client,)).start()

# if __name__ == "__main__":
#     start_server()
