from typing import Optional, Any

from mamba_client.station import NetworkController, ParameterSet, ParameterGet


class Parameter:
    def __init__(self,
                 parameter_id: str,
                 network_controller: NetworkController,
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
        self._parameter_id = parameter_id
        self._get = ParameterGet(network_controller,
                                 get_alias) if get_alias is not None else None
        self._set = ParameterSet(
            network_controller,
            set_alias,
            arg_1=set_arg_1,
            arg_2=set_arg_2,
            arg_3=set_arg_3,
            arg_4=set_arg_4,
            arg_5=set_arg_5,
            arg_6=set_arg_6,
            arg_7=set_arg_7,
            arg_8=set_arg_8,
            arg_9=set_arg_9,
            arg_10=set_arg_10) if set_alias is not None else None

    @property
    def id(self) -> str:
        """ ID of the parameter """
        return self._parameter_id

    def get(self) -> str:
        if self._get is None:
            raise RuntimeError(
                f'Parameter {self._parameter_id} GET command is not defined.')

        return self._get()

    def set(self,
            arg_1: Optional[Any] = None,
            arg_2: Optional[Any] = None,
            arg_3: Optional[Any] = None,
            arg_4: Optional[Any] = None,
            arg_5: Optional[Any] = None,
            arg_6: Optional[Any] = None,
            arg_7: Optional[Any] = None,
            arg_8: Optional[Any] = None,
            arg_9: Optional[Any] = None,
            arg_10: Optional[Any] = None) -> None:
        if self._set is None:
            raise RuntimeError(
                f'Parameter {self._parameter_id} SET command is not defined.')

        self._set(arg_1, arg_2, arg_3, arg_4, arg_5, arg_6, arg_7, arg_8,
                  arg_9, arg_10)
