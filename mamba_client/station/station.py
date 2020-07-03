import json

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

    def import_dump_if(self, dump_file: str,
                       network_controller: NetworkController) -> None:
        with open(dump_file) as json_file:
            dump_data = json.load(json_file)
            for instr, parameters in dump_data.items():
                self.add_instrument(instrument_id=instr,
                                    network_controller=network_controller)

                param_dict = {}

                for param in parameters:
                    if param[0] not in param_dict:
                        param_dict[param[0]] = [param]
                    else:
                        param_dict[param[0]].append(param)

                for key, params in param_dict.items():
                    if len(params) == 2:
                        self._instruments[instr].add_parameter(
                            parameter_id=key,
                            parameter_get_type=params[0][2][1])
                    elif params[0][1] == 1:
                        self._instruments[instr].add_set_parameter(
                            parameter_id=key)
                    else:
                        self._instruments[instr].add_get_parameter(
                            parameter_id=key,
                            parameter_get_type=params[0][2][1])

    def add_instrument(self,
                       instrument_id: str,
                       network_controller: NetworkController,
                       alias: Optional[str] = None) -> None:
        inst_id = instrument_id if alias is None else alias

        if inst_id in self._instruments:
            raise KeyError(f'Duplicate instrument identifier {inst_id}')

        self._instruments[inst_id] = Instrument(instrument_id,
                                                network_controller)
