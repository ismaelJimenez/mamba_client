from typing import Optional, Dict, Any

from mamba_client.station import NetworkController, Parameter


class Instrument:
    def __init__(self, instrument_id: str,
                 network_controller: NetworkController) -> None:
        self._id = instrument_id
        self._network_controller = network_controller

        self._parameters: Dict[str, Parameter] = {}

    def __getattr__(self, parameter_id: str) -> Parameter:
        try:
            return self._parameters[parameter_id]
        except KeyError:
            raise AttributeError(
                f'{self._id} instrument has no property {parameter_id}')

    @property
    def id(self) -> str:
        """ Name of the instrument """
        return self._id

    def add_parameter(self,
                      parameter_id: str,
                      get_alias: Optional[str] = None,
                      set_alias: Optional[str] = None,
                      set_arg_1: Optional[Any] = None,
                      set_arg_2: Optional[Any] = None,
                      set_arg_3: Optional[Any] = None,
                      set_arg_4: Optional[Any] = None,
                      set_arg_5: Optional[Any] = None,
                      set_arg_6: Optional[Any] = None,
                      set_arg_7: Optional[Any] = None,
                      set_arg_8: Optional[Any] = None,
                      set_arg_9: Optional[Any] = None,
                      set_arg_10: Optional[Any] = None) -> None:

        if parameter_id in self._parameters:
            raise KeyError(f'Duplicate parameter name {parameter_id}')

        get_alias = get_alias if get_alias is not None else \
            f'{self._id}_{parameter_id}'
        set_alias = set_alias if set_alias is not None else \
            f'{self._id}_{parameter_id}'

        self._parameters[parameter_id] = Parameter(
            parameter_id=parameter_id,
            network_controller=self._network_controller,
            get_alias=get_alias,
            set_alias=set_alias,
            set_arg_1=set_arg_1,
            set_arg_2=set_arg_2,
            set_arg_3=set_arg_3,
            set_arg_4=set_arg_4,
            set_arg_5=set_arg_5,
            set_arg_6=set_arg_6,
            set_arg_7=set_arg_7,
            set_arg_8=set_arg_8,
            set_arg_9=set_arg_9,
            set_arg_10=set_arg_10)

    def add_get_parameter(self,
                          parameter_id: str,
                          get_alias: Optional[str] = None) -> None:
        if parameter_id in self._parameters:
            raise KeyError(f'Duplicate parameter name {parameter_id}')

        get_alias = get_alias if get_alias is not None else \
            f'{self._id}_{parameter_id}'

        self._parameters[parameter_id] = Parameter(
            parameter_id=parameter_id,
            network_controller=self._network_controller,
            get_alias=get_alias,
            set_alias=None)

    def add_set_parameter(self,
                          parameter_id: str,
                          set_alias: Optional[str] = None,
                          set_arg_1: Optional[Any] = None,
                          set_arg_2: Optional[Any] = None,
                          set_arg_3: Optional[Any] = None,
                          set_arg_4: Optional[Any] = None,
                          set_arg_5: Optional[Any] = None,
                          set_arg_6: Optional[Any] = None,
                          set_arg_7: Optional[Any] = None,
                          set_arg_8: Optional[Any] = None,
                          set_arg_9: Optional[Any] = None,
                          set_arg_10: Optional[Any] = None) -> None:

        if parameter_id in self._parameters:
            raise KeyError(f'Duplicate parameter name {parameter_id}')

        set_alias = set_alias if set_alias is not None else \
            f'{self._id}_{parameter_id}'

        self._parameters[parameter_id] = Parameter(
            parameter_id=parameter_id,
            network_controller=self._network_controller,
            get_alias=None,
            set_alias=set_alias,
            set_arg_1=set_arg_1,
            set_arg_2=set_arg_2,
            set_arg_3=set_arg_3,
            set_arg_4=set_arg_4,
            set_arg_5=set_arg_5,
            set_arg_6=set_arg_6,
            set_arg_7=set_arg_7,
            set_arg_8=set_arg_8,
            set_arg_9=set_arg_9,
            set_arg_10=set_arg_10)
