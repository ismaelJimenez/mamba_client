import os
import pytest

from mamba_client.station import NetworkController, Station
from mamba_client.mock.mamba_server_mock import MambaServerMock


class TestClass:
    def test_parameter_init(self):
        mock = MambaServerMock(port=34577)
        network_controller = NetworkController(port=34577)

        station = Station(station_id='station_1')

        assert station._id == 'station_1'
        assert station._instruments == {}

        station.add_instrument(instrument_id='instrument_1',
                               network_controller=network_controller)

        assert list(station._instruments.keys()) == ['instrument_1']
        assert station.instrument_1.id == 'instrument_1'

        station.add_instrument(instrument_id='instrument_2',
                               network_controller=network_controller,
                               alias='inst_2')

        assert list(station._instruments.keys()) == ['instrument_1', 'inst_2']
        assert station.inst_2.id == 'instrument_2'

        with pytest.raises(AttributeError) as excinfo:
            station.instrument_2

        assert str(excinfo.value
                   ) == 'station_1 station has no instrument instrument_2'

        station.import_dump_if(
            os.path.join(os.path.dirname(__file__), 'example_mamba_if.json'),
            network_controller)
        assert list(station._instruments.keys()) == [
            'instrument_1', 'inst_2', 'dump_1', 'dump_2'
        ]
        assert list(station._instruments['dump_1']._parameters.keys()) == [
            'set_1', 'get_1', 'param_1'
        ]
        assert list(station._instruments['dump_2']._parameters.keys()) == [
            'set_2', 'get_2', 'param_2'
        ]

        reply = station.dump_1.param_1.get()

        assert mock._shared_memory['last_tc'] == 'tm dump_1_param_1'
        assert '> OK dump_1_param_1;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == '1'

        station.dump_1.param_1.set(1)

        assert mock._shared_memory['last_tc'] == 'tc dump_1_param_1 "1"'
        assert mock._shared_memory['last_tm'] == '> OK dump_1_param_1'

        reply = station.dump_1.get_1.get()

        assert mock._shared_memory['last_tc'] == 'tm dump_1_get_1'
        assert '> OK dump_1_get_1;' in mock._shared_memory['last_tm']
        assert ';1;1;0;1' in mock._shared_memory['last_tm']
        assert reply == 1

        network_controller.close()
