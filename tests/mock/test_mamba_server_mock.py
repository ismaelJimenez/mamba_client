import pytest

from mamba_client.core.network_controller import NetworkController
from mamba_client.mock.mamba_server_mock import MambaServerMock
from mamba_client.core.exceptions import MambaClientException

import socket
import time

# from mamba.core.context import Context
# from mamba.mock.tcp.single_port_tcp_mock import SinglePortTcpMock


class TestClass:
    def test_network_controller(self):
        MambaServerMock(port=34567)
        network_controller = NetworkController(port=34567)
        reply = network_controller.query('X')

        assert reply == 'X'

        with pytest.raises(MambaClientException) as excinfo:
            network_controller.query('wrong')
            time.sleep(.1)

        assert 'ERROR wrong' in str(excinfo.value)

        network_controller.close()
