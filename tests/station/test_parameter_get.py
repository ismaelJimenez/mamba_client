from mamba_client.station import NetworkController, ParameterGet
from mamba_client.mock.mamba_server_mock import MambaServerMock


class TestClass:
    def test_parameter_get_init(self):
        MambaServerMock(port=34562)
        network_controller = NetworkController(port=34562)

        param_set = ParameterGet(network_controller=network_controller,
                                 parameter_id='test_1')

        assert param_set._network_controller == network_controller
        assert param_set._parameter_id == 'test_1'

        network_controller.close()

    def test_parameter_set_call(self):
        mock = MambaServerMock(port=34563)
        network_controller = NetworkController(port=34563)

        parameter_get = ParameterGet(network_controller=network_controller,
                                     parameter_id='test_1')

        assert mock._shared_memory['last_tc'] == 'tm_meta test_1'
        assert mock._shared_memory[
            'last_tm'] == '> OK test_1;str;str;test description;7;4'

        reply = parameter_get()

        assert mock._shared_memory['last_tc'] == 'tm test_1'
        assert '> OK test_1;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'
