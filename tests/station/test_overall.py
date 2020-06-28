from mamba_client.station import NetworkController, Station
from mamba_client.mock.mamba_server_mock import MambaServerMock


class TestClass:
    def test_station_example(self):
        mock = MambaServerMock(port=34579)
        network_controller = NetworkController(port=34579)

        station = Station(station_id='station_1')
        station.add_instrument(instrument_id='inst_1',
                               network_controller=network_controller)

        station.inst_1.add_parameter(parameter_id='test_1')

        assert mock._shared_memory['last_tc'] == 'tc_meta inst_1_test_1'
        assert mock._shared_memory[
            'last_tm'] == '> OK inst_1_test_1;1;test description'

        reply = station.inst_1.test_1.get()

        assert mock._shared_memory['last_tc'] == 'tm inst_1_test_1'
        assert '> OK inst_1_test_1;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        station.inst_1.test_1.set(1)

        assert mock._shared_memory['last_tc'] == 'tc inst_1_test_1 "1"'
        assert mock._shared_memory['last_tm'] == '> OK inst_1_test_1'

        network_controller.close()
