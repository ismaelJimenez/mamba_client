import time

from typing import Optional, Any, Union, Dict, Callable

from mamba_client.flow.operator.lifecycle import OperatorLifecycle
from mamba_client.flow.exceptions import MambaFlowException
from mamba_client.station.station import Station


class PythonOperator:
    def __init__(self,
                 operator_id: Union[str, int],
                 python_callable: Callable,
                 schedule: Optional[int] = None,
                 schedule_ts: Optional[int] = None,
                 upstream: Optional[str] = None,
                 context: Optional[Dict] = None,
                 station: Optional[Station] = None,
                 op_args: Optional[Any] = None,
                 description: str = '',
                 log: Optional[Callable] = None) -> None:
        if upstream is not None and (schedule is not None or schedule_ts is not None):
            raise MambaFlowException(
                f'Operator {operator_id} can not have schedule and upstream')

        if schedule is not None and schedule_ts is not None:
            raise MambaFlowException(
                f'Operator {operator_id} can not have schedule and schedule_ts')

        if upstream is None and schedule is None and schedule_ts is None:
            raise MambaFlowException(
                f'Operator {operator_id} must have schedule or upstream')

        if schedule is not None and (not isinstance(schedule, int)
                                     or schedule < 0):
            raise MambaFlowException(
                f'Operator {operator_id} schedule must be a positive integer')

        if schedule_ts is not None and (not isinstance(schedule_ts, int)
                                        or schedule_ts < 0):
            raise MambaFlowException(
                f'Operator {operator_id} schedule_ts must be a positive integer')

        if not callable(python_callable):
            raise MambaFlowException(
                f'Operator {operator_id} python_callable param must be '
                f'callable')

        if log is not None and not callable(log):
            raise MambaFlowException(
                f'Operator {operator_id} log param must be callable')

        self._t0 = time.time()
        self._operator_id = str(operator_id)
        self._callable = python_callable
        self._context = context
        self._station = station
        self._schedule = schedule
        self._schedule_ts = schedule_ts
        self._upstream = upstream
        self._description = description
        self._op_args = op_args
        self._log = log
        self._lifecycle = OperatorLifecycle.no_status

    @property
    def id(self):
        return self._operator_id

    @property
    def upstream(self):
        return self._upstream

    @property
    def status(self):
        return self._lifecycle

    def ready(self, iteration: int,
              operators_lifecycle: Dict[str, OperatorLifecycle]) -> bool:
        if self._lifecycle == OperatorLifecycle.success:
            return False

        if self._upstream is not None:
            return operators_lifecycle.get(
                self._upstream) == OperatorLifecycle.success
        elif self._schedule is not None:
            return self._schedule <= iteration if self._schedule is not None\
                else False
        elif self._schedule_ts is not None:
            return self._schedule_ts <= (time.time() - self._t0)
        else:
            return False

    def execute(self, iteration: int) -> OperatorLifecycle:
        if self._log is not None:
            self._log(f'[INFO] [{time.strftime("%Y%m%dT%H%M%S")}] '
                      f'[{self._operator_id}] Start Operator Execution')

        self._callable(iteration, self._station, self._context, self._op_args)

        if self._log is not None:
            self._log(f'[INFO] [{time.strftime("%Y%m%dT%H%M%S")}] '
                      f'[{self._operator_id}] Stop Operator Execution')

        self._lifecycle = OperatorLifecycle.success

        return self._lifecycle
