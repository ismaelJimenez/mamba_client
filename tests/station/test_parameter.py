import pytest

from mamba_client.station import NetworkController, Parameter
from mamba_client.mock.mamba_server_mock import MambaServerMock
from mamba_client.station.exceptions import ParameterSetException


class TestClass:
    def test_parameter_init(self):
        MambaServerMock(port=34572)
        network_controller = NetworkController(port=34572)

        param = Parameter(parameter_id='test_1',
                          network_controller=network_controller,
                          get_alias='test_1_get',
                          set_alias='test_1_set')

        assert param._parameter_id == 'test_1'
        assert param._get is not None
        assert param._get._parameter_id == 'test_1_get'
        assert param._set is not None
        assert param._set._parameter_id == 'test_1_set'
        assert param.id == 'test_1'

        param = Parameter(parameter_id='test_1',
                          network_controller=network_controller,
                          set_alias='test_1_set')

        assert param._parameter_id == 'test_1'
        assert param._get is None
        assert param._set is not None
        assert param.id == 'test_1'

        param = Parameter(parameter_id='test_1',
                          network_controller=network_controller,
                          get_alias='test_1_get')

        assert param._parameter_id == 'test_1'
        assert param._get is not None
        assert param._set is None
        assert param.id == 'test_1'

        network_controller.close()

    def test_parameter_call(self):
        mock = MambaServerMock(port=34573)
        network_controller = NetworkController(port=34573)

        param = Parameter(parameter_id='test_1',
                          network_controller=network_controller,
                          get_alias='test_1_get',
                          set_alias='test_1_set')

        assert mock._shared_memory['last_tc'] == 'tc_meta test_1_set'
        assert mock._shared_memory[
            'last_tm'] == '> OK test_1_set;1;test description'

        reply = param.get()

        assert mock._shared_memory['last_tc'] == 'tm test_1_get'
        assert '> OK test_1_get;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        param.set(1)

        assert mock._shared_memory['last_tc'] == 'tc test_1_set "1"'
        assert mock._shared_memory['last_tm'] == '> OK test_1_set'

        with pytest.raises(ParameterSetException) as excinfo:
            param.set(1, 2)

        assert str(
            excinfo.value
        ) == 'test_1_set set - Wrong number of arguments. Expected: 1, Received: 2.'

        param = Parameter(parameter_id='test_2',
                          network_controller=network_controller,
                          get_alias='test_2_get',
                          set_alias='test_2_set',
                          set_arg_2='22')

        assert param.id == 'test_2'

        reply = param.get()

        assert mock._shared_memory['last_tc'] == 'tm test_2_get'
        assert '> OK test_2_get;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        param.set(1)

        assert mock._shared_memory['last_tc'] == 'tc test_2_set "1" "22"'
        assert mock._shared_memory['last_tm'] == '> OK test_2_set'

        with pytest.raises(ParameterSetException) as excinfo:
            param.set()

        assert str(
            excinfo.value
        ) == 'test_2_set set - Wrong number of arguments. Expected: 2, Received: 0.'

        param = Parameter(parameter_id='test_1',
                          network_controller=network_controller,
                          get_alias='test_1_get',
                          set_alias='test_1_set',
                          set_arg_1=1)

        reply = param.get()

        assert mock._shared_memory['last_tc'] == 'tm test_1_get'
        assert '> OK test_1_get;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        param.set()

        assert mock._shared_memory['last_tc'] == 'tc test_1_set "1"'
        assert mock._shared_memory['last_tm'] == '> OK test_1_set'

        network_controller.close()
