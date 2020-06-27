from typing import Optional, Any

from mamba_client.station import NetworkController
from mamba_client.station.exceptions import ParameterSetException


class ParameterSet:
    """ Parameter Setter """
    def __init__(self,
                 network_controller: NetworkController,
                 parameter_id: str,
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
        self._network_controller = network_controller
        self._parameter_id = parameter_id

        reply = self._network_controller.query(
            f'tc_meta {self._parameter_id}').split(";")

        self._argc = int(reply[1])

        self._arg_1 = arg_1
        self._arg_2 = arg_2
        self._arg_3 = arg_3
        self._arg_4 = arg_4
        self._arg_5 = arg_5
        self._arg_6 = arg_6
        self._arg_7 = arg_7
        self._arg_8 = arg_8
        self._arg_9 = arg_9
        self._arg_10 = arg_10

        if (self._argc == 1 and
            (self._arg_2 is not None or self._arg_3 is not None or self._arg_4
             is not None or self._arg_5 is not None or self._arg_6 is not None
             or self._arg_7 is not None or self._arg_8 is not None
             or self._arg_9 is not None or self._arg_10 is not None)) or (
                 self._argc == 2 and
                 (self._arg_3 is not None or self._arg_4 is not None
                  or self._arg_5 is not None or self._arg_6 is not None
                  or self._arg_7 is not None or self._arg_8 is not None
                  or self._arg_9 is not None or self._arg_10 is not None)
             ) or (self._argc == 3 and
                   (self._arg_4 is not None or self._arg_5 is not None
                    or self._arg_6 is not None or self._arg_7 is not None
                    or self._arg_8 is not None or self._arg_9 is not None
                    or self._arg_10 is not None)) or (self._argc == 4 and (
                        self._arg_5 is not None or self._arg_6 is not None
                        or self._arg_7 is not None or self._arg_8 is not None
                        or self._arg_9 is not None or self._arg_10 is not None
                    )) or (self._argc == 5 and
                           (self._arg_6 is not None or self._arg_7 is not None
                            or self._arg_8 is not None or self._arg_9
                            is not None or self._arg_10 is not None)) or (
                                self._argc == 6 and
                                (self._arg_7 is not None or self._arg_8
                                 is not None or self._arg_9 is not None
                                 or self._arg_10 is not None)) or (
                                     self._argc == 7 and
                                     (self._arg_8 is not None or self._arg_9
                                      is not None or self._arg_10 is not None)
                                 ) or (self._argc == 8 and
                                       (self._arg_9 is not None
                                        or self._arg_10 is not None)) or (
                                            self._argc == 9 and
                                            (self._arg_10 is not None)):
            raise ParameterSetException(
                f'{self._parameter_id} set - Wrong '
                f'number of arguments. Maximum Expected: '
                f'{self._argc}.')

    def __call__(self,
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

        args = []

        for local_arg, global_arg in [
            (arg_1, self._arg_1), (arg_2, self._arg_2), (arg_3, self._arg_3),
            (arg_4, self._arg_4), (arg_5, self._arg_5), (arg_6, self._arg_6),
            (arg_7, self._arg_7), (arg_8, self._arg_8), (arg_9, self._arg_9),
            (arg_10, self._arg_10)
        ]:
            if local_arg is not None:
                args.append('"' + str(local_arg) + '"')
            elif global_arg is not None:
                args.append('"' + str(global_arg) + '"')
            else:
                break

        if len(args) != self._argc:
            raise ParameterSetException(f'{self._parameter_id} set - Wrong '
                                        f'number of arguments. Expected: '
                                        f'{self._argc}, Received: '
                                        f'{len(args)}.')

        self._network_controller.query(
            f'tc {self._parameter_id} {" ".join(args)}')
