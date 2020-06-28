from typing import Optional, Any, Union, Dict, Callable

from mamba_client.flow.operator.lifecycle import OperatorLifecycle
from mamba_client.log import log_info
from mamba_client.flow.exceptions import MambaFlowException
from mamba_client.station.station import Station


class CyclicPythonOperator:
    def __init__(self,
                 operator_id: Union[str, int],
                 python_callable: Callable,
                 schedule: int,
                 cycle: int,
                 schedule_end: Optional[int] = None,
                 context: Optional[Dict] = None,
                 station: Optional[Station] = None,
                 op_args: Optional[Any] = None,
                 description: str = '') -> None:

        if not isinstance(schedule, int) or schedule < 0:
            raise MambaFlowException(
                f'Operator {operator_id} schedule must be a positive integer')

        if not isinstance(cycle, int) or cycle < 0:
            raise MambaFlowException(
                f'Operator {operator_id} cycle must be a positive integer')

        if schedule_end is not None and (not isinstance(schedule_end, int)
                                         or schedule_end < 0):
            raise MambaFlowException(
                f'Operator {operator_id} schedule_end must be a positive '
                f'integer or None'
            )

        if not callable(python_callable):
            raise MambaFlowException(
                '"python_callable" param must be callable')

        self._operator_id = str(operator_id)
        self._callable = python_callable
        self._context = context
        self._station = station
        self._schedule = schedule
        self._cycle = cycle
        self._schedule_end = schedule_end
        self._description = description
        self._op_args = op_args
        self._lifecycle = OperatorLifecycle.no_status

    @property
    def id(self):
        return self._operator_id

    def ready(self, iteration: int,
              operators_lifecycle: Dict[str, OperatorLifecycle]) -> bool:
        if self._lifecycle == OperatorLifecycle.success:
            return False
        if self._schedule_end is not None and self._schedule_end < iteration:
            self._lifecycle = OperatorLifecycle.success
            return False
        elif iteration - self._schedule < 0:
            return False
        else:
            return ((iteration - self._schedule) % self._cycle) == 0

    def execute(self, iteration: int) -> OperatorLifecycle:
        log_info(self._operator_id, 'Start Task Execution')
        self._callable(iteration, self._station, self._context, self._op_args)
        log_info(self._operator_id, 'Stop Task Execution')

        if self._schedule_end is not None and self._schedule_end < iteration:
            self._lifecycle = OperatorLifecycle.success
        else:
            self._lifecycle = OperatorLifecycle.running

        return self._lifecycle
