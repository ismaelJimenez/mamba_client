from typing import Optional, Dict

from mamba_client.station import NetworkController, Instrument


class Station:
    def __init__(self, station_id: str) -> None:
        self._id = station_id

        self._instruments: Dict[str, Instrument] = {}

    @property
    def id(self) -> str:
        """ Name of the instrument """
        return self._id

    def __getattr__(self, instrument_id: str) -> Instrument:
        try:
            return self._instruments[instrument_id]
        except KeyError:
            raise AttributeError(
                f'{self._id} station has no instrument {instrument_id}')

    def add_instrument(self,
                       instrument_id: str,
                       network_controller: NetworkController,
                       alias: Optional[str] = None) -> None:
        inst_id = instrument_id if alias is None else alias

        if inst_id in self._instruments:
            raise KeyError(f'Duplicate instrument identifier {inst_id}')

        self._instruments[inst_id] = Instrument(instrument_id,
                                                network_controller)
