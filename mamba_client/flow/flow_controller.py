from typing import List, Union, Dict, Optional, Callable

from mamba_client.flow.operator import PythonOperator, CyclicPythonOperator
from mamba_client.flow.operator.lifecycle import OperatorLifecycle
from mamba_client.flow.exceptions import MambaFlowException


class FlowController:
    def __init__(self,
                 iterations: int,
                 log: Optional[Callable] = None) -> None:
        if log is not None and not callable(log):
            raise MambaFlowException(
                f'FlowController log param must be callable')

        if not isinstance(iterations, int) or iterations < 0:
            raise MambaFlowException(
                f'FlowController iterations must be a positive integer')

        self._iterations = iterations
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
                operator._schedule > self._iterations - 1:
            raise MambaFlowException(f'Operator {operator.id} schedule is '
                                     f'greater than number of iterations: '
                                     f'[0-{self._iterations -1}]')

        self._operator_list.append(operator)
        self._operator_lifecycle[operator.id] = operator.status

        if operator.upstream is not None:
            if operator.upstream not in self._operator_lifecycle:
                raise MambaFlowException(f'Operator {operator.id} upstream '
                                         f'{operator.upstream} does not '
                                         f'exists')

            if operator.upstream not in self._operator_downstream:
                self._operator_downstream[operator.upstream] = [operator]
            else:
                self._operator_downstream[operator.upstream].append(operator)

    def execute(self):
        if self._log is not None:
            self._log('Start Execution Flow')

        for loop in range(self._iterations):
            if self._log is not None:
                self._log(f'Start iteration {loop}')

            for task in self._operator_list:
                if task.ready(loop, self._operator_lifecycle):
                    self._operator_lifecycle[task.id] = task.execute(loop)

                    if self._operator_lifecycle[
                            task.id] == OperatorLifecycle.success:
                        if task.id in self._operator_downstream:
                            for operator in self._operator_downstream[task.id]:
                                self._operator_lifecycle[
                                    operator.id] = operator.execute(loop)

        if self._log is not None:
            self._log('Stop Execution Flow')
