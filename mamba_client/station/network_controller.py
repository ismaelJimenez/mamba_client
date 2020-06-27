import telnetlib

from mamba_client.station.exceptions import MambaClientException

eom = '\r\n'


class NetworkController:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080) -> None:
        self._inst = telnetlib.Telnet(host, port)

    def query(self, msg: str) -> str:
        self._inst.write(f'{msg}{eom}'.encode('ascii'))
        reply = self._inst.read_until(
            f'{eom}'.encode('ascii'))[:-2].decode('ascii').rstrip().split(
                ' ', 2)[1:]

        if reply[0] != 'OK':
            raise MambaClientException(' '.join(reply))

        return reply[1]

    def close(self) -> None:
        self._inst.close()
