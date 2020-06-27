import pytest

from mamba_client.station import NetworkController, Station
from mamba_client.mock.mamba_server_mock import MambaServerMock
from mamba_client.station.exceptions import ParameterSetException


class TestClass:
    def test_parameter_init(self):
        MambaServerMock(port=34577)
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

        network_controller.close()
