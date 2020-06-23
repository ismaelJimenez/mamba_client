import socketserver
import threading
import time

eom = '\r\n'


class MambaServerMock:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080):
        self._shared_memory = {'last_tc': '', 'last_tm': ''}

        # Create the TM socket server, binding to host and port
        socketserver.TCPServer.allow_reuse_address = True
        self._server = ThreadedTcpServer((host, port), ThreadedTcpHandler,
                                         self)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self._server_thread = threading.Thread(
            target=self._server.serve_forever)

        # Exit the server thread when the main thread terminates
        self._server_thread.daemon = True
        self._server_thread.start()


class ThreadedTcpHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for the socket server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # Server to receive remote commands
        while True:
            data = self.request.recv(1024).strip().decode('ascii')
            if not data:
                break

            self.server.shared_memory['last_tc'] = data

            data_split = data.split(" ", 2)

            if data_split[1] == 'wrong':
                reply = f'> ERROR {data_split[1]} Non existing command '
            else:
                if data_split[0] == 'tc':
                    # just send back the same data, but upper-cased
                    reply = f'> OK {data_split[1]}'

                elif data_split[0] == 'tc_meta':
                    reply = f'> OK {data_split[1]};' \
                            f'{int(data_split[1].split("_")[1])};test ' \
                            f'description'

                elif data_split[0] == 'tm_meta':
                    reply = f'> OK {data_split[1]};str;str;test description' \
                            f';7;4'

                elif data_split[0] == 'tm':
                    reply = f"> OK {data_split[1]};{time.time()};1;1;0;1"

            self.server.shared_memory['last_tm'] = reply
            self.request.sendall(f'{reply}{eom}'.encode('ascii'))


class ThreadedTcpServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ TC server to modify the telemetries """
    def __init__(self, server_address, request_handler_class,
                 parent: MambaServerMock) -> None:
        super().__init__(server_address, request_handler_class)
        self.shared_memory = parent._shared_memory
