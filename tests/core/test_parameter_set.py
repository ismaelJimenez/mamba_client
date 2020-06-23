import pytest

from mamba_client.core.network_controller import NetworkController
from mamba_client.core.parameter_set import ParameterSet
from mamba_client.mock.mamba_server_mock import MambaServerMock
from mamba_client.core.exceptions import ParameterSetException, MambaClientException


class TestClass:
    def test_parameter_set_init(self):
        MambaServerMock(port=34568)
        network_controller = NetworkController(port=34568)

        param_set = ParameterSet(network_controller=network_controller,
                                 parameter_id='test_1')

        assert param_set._network_controller == network_controller
        assert param_set._parameter_id == 'test_1'
        assert param_set._arg_1 is None
        assert param_set._arg_2 is None
        assert param_set._arg_3 is None
        assert param_set._arg_4 is None
        assert param_set._arg_5 is None
        assert param_set._arg_6 is None
        assert param_set._arg_7 is None
        assert param_set._arg_8 is None
        assert param_set._arg_9 is None
        assert param_set._arg_10 is None
        assert param_set._argc == 1

        param_set = ParameterSet(network_controller=network_controller,
                                 parameter_id='test_10',
                                 arg_1=1,
                                 arg_10='10')

        assert param_set._network_controller == network_controller
        assert param_set._parameter_id == 'test_10'
        assert param_set._arg_1 == 1
        assert param_set._arg_2 is None
        assert param_set._arg_3 is None
        assert param_set._arg_4 is None
        assert param_set._arg_5 is None
        assert param_set._arg_6 is None
        assert param_set._arg_7 is None
        assert param_set._arg_8 is None
        assert param_set._arg_9 is None
        assert param_set._arg_10 == '10'
        assert param_set._argc == 10

        with pytest.raises(ParameterSetException) as excinfo:
            ParameterSet(network_controller=network_controller,
                         parameter_id='test_3',
                         arg_1=1,
                         arg_10='10')

        assert str(
            excinfo.value
        ) == 'test_3 set - Wrong number of arguments. Maximum Expected: 3.'

        with pytest.raises(MambaClientException) as excinfo:
            ParameterSet(network_controller=network_controller,
                         parameter_id='wrong')

        assert str(excinfo.value) == 'ERROR wrong Non existing command'

        network_controller.close()

    def test_parameter_set_call(self):
        mock = MambaServerMock(port=34569)
        network_controller = NetworkController(port=34569)

        parameter_set = ParameterSet(network_controller=network_controller,
                                     parameter_id='test_1')

        assert mock._shared_memory['last_tc'] == 'tc_meta test_1'
        assert mock._shared_memory[
            'last_tm'] == '> OK test_1;1;test description'

        parameter_set(1)

        assert mock._shared_memory['last_tc'] == 'tc test_1 "1"'
        assert mock._shared_memory['last_tm'] == '> OK test_1'

        with pytest.raises(ParameterSetException) as excinfo:
            parameter_set(1, 2)

        assert str(
            excinfo.value
        ) == 'test_1 set - Wrong number of arguments. Expected: 1, Received: 2.'

        parameter_set = ParameterSet(network_controller=network_controller,
                                     parameter_id='test_2',
                                     arg_2='22')
        parameter_set(1)

        assert mock._shared_memory['last_tc'] == 'tc test_2 "1" "22"'
        assert mock._shared_memory['last_tm'] == '> OK test_2'

        with pytest.raises(ParameterSetException) as excinfo:
            parameter_set()

        assert str(
            excinfo.value
        ) == 'test_2 set - Wrong number of arguments. Expected: 2, Received: 0.'

        parameter_set = ParameterSet(network_controller=network_controller,
                                     parameter_id='test_1',
                                     arg_1=1)
        parameter_set()

        assert mock._shared_memory['last_tc'] == 'tc test_1 "1"'
        assert mock._shared_memory['last_tm'] == '> OK test_1'

        network_controller.close()
