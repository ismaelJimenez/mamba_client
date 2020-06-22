import socketserver
import threading

eom = '\r\n'


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

            if data != 'wrong':
                # just send back the same data, but upper-cased
                self.request.sendall(f'> OK {data}{eom}'.encode('ascii'))
            else:
                self.request.sendall(f'> ERROR wrong{eom}'.encode('ascii'))


class ThreadedTcpServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ TC server to modify the telemetries """


class MambaServerMock:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080):
        # Create the TM socket server, binding to host and port
        socketserver.TCPServer.allow_reuse_address = True
        self._server = ThreadedTcpServer((host, port), ThreadedTcpHandler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self._server_thread = threading.Thread(
            target=self._server.serve_forever)

        # Exit the server thread when the main thread terminates
        self._server_thread.daemon = True
        self._server_thread.start()
