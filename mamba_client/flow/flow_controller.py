from typing import List, Union, Dict, Optional, Callable

from mamba_client.flow.operator import PythonOperator, CyclicPythonOperator
from mamba_client.flow.operator.lifecycle import OperatorLifecycle
from mamba_client.flow.exceptions import MambaFlowException


class FlowController:
    def __init__(self,
                 time_ticks: int,
                 log: Optional[Callable] = None) -> None:
        if log is not None and not callable(log):
            raise MambaFlowException(
                f'FlowController log param must be callable')

        if not isinstance(time_ticks, int) or time_ticks < 0:
            raise MambaFlowException(
                f'FlowController time_ticks must be a positive integer')

        self._time_ticks = time_ticks
        self._operator_list: List[Union[PythonOperator,
                                        CyclicPythonOperator]] = []
        self._operator_lifecycle: Dict[str, OperatorLifecycle] = {}
        self._operator_downstream: Dict[str, List[Union[
            PythonOperator, CyclicPythonOperator]]] = {}
        self._log = log

    def add(self, operator: Union[PythonOperator,
                                  CyclicPythonOperator]) -> None:
        if operator.id in self._operator_lifecycle:
            raise MambaFlowException(
                f'Operator {operator.id} is already defined')

        if operator._schedule is not None and \
                operator._schedule > self._time_ticks - 1:
            raise MambaFlowException(f'Operator {operator.id} schedule is '
                                     f'greater than number of time_ticks: '
                                     f'[0-{self._time_ticks - 1}]')

        self._operator_list.append(operator)
        self._operator_lifecycle[operator.id] = operator.status

        if operator.upstream is not None:
            if operator.upstream not in self._operator_downstream:
                self._operator_downstream[operator.upstream] = [operator]
            else:
                self._operator_downstream[operator.upstream].append(operator)

    def _operation_execute(self, task, time_tick, operator_downstream):
        if task.ready(time_tick, self._operator_lifecycle):
            self._operator_lifecycle[task.id] = task.execute(time_tick)

            for operator in operator_downstream.get(task.id, []):
                self._operation_execute(operator, time_tick,
                                        operator_downstream)

    def execute(self):
        if self._log is not None:
            self._log('Start Execution Flow')

        for time_tick in range(self._time_ticks):
            if self._log is not None:
                self._log(f'=== Start Time Tick: {time_tick}')

            for task in self._operator_list:
                self._operation_execute(task, time_tick,
                                        self._operator_downstream)

        if self._log is not None:
            self._log('Stop Execution Flow')

        for task in self._operator_list:
            if task._lifecycle == OperatorLifecycle.no_status:
                if self._log is not None:
                    self._log(f'WARNING: {task.id} has not been scheduled')
