from starter import Starter 
from server.ssh import SSHServer
from output import FileOutHandler, SocketOutHandler
from executor import SimpleExecutor, LocalExecutor
from emulate_terminal import EmulateSSHTerminal, BashEmulateTerminal
from config import config
from logger import FileLogger, DataLog, DataBaseLogger


service = {
	"EmulateSSHTerminal": EmulateSSHTerminal,
    "LocalExecutor": LocalExecutor,
    "SimpleExecutor": SimpleExecutor,
    "SocketOutHandler": SocketOutHandler,
    "FileOutHandler": FileOutHandler,
    "FileLogger": FileLogger,
    "DataBaseLogger": DataBaseLogger,
    "SSHServer": SSHServer,
    "Starter": Starter,
}

#emul_term = service[config.data.service.emulate_terminal]()
executor = service[config.data.service.executor]()
logger = service[config.data.service.logger]()
emul_term = BashEmulateTerminal(logger)

if config.data.service.output == "SocketOutHandler":
	out = SocketOutHandler(config.data.socket_out.server_ip, config.data.socket_out.server_port)

if config.data.service.output == "FileOutHandler":
	out = FileOutHandler(config.data.path.file_out_path)

if config.data.service.server == "SSHServer":
	server = SSHServer(
		config.data.path.ssh_keys_path, 
		emul_term, 
		executor, 
		out,
		logger,
		login=config.data.client.login,
		password=config.data.client.password,
	)

starter = service[config.data.service.starter](
	server, logger, host=config.data.server.host, 
	port=config.data.server.port
)
starter.start_server(listen_number=config.data.server.listen_number)

