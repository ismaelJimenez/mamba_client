from typing import Any

from mamba_client.station import NetworkController


class ParameterGet:
    """ Parameter Getter """
    def __init__(self,
                 network_controller: NetworkController,
                 parameter_id: str,
                 parameter_type: str = 'str') -> None:
        self._network_controller = network_controller
        self._parameter_id = parameter_id
        self._parameter_type = parameter_type

        self._network_controller.query(f'tm_meta {self._parameter_id}').split(
            ";")

    def __call__(self) -> Any:
        reply = self._network_controller.query(
            f'tm {self._parameter_id}').split(";")

        tm_time = float(reply[1])

        if tm_time > 0:
            reply_value = reply[2]
        else:
            reply_value = ''

        if self._parameter_type == 'hex':
            return int(reply_value, 16)
        elif self._parameter_type == 'int':
            return int(reply_value)
        elif self._parameter_type == 'float':
            return float(reply_value)
        else:
            return reply_value
